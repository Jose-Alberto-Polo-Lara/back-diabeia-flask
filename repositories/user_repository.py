"""
User Repository
Maneja todas las operaciones de base de datos relacionadas con usuarios
Usa procedimientos almacenados de PostgreSQL a través de Query
"""
from database import Query
from typing import Any, Dict, Optional




class UserRepository:
   """
   Repositorio para operaciones de usuarios en PostgreSQL.
   Ejecuta procedimientos almacenados usando la clase Query.
   Similar al patrón usado en CommonRepository.
   """
  
   def __init__(self):
       """Inicializa el repositorio con una instancia de Query"""
       self.query = Query()
  
   # ============================================
   # AUTENTICACIÓN
   # ============================================
  
   def validate_login(self, username: str, password: str) -> Dict[str, Any]:
       """
       Valida credenciales de usuario usando el procedimiento almacenado validate_login.
      
       El procedimiento almacenado valida las credenciales dentro de PostgreSQL
       y retorna datos del usuario SIN exponer la contraseña.
      
       Args:
           username: Nombre de usuario
           password: Contraseña en texto plano
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [{
                   'is_valid': bool,      # True si credenciales correctas
                   'user_id': int,        # ID del usuario
                   'username': str,       # Nombre de usuario
                   'name': str,           # Nombre completo
                   'email': str,          # Email (si existe)
                   'message': str         # Mensaje de resultado
               }]
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.validate_login('admin', 'password123')
           >>> if result['recordsets'] and result['recordsets'][0]['is_valid']:
           >>>    print(f"Login exitoso, user_id: {result['recordsets'][0]['user_id']}")
       """
       query_params = {
           'username': username,
           'password': password
       }
       return self.query.sp_execute(query_params, 'validate_login')
  
  
   def register_user(
       self,
       username: str,
       password: str,
       name: Optional[str] = None,
       email: Optional[str] = None
   ) -> Dict[str, Any]:
       """
       Registra un nuevo usuario usando el procedimiento almacenado register_user.
      
       El procedimiento almacenado valida que el username no exista
       y registra al usuario en la base de datos.
      
       Args:
           username: Nombre de usuario (único)
           password: Contraseña en texto plano
           name: Nombre completo del usuario (opcional)
           email: Email del usuario (opcional)
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [{
                   'success': bool,       # True si registro exitoso
                   'user_id': int,        # ID del nuevo usuario
                   'message': str         # Mensaje de resultado
               }]
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.register_user('nuevo', 'pass123', 'Nuevo Usuario')
           >>> if result['recordsets'] and result['recordsets'][0]['success']:
           >>>    print(f"Usuario creado con ID: {result['recordsets'][0]['user_id']}")
       """
       query_params = {
           'username': username,
           'password': password,
           'name': name,
           'email': email
       }
       return self.query.sp_execute(query_params, 'register_user')
  
  
   def update_last_login(self, user_id: int) -> Dict[str, Any]:
       """
       Actualiza la fecha del último login del usuario.
       Ejecuta el procedimiento almacenado: update_last_login
      
       Args:
           user_id: ID del usuario
      
       Returns:
           Dict con estructura: {'error': None, 'excepcion': None, 'recordsets': []}
      
       Example:
           >>> repo = UserRepository()
           >>> repo.update_last_login(1)
       """
       query_params = {'user_id': user_id}
       return self.query.sp_execute(query_params, 'update_last_login')
  
  
   # ============================================
   # CONSULTAS
   # ============================================
  
   def check_username_exists(self, username: str) -> Dict[str, Any]:
       """
       Verifica si un nombre de usuario ya existe.
       Ejecuta el procedimiento almacenado: check_username_exists
      
       Args:
           username: Nombre de usuario a verificar
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [bool]  # True si existe, False si no
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.check_username_exists('admin')
           >>> exists = result['recordsets'][0] if result['recordsets'] else False
           >>> if exists:
           >>>    print("El username ya está en uso")
       """
       query_params = {'username': username}
       return self.query.sp_execute(query_params, 'check_username_exists')
  
  
   def find_by_id(self, user_id: int) -> Dict[str, Any]:
       """
       Busca un usuario por su ID.
       Ejecuta consulta SQL directa (sin procedimiento almacenado)
      
       Args:
           user_id: ID del usuario
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [{
                   'id': int,
                   'username': str,
                   'name': str,
                   'email': str,
                   'is_active': bool,
                   'created_at': datetime,
                   'last_login': datetime
               }]
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.find_by_id(1)
           >>> if result['recordsets']:
           >>>    user = result['recordsets'][0]
           >>>    print(f"Usuario: {user['username']}")
       """
       query_params = {'user_id': user_id}
       sql_query = """
           SELECT id, username, name, email, is_active, created_at, last_login
           FROM users
           WHERE id = %s
       """
       return self.query.sp_execute(query_params, sql_query)
  
  
   def find_by_username(self, username: str) -> Dict[str, Any]:
       """
       Busca un usuario por su nombre de usuario.
       Ejecuta consulta SQL directa (sin procedimiento almacenado)
      
       Args:
           username: Nombre de usuario
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [{
                   'id': int,
                   'username': str,
                   'name': str,
                   'email': str,
                   'is_active': bool,
                   'created_at': datetime,
                   'last_login': datetime
               }]
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.find_by_username('admin')
           >>> if result['recordsets']:
           >>>    user = result['recordsets'][0]
           >>>    print(f"ID: {user['id']}")
       """
       query_params = {'username': username}
       sql_query = """
           SELECT id, username, name, email, is_active, created_at, last_login
           FROM users
           WHERE username = %s
       """
       return self.query.sp_execute(query_params, sql_query)
  
  
   # ============================================
   # ADMINISTRACIÓN
   # ============================================
  
   def deactivate_user(self, username: str) -> Dict[str, Any]:
       """
       Desactiva una cuenta de usuario (no la elimina).
       Ejecuta el procedimiento almacenado: deactivate_user
      
       Args:
           username: Nombre de usuario a desactivar
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [bool]  # True si se desactivó, False si no existe
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.deactivate_user('usuario1')
           >>> success = result['recordsets'][0] if result['recordsets'] else False
           >>> if success:
           >>>    print("Usuario desactivado")
       """
       query_params = {'username': username}
       return self.query.sp_execute(query_params, 'deactivate_user')
   
   def catalog_menu(self, iduser: int) -> Dict[int, Any]:
       """
       Obtiene el catálogo de menú para un usuario específico.
       Ejecuta el procedimiento almacenado: catalog_menu
      
       Args:
           iduser: ID del usuario para quien obtener el catálogo
      
       Returns:
           Dict con estructura: {
               'error': None,
               'excepcion': None,
               'recordsets': [bool]  # True si se desactivó, False si no existe
           }
      
       Example:
           >>> repo = UserRepository()
           >>> result = repo.deactivate_user('usuario1')
           >>> success = result['recordsets'][0] if result['recordsets'] else False
           >>> if success:
           >>>    print("Usuario desactivado")
       """
       query_params = {'iduser': iduser}
       return self.query.sp_execute(query_params, 'fn_menu')
  
   # ============================================
   # UTILIDADES
   # ============================================
  
   def close(self):
       """Cierra la conexión del pool"""
       self.query.close()
  
   def __enter__(self):
       """Permite usar el repository como context manager"""
       return self
  
   def __exit__(self, exc_type, exc_val, exc_tb):
       """Cierra el pool al salir del contexto"""
       self.close()
