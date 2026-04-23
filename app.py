import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
from config import config
from backend.models import db, init_db, Furniture
from backend.routes import register_routes
from backend.services import FurnitureService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config_name='development'):
    """Application factory with improved static file handling"""
    app = Flask(__name__, template_folder='frontend', static_folder='frontend/assets', static_url_path='/assets')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    init_db(app)
    
    logger.info(f"Creating app with config: {config_name}")
    
    # Register blueprints
    register_routes(app)
    
    # Serve HTML pages
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/editor')
    def editor():
        return render_template('editor.html')
    
    @app.route('/admin')
    def admin():
        return render_template('admin.html')
    
    @app.route('/3d-view')
    def three_d_view():
        return render_template('3d-view.html')
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'environment': os.getenv('FLASK_ENV', 'development')
        }), 200
    
    # API status endpoint
    @app.route('/api/status', methods=['GET'])
    def api_status():
        """API status endpoint"""
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            db_status = 'connected'
        except Exception as e:
            logger.warning(f"Database connection check failed: {str(e)}")
            db_status = 'disconnected'
        
        return jsonify({
            'api': 'online',
            'database': db_status,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    # Serve CSS files with proper mime type
    @app.route('/css/<path:path>')
    def send_css(path):
        try:
            return send_from_directory('frontend/css', path, mimetype='text/css')
        except Exception as e:
            logger.error(f"Error serving CSS {path}: {str(e)}")
            return jsonify({'error': 'CSS file not found'}), 404
    
    # Serve JavaScript files
    @app.route('/js/<path:path>')
    def send_js(path):
        try:
            return send_from_directory('frontend/js', path, mimetype='text/javascript')
        except Exception as e:
            logger.error(f"Error serving JS {path}: {str(e)}")
            return jsonify({'error': 'JS file not found'}), 404
    
    # Serve images
    @app.route('/images/<path:path>')
    def send_images(path):
        try:
            return send_from_directory('frontend/images', path)
        except Exception as e:
            logger.error(f"Error serving image {path}: {str(e)}")
            return jsonify({'error': 'Image not found'}), 404
    
    # Serve assets
    @app.route('/assets/<path:path>')
    def send_assets(path):
        try:
            return send_from_directory('frontend/assets', path)
        except Exception as e:
            logger.error(f"Error serving asset {path}: {str(e)}")
            return jsonify({'error': 'Asset not found'}), 404
    
    # Initialize database and sample data
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Initialize furniture only if not already present
            furniture_count = db.session.query(Furniture).count()
            if furniture_count == 0:
                logger.info("Initializing sample furniture...")
                FurnitureService.init_sample_furniture()
                logger.info("Sample furniture initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}", exc_info=True)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 Error: {error}")
        return jsonify({'error': 'Resource not found', 'status': 404}), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Error: {error}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'status': 500}), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        logger.warning(f"403 Error: {error}")
        return jsonify({'error': 'Forbidden', 'status': 403}), 403
    
    @app.after_request
    def after_request(response):
        """Add headers to prevent caching of HTML files"""
        if response.content_type and 'html' in response.content_type:
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    
    logger.info(f"Application created successfully")
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    logger.info(f"Starting server on 0.0.0.0:{port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)

