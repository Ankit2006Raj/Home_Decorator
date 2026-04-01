from .database import db

class Theme(db.Model):
    __tablename__ = 'themes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    style = db.Column(db.String(50), nullable=False)  # modern, classic, minimal
    primary_color = db.Column(db.String(7), nullable=False)
    secondary_color = db.Column(db.String(7), nullable=False)
    accent_color = db.Column(db.String(7), nullable=False)
    wall_texture = db.Column(db.String(100))
    floor_texture = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'style': self.style,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'accent_color': self.accent_color,
            'wall_texture': self.wall_texture,
            'floor_texture': self.floor_texture,
            'description': self.description
        }
