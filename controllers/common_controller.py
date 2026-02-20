"""
Common Controller
Controlador para endpoints comunes (catálogos, registros de glucosa)
Traducido desde TypeScript/routing-controllers
"""
from flask import Blueprint, request, jsonify
from repositories.common_repository import CommonRepository

common_bp = Blueprint('common', __name__)
common_repository = CommonRepository()


# ************ SERVICIOS GET ************

@common_bp.route('/getDataMomentToDayDB', methods=['GET'])
def get_data_moment_to_day_db():
    """
    Obtiene el Catálogo del Momento Toma de Muestra de glucosa
    
    @author Jose Alberto Polo Lara
    FN: catalogomomentotomamuestra
    URL: http://{server}:{port}/api/common/getDataMomentToDayDB
    
    Returns:
        JSON con el catálogo de momentos del día
    """
    try:
        # request.args contiene los query parameters (equivalente a req.query)
        query_params = request.args.to_dict()
        
        result = common_repository.get_data_moment_to_day_db(query_params)
        
        return jsonify({
            'success': True,
            'data': result['recordsets'],
            'count': len(result['recordsets']) if result['recordsets'] else 0
        }), 200
        
    except Exception as e:
        error_data = e if isinstance(e, dict) else {'error': str(e)}
        return jsonify({
            'success': False,
            'error': str(error_data.get('error', e))
        }), 500


@common_bp.route('/getDataActivityFisicaDB', methods=['GET'])
def get_data_activity_fisica_db():
    """
    Obtiene el Catálogo de la actividad física
    
    @author Jose Alberto Polo Lara
    FN: catalogoactividadfisica
    URL: http://{server}:{port}/api/common/getDataActivityFisicaDB
    
    Returns:
        JSON con el catálogo de actividades físicas
    """
    try:
        # request.args contiene los query parameters (equivalente a req.query)
        query_params = request.args.to_dict()
        
        result = common_repository.get_data_activity_fisica_db(query_params)
        
        return jsonify({
            'success': True,
            'data': result['recordsets'],
            'count': len(result['recordsets']) if result['recordsets'] else 0
        }), 200
        
    except Exception as e:
        error_data = e if isinstance(e, dict) else {'error': str(e)}
        return jsonify({
            'success': False,
            'error': str(error_data.get('error', e))
        }), 500


# ************ SERVICIOS POST ************

@common_bp.route('/postInsGlucoseRecord', methods=['POST'])
def post_ins_glucose_record():
    """
    Registra un nuevo registro de glucosa
    
    @author José Alberto Polo Lara
    fn: ins_glucose_record
    URL: http://{server}:{port}/api/common/postInsGlucoseRecord
    
    Body (JSON):
    {
        "user_id": 1,
        "glucose_value": 120,
        "moment_id": 2,
        "date": "2024-02-19",
        "notes": "Después del desayuno"
    }
    
    Returns:
        JSON con el resultado de la inserción
    """
    try:
        # request.get_json() obtiene el body (equivalente a @Body() en routing-controllers)
        data = request.get_json()
        
        # Validación básica
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se recibieron datos en el body'
            }), 400
        
        # Ejecutar función de inserción
        result = common_repository.post_ins_glucose_record(data)
        
        return jsonify({
            'success': True,
            'data': result['recordsets'],
            'message': 'Registro de glucosa creado exitosamente'
        }), 201
        
    except Exception as e:
        error_data = e if isinstance(e, dict) else {'error': str(e)}
        return jsonify({
            'success': False,
            'error': str(error_data.get('error', e))
        }), 500

