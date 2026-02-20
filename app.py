"""
Archivo principal - Index
Aquí se cargan y registran todos los módulos del framework
"""
from flask import Flask
from config import Config
from controllers.common_controller import common_bp

def create_app(config_class=Config):
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Registrar blueprints (módulos)
    app.register_blueprint(common_bp, url_prefix='/v0/common')
    
    @app.route('/')
    def index():
        return {
            'message': 'Framework Flask - API REST',
            'version': '0.1.0',
            'api_version': 'v0',
            'endpoints': {
                'common': '/v0/common'
            }
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'version': 'v0'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
