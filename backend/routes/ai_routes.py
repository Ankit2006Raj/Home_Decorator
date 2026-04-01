from flask import Blueprint, request, jsonify
from backend.services import GeminiService

ai_routes = Blueprint('ai', __name__, url_prefix='/api/ai')

gemini_service = GeminiService()

@ai_routes.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get AI furniture recommendations"""
    try:
        data = request.get_json()
        
        recommendations = gemini_service.get_furniture_recommendations(
            room_type=data.get('room_type'),
            budget=data.get('budget', 2000),
            style=data.get('style', 'modern')
        )
        
        return {'success': True, 'recommendations': recommendations}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@ai_routes.route('/color-palette', methods=['POST'])
def get_color_palette():
    """Get AI color palette suggestions"""
    try:
        data = request.get_json()
        
        palette = gemini_service.get_color_palette_suggestions(
            style=data.get('style', 'modern'),
            mood=data.get('mood', 'calm')
        )
        
        return {'success': True, 'palette': palette}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@ai_routes.route('/layout-suggestions', methods=['POST'])
def get_layout_suggestions():
    """Get AI layout suggestions"""
    try:
        data = request.get_json()
        
        suggestions = gemini_service.get_layout_suggestions(
            room_type=data.get('room_type'),
            room_width=data.get('room_width'),
            room_length=data.get('room_length'),
            budget=data.get('budget', 2000)
        )
        
        return {'success': True, 'suggestions': suggestions}, 200
    except Exception as e:
        return {'error': str(e)}, 500
