"""
Configuración de base de datos PostgreSQL por entornos
"""
import os

# Configuración de base de datos por entorno
DB_CONFIG = {
    "development": {
        "server": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "12345"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "DiabeIA"),
        "connection_timeout": 180000,
        "request_timeout": 180000
    },
    "qa": {
        "server": os.getenv("DB_HOST_QA", "localhost"),
        "user": os.getenv("DB_USER_QA", "postgres"),
        "password": os.getenv("DB_PASSWORD_QA", ""),
        "port": int(os.getenv("DB_PORT_QA", "5432")),
        "database": os.getenv("DB_NAME_QA", ""),
        "connection_timeout": 180000,
        "request_timeout": 180000
    },
    "production": {
        "server": os.getenv("DB_HOST_PROD", "localhost"),
        "user": os.getenv("DB_USER_PROD", "postgres"),
        "password": os.getenv("DB_PASSWORD_PROD", ""),
        "port": int(os.getenv("DB_PORT_PROD", "5432")),
        "database": os.getenv("DB_NAME_PROD", ""),
        "connection_timeout": 180000,
        "request_timeout": 180000
    },
    "training": {
        "server": os.getenv("DB_HOST_TRAINING", "localhost"),
        "user": os.getenv("DB_USER_TRAINING", "postgres"),
        "password": os.getenv("DB_PASSWORD_TRAINING", ""),
        "port": int(os.getenv("DB_PORT_TRAINING", "5432")),
        "database": os.getenv("DB_NAME_TRAINING", ""),
        "connection_timeout": 180000,
        "request_timeout": 180000
    }
}


def get_db_config(env: str = None) -> dict:
    """
    Obtiene la configuración de base de datos según el entorno.
    
    Args:
        env: Entorno ('development', 'qa', 'production', 'training')
             Si es None, usa la variable FLASK_ENV
    
    Returns:
        Diccionario con la configuración de BD
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    
    config = DB_CONFIG.get(env, DB_CONFIG['development'])
    return config


# Export por defecto para importación simple
default = DB_CONFIG
