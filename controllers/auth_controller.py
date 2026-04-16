"""
Controlador de autenticación
Maneja login, registro y validación de usuarios
USA PATRÓN REPOSITORY para acceso a datos
"""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import generate_token, token_required
from repositories.user_repository import UserRepository


# Crear el blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)


# Instancia única del repository (igual que common_controller)
user_repository = UserRepository()




# ============================================
# RUTA DE REGISTRO (SIGN UP)
# ============================================
@auth_bp.route('/register', methods=['POST'])
def register():
   """
   Registra un nuevo usuario en el sistema
  
   @author Jose Alberto Polo Lara
   fn: register_user
   URL: http://{server}:{port}/api/auth/register
  
   Body (JSON):
   {
       "username": "nombre_usuario",
       "password": "contraseña123",
       "name": "Nombre Usuario",
       "email": "usuario@example.com"
   }
  
   Returns:
       JSON con el resultado del registro y token JWT
   """
   data = request.get_json()
  
   # Registrar usuario
   result = user_repository.register_user(
       username=data.get('username'),
       password=data.get('password'),
       name=data.get('name', ''),
       email=data.get('email')
   )
  
   # Si el registro fue exitoso, agregar token
   if result.get('recordsets') and len(result['recordsets']) > 0:
       record = result['recordsets'][0]
       if record.get('success'):
           token = generate_token(record['user_id'], data.get('username'))
           record['token'] = token
  
   return result




# ============================================
# RUTA DE LOGIN (SIGN IN)
# ============================================
@auth_bp.route('/login', methods=['POST'])
def login():
   """
   Autentica un usuario existente
  
   @author Jose Alberto Polo Lara
   fn: validate_login
   URL: http://{server}:{port}/api/auth/login
  
   Body (JSON):
   {
       "username": "nombre_usuario",
       "password": "contraseña123"
   }
  
   Returns:
       JSON con el resultado de la validación y token JWT
   """
   data = request.get_json()
  
   # Validar login
   result = user_repository.validate_login(
       username=data.get('username'),
       password=data.get('password')
   )
  
   # Si el login fue exitoso, agregar token
   if result.get('recordsets') and len(result['recordsets']) > 0:
       record = result['recordsets'][0]
       if record.get('is_valid'):
           token = generate_token(record['user_id'], record['username'])
           record['token'] = token
           result_menu = user_repository.catalog_menu(record.get('user_id'))
           record['menu'] = result_menu.get('recordsets', [])
  
   return result




# ============================================
# RUTA DE VERIFICACIÓN (Protegida)
# ============================================
@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify(current_user):
   """
   Verifica si el token del usuario es válido
  
   @author Jose Alberto Polo Lara
   URL: http://{server}:{port}/api/auth/verify
  
   Headers:
       Authorization: Bearer <token>
  
   Returns:
       JSON con la información del usuario
   """
   return jsonify({
       'recordsets': [current_user]
   })




# ============================================
# RUTA DE PERFIL (Ejemplo de ruta protegida)
# ============================================
@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
   """
   Obtiene el perfil del usuario autenticado
  
   @author Jose Alberto Polo Lara
   fn: find_by_id
   URL: http://{server}:{port}/api/auth/profile
  
   Headers:
       Authorization: Bearer <token>
  
   Returns:
       JSON con el perfil completo del usuario
   """
   # Obtener detalles completos del usuario desde la BD
   return user_repository.find_by_id(current_user['user_id'])


