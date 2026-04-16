"""
Middleware de autenticación JWT
Este módulo maneja la autenticación basada en tokens JWT
"""
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def generate_token(user_id, username):
   """
   Genera un token JWT para un usuario autenticado
  
   PASO A PASO:
   1. Toma el user_id y username del usuario
   2. Crea un payload (carga útil) con información del usuario
   3. Agrega tiempo de expiración al token
   4. Firma el token con la clave secreta
  
   Args:
       user_id (int): ID del usuario en la base de datos
       username (str): Nombre de usuario
  
   Returns:
       str: Token JWT codificado
   """
   try:
       # Obtener configuración de forma segura
       expiration_hours = current_app.config.get('JWT_EXPIRATION_HOURS', 0.25)
       secret_key = current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
       algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
      
       # PASO 1: Crear el payload con la información del usuario
       payload = {
           'user_id': user_id,
           'username': username,
           'iat': datetime.utcnow(),  # Issued At (cuándo se creó)
           'exp': datetime.utcnow() + timedelta(hours=expiration_hours)  # Expiration time (cuándo expira)
       }
      
       # PASO 2: Codificar el token usando la clave secreta
       token = jwt.encode(
           payload,
           secret_key,
           algorithm=algorithm
       )
      
       return token
  
   except Exception as e:
       raise Exception(f"Error generando token: {str(e)}")




def verify_token(token):
   """
   Verifica y decodifica un token JWT
  
   PASO A PASO:
   1. Intenta decodificar el token con la clave secreta
   2. Verifica que no haya expirado
   3. Retorna la información del usuario
  
   Args:
       token (str): Token JWT a verificar
  
   Returns:
       dict: Información del usuario si el token es válido
       None: Si el token es inválido o expiró
   """
   try:
       # Obtener configuración de forma segura
       secret_key = current_app.config.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
       algorithm = current_app.config.get('JWT_ALGORITHM', 'HS256')
      
       # PASO 1: Decodificar el token
       payload = jwt.decode(
           token,
           secret_key,
           algorithms=[algorithm]
       )
      
       # PASO 2: Si llegamos aquí, el token es válido
       return payload
  
   except jwt.ExpiredSignatureError:
       # El token expiró
       return None
  
   except jwt.InvalidTokenError:
       # El token es inválido
       return None
  
   except Exception as e:
       # Cualquier otro error
       return None




def token_required(f):
   """
   Decorador que protege rutas que requieren autenticación
  
   PASO A PASO:
   1. Extrae el token del header 'Authorization'
   2. Verifica que el token sea válido
   3. Si es válido, permite acceso a la ruta
   4. Si no es válido, retorna error 401 (No autorizado)
  
   Uso:
       @app.route('/ruta-protegida')
       @token_required
       def ruta_protegida(current_user):
           return {'message': f'Hola {current_user["username"]}'}
   """
   @wraps(f)
   def decorated(*args, **kwargs):
       token = None
      
       # PASO 1: Extraer el token del header Authorization
       if 'Authorization' in request.headers:
           # El header debe ser: "Bearer <token>"
           auth_header = request.headers['Authorization']
           try:
               # Separar "Bearer" del token
               token = auth_header.split(" ")[1]
           except IndexError:
               return jsonify({
                   'error': 'Formato de token inválido. Use: Bearer <token>',
                   'recordsets': []
               }), 401
      
       # PASO 2: Si no hay token, denegar acceso
       if not token:
           return jsonify({
               'error': 'Token de autenticación requerido',
               'recordsets': []
           }), 401
      
       # PASO 3: Verificar el token
       current_user = verify_token(token)
      
       # PASO 4: Si el token no es válido, denegar acceso
       if current_user is None:
           return jsonify({
               'error': 'Token inválido o expirado',
               'recordsets': []
           }), 401
      
       # PASO 5: Si todo está bien, ejecutar la función protegida
       # NO capturamos errores aquí - dejamos que se propaguen normalmente
       return f(current_user, *args, **kwargs)
  
   return decorated