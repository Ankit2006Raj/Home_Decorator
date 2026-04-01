import os
import sys
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
from config import config
from backend.models import db, init_db, Furniture
from backend.routes import register_routes
from backend.services import FurnitureService

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__, template_folder='frontend', static_folder='frontend/assets')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    init_db(app)
    
    # Register blueprints
    register_routes(app)
    
    # Serve static files
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
    
    @app.route('/assets/<path:path>')
    def send_assets(path):
        return send_from_directory('frontend/assets', path)
    
    @app.route('/images/<path:path>')
    def send_images(path):
        return send_from_directory('frontend/images', path)
    
    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('frontend/css', path)
    
    @app.route('/js/<path:path>')
    def send_js(path):
        return send_from_directory('frontend/js', path)
    
    # Initialize sample data
    with app.app_context():
        db.create_all()
        # Initialize furniture only if not already present
        furniture_count = db.session.query(Furniture).count()
        if furniture_count == 0:
            FurnitureService.init_sample_furniture()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
