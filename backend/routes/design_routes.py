from flask import Blueprint, request, jsonify
from backend.models import db, Design, DesignItem
from backend.services import DesignService

design_routes = Blueprint('designs', __name__, url_prefix='/api/designs')

@design_routes.route('/create', methods=['POST'])
def create_design():
    """Create a new design"""
    try:
        data = request.get_json()
        
        design = DesignService.create_design(
            user_id=data.get('user_id', 1),
            room_name=data.get('room_name'),
            room_type=data.get('room_type'),
            room_length=data.get('room_length'),
            room_width=data.get('room_width'),
            room_height=data.get('room_height')
        )
        
        if not design:
            return {'error': 'Failed to create design'}, 500
        
        return {'success': True, 'design': design.to_dict()}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/<int:design_id>', methods=['GET'])
def get_design(design_id):
    """Get a specific design"""
    try:
        design = Design.query.get(design_id)
        if not design:
            return {'error': 'Design not found'}, 404
        
        return {'success': True, 'design': design.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user_designs(user_id):
    """Get all designs for a user"""
    try:
        designs = DesignService.get_user_designs(user_id)
        return {'success': True, 'designs': [d.to_dict() for d in designs]}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/<int:design_id>/add-item', methods=['POST'])
def add_item_to_design(design_id):
    """Add furniture item to design"""
    try:
        data = request.get_json()
        
        item = DesignService.add_item_to_design(
            design_id=design_id,
            furniture_id=data.get('furniture_id'),
            position_x=data.get('position_x', 0),
            position_y=data.get('position_y', 0),
            rotation=data.get('rotation', 0),
            scale_x=data.get('scale_x', 1),
            scale_y=data.get('scale_y', 1)
        )
        
        if not item:
            return {'error': 'Failed to add item'}, 500
        
        design = Design.query.get(design_id)
        return {'success': True, 'item': item.to_dict(), 'design': design.to_dict()}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/item/<int:item_id>/update', methods=['POST'])
def update_item(item_id):
    """Update furniture item position"""
    try:
        data = request.get_json()
        
        item = DesignService.update_item_position(
            item_id=item_id,
            position_x=data.get('position_x'),
            position_y=data.get('position_y'),
            rotation=data.get('rotation', 0),
            scale_x=data.get('scale_x', 1),
            scale_y=data.get('scale_y', 1)
        )
        
        if not item:
            return {'error': 'Item not found'}, 404
        
        return {'success': True, 'item': item.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/item/<int:item_id>/remove', methods=['POST'])
def remove_item(item_id):
    """Remove furniture item from design"""
    try:
        success = DesignService.remove_item_from_design(item_id)
        
        if not success:
            return {'error': 'Item not found'}, 404
        
        return {'success': True}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/<int:design_id>/update-colors', methods=['POST'])
def update_design_colors(design_id):
    """Update design colors"""
    try:
        data = request.get_json()
        
        design = DesignService.update_design_colors(
            design_id=design_id,
            wall_color=data.get('wall_color'),
            floor_color=data.get('floor_color'),
            ceiling_color=data.get('ceiling_color')
        )
        
        if not design:
            return {'error': 'Design not found'}, 404
        
        return {'success': True, 'design': design.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/<int:design_id>/delete', methods=['POST'])
def delete_design(design_id):
    """Delete a design"""
    try:
        success = DesignService.delete_design(design_id)
        
        if not success:
            return {'error': 'Design not found'}, 404
        
        return {'success': True}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@design_routes.route('/<int:design_id>/export', methods=['GET'])
def export_design(design_id):
    """Export design as JSON"""
    try:
        design = Design.query.get(design_id)
        if not design:
            return {'error': 'Design not found'}, 404
        
        return design.to_dict(), 200
    except Exception as e:
        return {'error': str(e)}, 500
