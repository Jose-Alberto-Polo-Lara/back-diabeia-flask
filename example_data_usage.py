"""
Ejemplos de uso de la clase Query para PostgreSQL
"""
from database.data import Query, execute_query


def ejemplo_1_funcion_simple():
    """Ejemplo 1: Ejecutar una función de PostgreSQL por nombre"""
    query = Query()
    
    # Si tienes una función en PostgreSQL: get_user_by_id(user_id INT)
    result = query.sp_execute(
        params={'user_id': 1},
        sp='get_user_by_id'
    )
    
    if result['recordsets']:
        users = result['recordsets']
        print("Usuarios encontrados:", users)


def ejemplo_2_sql_directo():
    """Ejemplo 2: Ejecutar SQL directo con parámetros"""
    query = Query()
    
    result = query.sp_execute(
        params={'name': 'Juan'},
        sp='SELECT * FROM users WHERE name = %s'
    )
    
    users = result['recordsets']
    print("Usuarios:", users)


def ejemplo_3_multiples_parametros():
    """Ejemplo 3: Función con múltiples parámetros"""
    query = Query()
    
    # Función PostgreSQL: create_user(p_name VARCHAR, p_email VARCHAR)
    result = query.sp_execute(
        params={
            'name': 'Carlos López',
            'email': 'carlos@example.com'
        },
        sp='create_user'
    )
    
    print("Usuario creado:", result['recordsets'])


def ejemplo_4_con_callback():
    """Ejemplo 4: Usando callback"""
    query = Query()
    
    def handle_result(result):
        if 'error' in result and result['error']:
            print("Error:", result['error'])
        else:
            print("Datos:", result['recordsets'])
    
    query.sp_execute_param(
        params={'id': 1},
        sp='get_product_by_id',
        cb=handle_result
    )


def ejemplo_5_context_manager():
    """Ejemplo 5: Usando context manager (auto-cierre)"""
    with Query() as query:
        result = query.sp_execute(
            params={'category': 'Electronics'},
            sp='SELECT * FROM products WHERE category = %s'
        )
        print("Productos:", result['recordsets'])
    # Pool se cierra automáticamente al salir del contexto


def ejemplo_6_funcion_helper():
    """Ejemplo 6: Usando la función helper execute_query"""
    result = execute_query(
        params={'status': 'active'},
        sp='get_active_users'
    )
    
    active_users = result['recordsets']
    print("Usuarios activos:", active_users)


def ejemplo_7_insert_update():
    """Ejemplo 7: INSERT/UPDATE con SQL directo"""
    query = Query()
    
    # INSERT
    result = query.sp_execute(
        params={'name': 'Nuevo Producto', 'price': 99.99},
        sp='INSERT INTO products (name, price) VALUES (%s, %s) RETURNING *'
    )
    print("Producto insertado:", result['recordsets'])
    
    # UPDATE
    result = query.sp_execute(
        params={'price': 89.99, 'id': 1},
        sp='UPDATE products SET price = %s WHERE id = %s RETURNING *'
    )
    print("Producto actualizado:", result['recordsets'])


def ejemplo_8_manejo_errores():
    """Ejemplo 8: Manejo de errores"""
    query = Query()
    
    try:
        result = query.sp_execute(
            params={'id': 999},
            sp='get_user_by_id'
        )
        
        if result['recordsets']:
            print("Usuario encontrado")
        else:
            print("Usuario no encontrado")
            
    except Exception as e:
        if isinstance(e, dict):
            print("Error de BD:", e.get('error'))
        else:
            print("Error:", str(e))


if __name__ == '__main__':
    print("Ejemplos de uso de Query para PostgreSQL")
    print("=" * 50)
    
    # Descomentar el ejemplo que quieras probar
    # ejemplo_1_funcion_simple()
    # ejemplo_2_sql_directo()
    # ejemplo_3_multiples_parametros()
    # ejemplo_4_con_callback()
    # ejemplo_5_context_manager()
    # ejemplo_6_funcion_helper()
    # ejemplo_7_insert_update()
    # ejemplo_8_manejo_errores()
