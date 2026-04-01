from flask import Blueprint

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')

from .design_routes import design_routes
from .furniture_routes import furniture_routes
from .ai_routes import ai_routes
from .user_routes import user_routes

# Register blueprints
def register_routes(app):
    app.register_blueprint(design_routes)
    app.register_blueprint(furniture_routes)
    app.register_blueprint(ai_routes)
    app.register_blueprint(user_routes)
