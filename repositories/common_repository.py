"""
Common Repository
Contiene métodos comunes que ejecutan funciones de PostgreSQL
Traducido desde TypeScript
"""
from database import Query
from typing import Any, Dict, Optional


class CommonRepository:
    """
    Repositorio común con métodos que ejecutan funciones de PostgreSQL.
    Equivalente al CommonRepository de TypeScript.
    """
    
    def __init__(self):
        """Inicializa el repositorio con una instancia de Query"""
        self.query = Query()
    
    # ************ SERVICIOS GET ************
    
    def get_data_moment_to_day_db(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtiene datos de momentos del día para toma de muestra.
        Ejecuta la función PostgreSQL: catalogomomentotomamuestra
        
        Args:
            query_params: Diccionario con parámetros para la función
            
        Returns:
            Dict con estructura: {'error': None, 'excepcion': None, 'recordsets': [...]}
            
        Example:
            result = repo.get_data_moment_to_day_db({})
            moments = result['recordsets']
        """
        return self.query.sp_execute(query_params, 'catalogomomentotomamuestra')
    
    def get_data_activity_fisica_db(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Obtiene catálogo de actividad física.
        Ejecuta la función PostgreSQL: catalogo_actividad_fisica_fn
        
        Args:
            query_params: Diccionario con parámetros para la función
            
        Returns:
            Dict con estructura: {'error': None, 'excepcion': None, 'recordsets': [...]}
            
        Example:
            result = repo.get_data_activity_fisica_db({})
            activities = result['recordsets']
        """
        return self.query.sp_execute(query_params, 'catalogo_actividad_fisica_fn')
    
    # ************ SERVICIOS POST ************
    
    def post_ins_glucose_record(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserta un registro de glucosa.
        Ejecuta la función PostgreSQL: ins_glucose_record
        
        Args:
            query_params: Diccionario con los datos del registro de glucosa
                         Ejemplo: {'user_id': 1, 'glucose_value': 120, 'moment_id': 2, ...}
            
        Returns:
            Dict con estructura: {'error': None, 'excepcion': None, 'recordsets': [...]}
            
        Example:
            result = repo.post_ins_glucose_record({
                'user_id': 1,
                'glucose_value': 120,
                'moment_id': 2,
                'date': '2024-02-19'
            })
            new_record = result['recordsets']
        """
        return self.query.sp_execute(query_params, 'ins_glucose_record')
    
    def close(self):
        """Cierra la conexión del pool"""
        self.query.close()
    
    def __enter__(self):
        """Permite usar el repository como context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra el pool al salir del contexto"""
        self.close()
