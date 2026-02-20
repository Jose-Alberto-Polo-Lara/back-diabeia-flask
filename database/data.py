"""
Data Layer - Conexión genérica a PostgreSQL
Adaptado desde TypeScript a Python usando psycopg2
"""
import os
from typing import Any, Dict, List, Optional, Callable
from psycopg2 import pool, extras
from contextlib import contextmanager
import re


class Query:
    """
    Clase para ejecutar consultas y funciones de PostgreSQL de forma genérica.
    
    Características:
    - Pool de conexiones reutilizable
    - Ejecución de funciones SQL automática
    - Soporte para placeholders dinámicos
    - Manejo de errores estructurado
    """
    
    _pool: Optional[pool.SimpleConnectionPool] = None
    
    def _get_pool(self) -> pool.SimpleConnectionPool:
        """Obtiene o crea el pool de conexiones PostgreSQL"""
        if self._pool:
            return self._pool
        
        env = os.getenv('FLASK_ENV', 'development')
        
        # Importar configuración desde config_db
        try:
            from .config_db import get_db_config
            db_config = get_db_config(env)
            
            config = {
                'host': db_config.get('server', 'localhost'),
                'user': db_config.get('user', 'postgres'),
                'password': db_config.get('password', ''),
                'database': db_config.get('database', 'mydb'),
                'port': db_config.get('port', 5432),
            }
        except Exception:
            # Fallback a variables de entorno si no se encuentra config_db
            config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'mydb'),
                'port': int(os.getenv('DB_PORT', '5432')),
            }
        
        # Crear pool con mínimo 1 y máximo 10 conexiones
        self._pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            **config
        )
        
        return self._pool
    
    @contextmanager
    def _get_connection(self):
        """Context manager para obtener y liberar conexiones del pool"""
        pool_instance = self._get_pool()
        conn = pool_instance.getconn()
        try:
            yield conn
        finally:
            pool_instance.putconn(conn)
    
    def _build_sql(self, sp: str, params: Optional[Dict[str, Any]]) -> tuple:
        """
        Construye la consulta SQL y los valores de parámetros.
        
        Si `sp` es solo el nombre de una función, construye: SELECT * FROM func($1, $2, ...)
        Si `sp` es una consulta completa, la usa directamente.
        
        Args:
            sp: Nombre de función o consulta SQL completa
            params: Diccionario de parámetros
            
        Returns:
            Tuple (sql_query, list_of_values)
        """
        sp_trim = sp.strip() if sp else ''
        values = list(params.values()) if params else []
        
        # Si parece una consulta completa (contiene SELECT, WITH, INSERT, UPDATE, DELETE)
        sql_keywords = re.compile(r'\b(SELECT|INSERT|UPDATE|DELETE|WITH)\b', re.IGNORECASE)
        
        if sql_keywords.search(sp_trim) or '(' in sp_trim:
            # Es una consulta SQL completa, usarla directamente
            sql_to_execute = sp_trim
        else:
            # Es el nombre de una función, construir SELECT * FROM func(...)
            if params:
                placeholders = ', '.join([f'%s' for _ in params])
                sql_to_execute = f"SELECT * FROM {sp_trim}({placeholders})"
            else:
                sql_to_execute = f"SELECT * FROM {sp_trim}()"
        
        return sql_to_execute, values
    
    def sp_execute(
        self, 
        params: Optional[Dict[str, Any]] = None, 
        sp: str = '', 
        auto_close: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta una consulta SQL o función de PostgreSQL.
        
        Args:
            params: Diccionario con parámetros {key: value}
            sp: Nombre de función o consulta SQL completa con placeholders %s
            auto_close: Si es True, cierra el pool después de ejecutar
            
        Returns:
            Dict con estructura:
            {
                'error': None o exception,
                'excepcion': None o exception,
                'recordsets': Lista de registros (dicts)
            }
            
        Raises:
            Exception si hay error en la ejecución
            
        Ejemplos:
            # Ejecutar función
            query.sp_execute({'id': 1}, 'get_user_by_id')
            
            # Ejecutar SQL directo
            query.sp_execute({'name': 'Juan'}, 'SELECT * FROM users WHERE name = %s')
        """
        try:
            sql_query, values = self._build_sql(sp, params)
            
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                    cursor.execute(sql_query, values)

                    # Commit de la transacción siempre después de ejecutar la consulta.
                    # Esto asegura que las funciones de Postgres que realizan INSERT
                    # y además retornan valores (cursor.description is True) vean
                    # sus cambios persistidos.
                    try:
                        conn.commit()
                    except Exception:
                        # No bloquear si el commit falla aquí; el error se manejará
                        # en el bloque externo.
                        pass

                    # Verificar si es una consulta que retorna datos
                    if cursor.description:
                        rows = cursor.fetchall()
                        # Convertir RealDictRow a dict normal
                        recordsets = [dict(row) for row in rows]
                    else:
                        # Para INSERT, UPDATE, DELETE sin RETURNING
                        recordsets = []
                    
                    result = {
                        'error': None,
                        'excepcion': None,
                        'recordsets': recordsets
                    }
                    
                    return result
                    
        except Exception as err:
            result = {
                'error': err,
                'excepcion': err,
                'recordsets': None
            }
            # Re-raise the original exception so Flask/CORS error handlers
            # receive a proper Exception object (raising a dict caused
            # TypeError: exceptions must derive from BaseException).
            raise
            
        finally:
            if auto_close:
                try:
                    self.close()
                except Exception:
                    pass  # No bloquear por errores al cerrar
    
    def sp_execute_param(
        self,
        params: Optional[Dict[str, Any]] = None,
        sp: str = '',
        cb: Optional[Callable] = None,
        auto_close: bool = False
    ) -> Dict[str, Any]:
        """
        Ejecuta una consulta SQL y acepta callback opcional.
        
        Args:
            params: Diccionario de parámetros
            sp: Nombre de función o consulta SQL
            cb: Función callback que recibe el resultado
            auto_close: Si es True, cierra el pool después
            
        Returns:
            Resultado de la ejecución
        """
        try:
            result = self.sp_execute(params, sp, auto_close)
            if cb:
                cb(result)
            return result
        except Exception as err:
            if cb:
                cb(err)
            raise err
    
    def close(self):
        """Cierra todas las conexiones del pool"""
        if self._pool:
            self._pool.closeall()
            self._pool = None
    
    def __enter__(self):
        """Permite usar la clase como context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el pool al salir del contexto"""
        self.close()


# Instancia singleton para uso global
query_instance = Query()


def execute_query(params: Optional[Dict[str, Any]] = None, sp: str = '') -> Dict[str, Any]:
    """
    Función helper para ejecutar consultas de forma rápida.
    
    Ejemplos:
        result = execute_query({'id': 1}, 'get_user_by_id')
        users = result['recordsets']
    """
    return query_instance.sp_execute(params, sp, auto_close=False)
