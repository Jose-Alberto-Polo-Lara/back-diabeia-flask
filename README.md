# Framework Flask - Arquitectura MVC

Framework Flask profesional con arquitectura en capas: Controller, Repository y Data Layer para PostgreSQL.

## 📁 Estructura del Proyecto

```
flask/
├── app.py                          # Archivo principal (Index) - Carga todos los módulos
├── config.py                       # Configuración de la aplicación por entornos
├── example_data_usage.py          # Ejemplos de uso de la capa de datos
├── requirements.txt               # Dependencias Python
├── .env.example                   # Plantilla de variables de entorno
├── .gitignore                     # Archivos ignorados por git
│
├── controllers/                   # 🎮 Capa de presentación
│   ├── __init__.py
│   ├── user_controller.py        # Controlador CRUD de usuarios
│   └── product_controller.py     # Controlador CRUD de productos
│
├── repositories/                  # 📦 Capa de lógica de negocio
│   ├── __init__.py
│   ├── user_repository.py        # Repository de usuarios
│   └── product_repository.py     # Repository de productos
│
└── database/                      # 🗄️ Capa de acceso a datos
    ├── __init__.py
    ├── data.py                    # Clase Query para PostgreSQL
    └── config_db.py               # Configuración BD por entornos
```

## 🏗️ Arquitectura

### Capas del Framework:

1. **app.py (Index)**: Archivo principal que carga y registra todos los módulos/blueprints
2. **Controllers**: Manejan peticiones HTTP, validaciones de entrada y respuestas JSON
3. **Repositories**: Lógica de negocio y procesamiento de datos
4. **Database**: Capa de acceso a PostgreSQL con pool de conexiones y ejecución de funciones/queries

## 📋 Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- Virtualenv (recomendado)

## 🚀 Instalación

### Paso 1: Clonar o descargar el proyecto

```bash
cd /ruta/donde/quieres/el/proyecto
# Si usas git:
git clone <url-del-repositorio>
cd flask
pip install -r requirements.txt
python app.py
```

### PaAPI Endpoints

### General
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información del API |
| GET | `/health` | Estado de salud del servicio |

### Usuarios (`/api/users`)
| Método | Endpoint | Descripción | Body |
|--------|----------|-------------|------|
| GET | `/api/users` | Listar todos los usuarios | - |
| GET | `/api/users/<id>` | Obtener usuario por ID | - |
| POST | `/api/users` | Crear nuevo usuario | `{"name": "...", "email": "..."}` |
| PUT | `/api/users/<id>` | Actualizar usuario | `{"name": "...", "email": "..."}` |
| DELETE | `/api/users/<id>` | Eliminar usuario | - |

### Productos (`/api/products`)
| Método | Endpoint | Descripción | Body |
|--------|----------|-------------|------|
| GET | `/api/products` | Listar todos los productos | - |
| GET | `/api/products/<id>` | Obtener producto por ID | - |
| POST | `/api/products` | Crear nuevo producto | `{"name": "...", "price": 99.99, ...}` |
| PUT | `/api/products/<id>` | Actualizar producto | `{"name": "...", "price": 99.99, ...}` |
| DELETE | `/api/products/<id>` | Eliminar producto | - |

## 📝 Ejemplos de Uso con cURL

### Listar usuarios
```bash
curl http://localhost:5000/api/users
```

### Obtener usuario específico
```bash
curl http://localhost:5000/api/users/1
```

### Crear usuario
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos López",
    "email": "carlos@example.com"
  }'
```

### Actualizar usuario
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos López Actualizado",
    "email": "carlos.nuevo@example.com"
  }'
```

### Eliminar usuario
```bash
curl -X DELETE http://localhost:5000/api/users/1
```

### Crear producto
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teclado Mecánico",
    "description": "Teclado RGB gaming",
    "price": 89.99,
    "stock": 20
  }'
```

### Listar productos
```bash
curl http://localhost:5000/api/products
psql -U postgres

# Crear base de datos
CREATE DATABASE DiabeIA;

# Crear usuario (opcional)
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE DiabeIA TO myuser;

# Salir
\q
```

#### B. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tu editor favorito
nano .env
# o
vim .env
# o
code .env
```

**Configurar en `.env`:**
```bash
# Configuración de la aplicación
SECRET_KEY=tu-clave-secreta-aqui-cambiar-en-produccion
DATABASE_URI=sqlite:///app.db

# PostgreSQL - Development
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=12345
DB_NAME=DiabeIA
DB_PORT=5432

# Entorno
FLASK_ENV=development
```

### Paso 5: Verificar configuración (opcional)

```bash
# Probar conexión a PostgreSQL
python -c "from database import Query; q = Query(); print('✓ Conexión exitosa')"
```

## ▶️ Ejecución

### Modo Development (con debug)

```bash
python app.py
```

La aplicación estará disponible en:
- **URL**: `http://localhost:5000`
- **Health check**: `http://localhost:5000/health`

### Modo Production

```bash
# Cambiar entorno
export FLASK_ENV=production  # macOS/Linux
set FLASK_ENV=production     # Windows

# Usar servidor WSGI como Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Probar la Aplicación

### 1. Verificar que está corriendo

```bash
curl http://localhost:5000/
```

Respuesta esperada:
```json
{
  "message": "Framework Flask - API REST",
  "version": "1.0.0",
  "endpoints": {
    "users": "/api/users",
    "products": "/api/products"
  }
}
```

### 2. Health check Avanzada

### Entornos disponibles

El framework soporta múltiples entornos configurables en `config.py`:

```python
# Development (por defecto)
FLASK_ENV=development

# QA/Testing
FLASK_ENV=qa

# Production
FLASK_ENV=production

# Training
FLASK_ENV=training
```

### Configuración de base de datos

Edita `database/config_db.py` para personalizar la configuración por entorno:

```python
DB_CONFIG = {
    "development": {
        "server": "localhost",
        "user": "postgres",
        "password": "12345",
        "database": "DiabeIA",
        ...
    },
    "production": {
        "server": "prod-server.example.com",
        "user": "prod_user",
        ...
    }
}
```

### Variables de entorno

Todas las configuraciones pueden sobrescribirse con variables de entorno en `.env`:

```bash
# Base de datos
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=tu-password
DB_NAME=DiabeIA
DB_PORT=5432

# Aplicación
SECRET_KEY=clave-secreta-super-segura
FLASK_ENV=development
```

## 🗄️ Uso de la Capa de Datos

### Ejecutar funciones de PostgreSQL

```python
from database import Query

query = Query()

# Ejecutar función: SELECT * FROM get_user_by_id(1)
result = query.sp_execute({'id': 1}, 'get_user_by_id')
users = result['recordsets']
```

### Ejecutar SQL directo

```python
from database import Query

query = Query()

# SQL con placeholders %s
result = query.sp_execute(
    {'name': 'Juan'},
    'SELECT * FROM users WHERE name = %s'
)
```

### Función helper rápida

```python
from database import execute_query

result = execute_query({'status': 'active'}, 'get_active_users')
users = result['recordsets']
```

Ver más ejemplos en `example_data_usage.py`.

## 📦 Agregar Nuevos Módulos

### 1. Crear Controller

Crea `controllers/mi_controller.py`:

```python
from flask import Blueprint, request, jsonify
from repositories.mi_repository import MiRepository

mi_bp = Blueprint('mi_modulo', __name__)
mi_repository = MiRepository()

@mi_bp.route('/', methods=['GET'])
def get_all():
    items = mi_repository.get_all()
    return jsonify({'success': True, 'data': items}), 200
```

### 2. Crear Repository

Crea `repositories/mi_repository.py`:

```python
from database import Query

class MiRepository:
    def __init__(self):
        self.query = Query()
    
    def get_all(self):
        result = self.query.sp_execute({}, 'get_all_items')
        return result['recordsets']
```

### 3. Registrar en app.py

```python
from controllers.mi_controller import mi_bp

app.register_blueprint(mi_bp, url_prefix='/api/mi-ruta')
```

## 🎯 Características

- ✅ Arquitectura limpia en 3 capas (Controller → Repository → Data)
- ✅ Pool de conexiones PostgreSQL reutilizable
- ✅ Ejecución automática de funciones SQL
- ✅ Patrón Repository para lógica de negocio
- ✅ Configuración multi-entorno (dev/qa/prod/training)
- ✅ API RESTful con respuestas JSON estandarizadas
- ✅ Manejo estructurado de errores
- ✅ Variables de entorno con `.env`
- ✅ Factory pattern para la app Flask

## 🐛 Solución de Problemas

### Error: "No module named 'psycopg2'"
```bash
pip install psycopg2-binary
```

### Error: "Connection refused" a PostgreSQL
- Verifica que PostgreSQL esté corriendo: `pg_ctl status`
- Verifica host y puerto en `.env`
- En macOS: `brew services start postgresql`

### Error: "ModuleNotFoundError: No module named 'database'"
- Asegúrate de estar en el directorio del proyecto
- Verifica que existe `database/__init__.py`

### Puerto 5000 en uso
```bash
# Cambiar puerto en app.py
app.run(debug=True, host='0.0.0.0', port=8000)
```

## 📚 Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Requestts/<id>` - Eliminar un producto

## 📝 Ejemplos de Uso

### Crear un usuario:
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos López", "email": "carlos@example.com"}'
```

### Crear un producto:
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Teclado", "description": "Teclado mecánico", "price": 89.99, "stock": 20}'
```

## 🔧 Configuración

Edita `config.py` para ajustar la configuración según el entorno:
- `DevelopmentConfig`: Para desarrollo
- `ProductionConfig`: Para producción
- `TestingConfig`: Para pruebas

## 📦 Agregar Nuevos Módulos

1. Crea un nuevo controller en `controllers/`
2. Crea un nuevo repository en `repositories/`
3. Registra el blueprint en `app.py`:

```python
from controllers.tu_controller import tu_bp
app.register_blueprint(tu_bp, url_prefix='/api/tu-ruta')
```

## 🎯 Características

- ✅ Arquitectura limpia con separación de responsabilidades
- ✅ Patrón Repository para lógica de datos
- ✅ Controllers para manejo de rutas
- ✅ Configuración por entornos
- ✅ API RESTful
- ✅ Respuestas JSON estructuradas
- ✅ Manejo de errores

## 📄 Licencia

MIT
