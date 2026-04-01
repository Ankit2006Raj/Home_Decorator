from .database import db
from datetime import datetime

class Furniture(db.Model):
    __tablename__ = 'furniture'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # beds, sofas, chairs, tables, etc.
    room_type = db.Column(db.String(50), nullable=False)  # bedroom, kitchen, hall, office
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    material = db.Column(db.String(100))
    style = db.Column(db.String(100))  # modern, classic, minimal
    color = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    is_custom = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'room_type': self.room_type,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'price': self.price,
            'material': self.material,
            'style': self.style,
            'color': self.color,
            'image_url': self.image_url,
            'description': self.description,
            'is_custom': self.is_custom
        }
