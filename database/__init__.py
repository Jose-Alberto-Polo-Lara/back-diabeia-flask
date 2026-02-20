"""
Database package
Contiene la capa de acceso a datos y utilidades de base de datos
"""
from .data import Query, execute_query
from .config_db import DB_CONFIG, get_db_config

__all__ = ['Query', 'execute_query', 'DB_CONFIG', 'get_db_config']
