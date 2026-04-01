from .database import db
from datetime import datetime
import json

class Design(db.Model):
    __tablename__ = 'designs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_name = db.Column(db.String(200), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    room_length = db.Column(db.Float, nullable=False)
    room_width = db.Column(db.Float, nullable=False)
    room_height = db.Column(db.Float, nullable=False)
    wall_color = db.Column(db.String(7), default='#FFFFFF')
    floor_color = db.Column(db.String(7), default='#D4A574')
    ceiling_color = db.Column(db.String(7), default='#FFFFFF')
    wall_texture = db.Column(db.String(100))
    floor_texture = db.Column(db.String(100))
    theme = db.Column(db.String(50))
    total_cost = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('DesignItem', backref='design', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_name': self.room_name,
            'room_type': self.room_type,
            'room_length': self.room_length,
            'room_width': self.room_width,
            'room_height': self.room_height,
            'wall_color': self.wall_color,
            'floor_color': self.floor_color,
            'ceiling_color': self.ceiling_color,
            'wall_texture': self.wall_texture,
            'floor_texture': self.floor_texture,
            'theme': self.theme,
            'total_cost': self.total_cost,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class DesignItem(db.Model):
    __tablename__ = 'design_items'
    
    id = db.Column(db.Integer, primary_key=True)
    design_id = db.Column(db.Integer, db.ForeignKey('designs.id'), nullable=False)
    furniture_id = db.Column(db.Integer, nullable=False)
    furniture_name = db.Column(db.String(200), nullable=False)
    furniture_image = db.Column(db.String(500))
    position_x = db.Column(db.Float, default=0)
    position_y = db.Column(db.Float, default=0)
    rotation = db.Column(db.Float, default=0)
    scale_x = db.Column(db.Float, default=1)
    scale_y = db.Column(db.Float, default=1)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'design_id': self.design_id,
            'furniture_id': self.furniture_id,
            'furniture_name': self.furniture_name,
            'furniture_image': self.furniture_image,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'rotation': self.rotation,
            'scale_x': self.scale_x,
            'scale_y': self.scale_y,
            'width': self.width,
            'height': self.height,
            'price': self.price,
            'created_at': self.created_at.isoformat()
        }
