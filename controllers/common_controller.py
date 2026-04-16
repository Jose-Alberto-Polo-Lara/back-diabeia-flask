"""
Common Controller
Controlador para endpoints comunes (catálogos, registros de glucosa)
Traducido desde TypeScript/routing-controllers
"""
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import token_required
from repositories.common_repository import CommonRepository
from services.data_service import DataService
common_bp = Blueprint('common', __name__)
common_repository = CommonRepository()
data_service = DataService()


# ************ SERVICIOS GET ************

@common_bp.route('/getDataMomentToDayDB', methods=['GET'])
@token_required
def get_data_moment_to_day_db(current_user):
    """
    Obtiene el Catálogo del Momento Toma de Muestra de glucosa
    
    @author Jose Alberto Polo Lara
    FN: catalogomomentotomamuestra
    URL: http://{server}:{port}/api/common/getDataMomentToDayDB
    
    Returns:
        JSON con el catálogo de momentos del día
    """
    
        # request.args contiene los query parameters (equivalente a req.query)
    query_params = request.args.to_dict()
        
    return common_repository.get_data_moment_to_day_db(query_params)
        
       ## return jsonify({
       ##     'success': True,
       ##     'data': result['recordsets'],
       ##     'count': len(result['recordsets']) if result['recordsets'] else 0
       # }), 200
        
   

@common_bp.route('/getDataActivityFisicaDB', methods=['GET'])
@token_required
def get_data_activity_fisica_db(current_user):
    """
    Obtiene el Catálogo de la actividad física
    
    @author Jose Alberto Polo Lara
    FN: catalogoactividadfisica
    URL: http://{server}:{port}/api/common/getDataActivityFisicaDB
    
    Returns:
        JSON con el catálogo de actividades físicas
    """
    
    # request.args contiene los query parameters (equivalente a req.query)
    query_params = request.args.to_dict()
        
    return common_repository.get_data_activity_fisica_db(query_params)

@common_bp.route('/getCatalogoSintomas', methods=['GET'])
@token_required
def get_data_sintomas_db(current_user):
    """
    Obtiene el Catálogo de síntomas
    
    @author Jose Alberto Polo Lara
    FN: catalogosintomas
    URL: http://{server}:{port}/api/common/getCatalogoSintomas
    
    Returns:
        JSON con el catálogo de síntomas
    """
    
    # request.args contiene los query parameters (equivalente a req.query)
    query_params = request.args.to_dict()
    array_sintomas = common_repository.get_data_sintomas_db(query_params)
    process_data = data_service.agrupacion_sintomas(array_sintomas)
    return process_data
        

# ************ SERVICIOS POST ************

@common_bp.route('/postInsGlucoseRecord', methods=['POST'])
@token_required
def post_ins_glucose_record(current_user):
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
    
    data = request.get_json()
        # Ejecutar función de inserción
    return common_repository.post_ins_glucose_record(data)
        
       