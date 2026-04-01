from flask import Blueprint, request, jsonify
from backend.models import db, User

user_routes = Blueprint('users', __name__, url_prefix='/api/users')

@user_routes.route('/create', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return {'error': 'User already exists'}, 400
        
        user = User(
            username=data.get('username'),
            email=data.get('email')
        )
        db.session.add(user)
        db.session.commit()
        
        return {'success': True, 'user': user.to_dict()}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@user_routes.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {'success': True, 'user': user.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@user_routes.route('', methods=['GET'])
def get_or_create_default_user():
    """Get or create default user"""
    try:
        user = User.query.first()
        if not user:
            user = User(username='default', email='default@homedecorator.local')
            db.session.add(user)
            db.session.commit()
        
        return {'success': True, 'user': user.to_dict()}, 200
    except Exception as e:
        return {'error': str(e)}, 500
