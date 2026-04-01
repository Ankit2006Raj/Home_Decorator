from .database import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)  # bedroom, kitchen, hall, office
    length = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'room_type': self.room_type,
            'length': self.length,
            'width': self.width,
            'height': self.height,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
