from flask import Blueprint, request, jsonify
from backend.models import db, Furniture
from backend.services import FurnitureService

furniture_routes = Blueprint('furniture', __name__, url_prefix='/api/furniture')

@furniture_routes.route('/all', methods=['GET'])
def get_all_furniture():
    """Get all furniture items"""
    try:
        furniture = FurnitureService.get_all_furniture()
        return {'success': True, 'furniture': [f.to_dict() for f in furniture]}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/room/<room_type>', methods=['GET'])
def get_furniture_by_room(room_type):
    """Get furniture by room type"""
    try:
        furniture = FurnitureService.get_furniture_by_room(room_type)
        return {'success': True, 'furniture': [f.to_dict() for f in furniture]}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/category/<category>', methods=['GET'])
def get_furniture_by_category(category):
    """Get furniture by category"""
    try:
        furniture = FurnitureService.get_furniture_by_category(category)
        return {'success': True, 'furniture': [f.to_dict() for f in furniture]}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/search', methods=['GET'])
def search_furniture():
    """Search furniture"""
    try:
        query = request.args.get('q', '')
        room_type = request.args.get('room_type', None)
        
        furniture = FurnitureService.search_furniture(query, room_type)
        return {'success': True, 'furniture': [f.to_dict() for f in furniture]}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/<int:furniture_id>', methods=['GET'])
def get_furniture(furniture_id):
    """Get specific furniture item"""
    try:
        furniture = Furniture.query.get(furniture_id)
        if not furniture:
            return {'error': 'Furniture not found'}, 404
        
        return {'success': True, 'furniture': furniture.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/add', methods=['POST'])
def add_furniture():
    """Add custom furniture"""
    try:
        data = request.get_json()
        
        furniture = Furniture(
            name=data.get('name'),
            category=data.get('category'),
            room_type=data.get('room_type'),
            length=data.get('length', 1),
            width=data.get('width', 1),
            height=data.get('height', 1),
            price=data.get('price', 0),
            material=data.get('material'),
            style=data.get('style'),
            color=data.get('color'),
            image_url=data.get('image_url'),
            description=data.get('description'),
            is_custom=True
        )
        db.session.add(furniture)
        db.session.commit()
        
        return {'success': True, 'furniture': furniture.to_dict()}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@furniture_routes.route('/categories', methods=['GET'])
def get_categories():
    """Get all furniture categories"""
    try:
        categories = db.session.query(Furniture.category).distinct().all()
        return {'success': True, 'categories': [c[0] for c in categories]}, 200
    except Exception as e:
        return {'error': str(e)}, 500
