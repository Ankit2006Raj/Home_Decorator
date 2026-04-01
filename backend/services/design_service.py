from backend.models import db, Design, DesignItem, Furniture
from datetime import datetime

class DesignService:
    @staticmethod
    def create_design(user_id, room_name, room_type, room_length, room_width, room_height):
        """Create a new design"""
        try:
            design = Design(
                user_id=user_id,
                room_name=room_name,
                room_type=room_type,
                room_length=room_length,
                room_width=room_width,
                room_height=room_height
            )
            db.session.add(design)
            db.session.commit()
            return design
        except Exception as e:
            print(f"Error creating design: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def add_item_to_design(design_id, furniture_id, position_x, position_y, rotation=0, scale_x=1, scale_y=1):
        """Add furniture item to design"""
        try:
            furniture = Furniture.query.get(furniture_id)
            if not furniture:
                return None
            
            item = DesignItem(
                design_id=design_id,
                furniture_id=furniture_id,
                furniture_name=furniture.name,
                furniture_image=furniture.image_url,
                position_x=position_x,
                position_y=position_y,
                rotation=rotation,
                scale_x=scale_x,
                scale_y=scale_y,
                width=furniture.width,
                height=furniture.height,
                price=furniture.price
            )
            db.session.add(item)
            
            # Update design total cost
            design = Design.query.get(design_id)
            design.total_cost = sum(i.price for i in design.items) + furniture.price
            design.updated_at = datetime.utcnow()
            
            db.session.commit()
            return item
        except Exception as e:
            print(f"Error adding item to design: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def update_item_position(item_id, position_x, position_y, rotation, scale_x, scale_y):
        """Update furniture item position and rotation"""
        try:
            item = DesignItem.query.get(item_id)
            if not item:
                return None
            
            item.position_x = position_x
            item.position_y = position_y
            item.rotation = rotation
            item.scale_x = scale_x
            item.scale_y = scale_y
            
            design = item.design
            design.updated_at = datetime.utcnow()
            
            db.session.commit()
            return item
        except Exception as e:
            print(f"Error updating item position: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def remove_item_from_design(item_id):
        """Remove furniture item from design"""
        try:
            item = DesignItem.query.get(item_id)
            if not item:
                return False
            
            design = item.design
            db.session.delete(item)
            
            # Update design total cost
            design.total_cost = sum(i.price for i in design.items if i.id != item_id)
            design.updated_at = datetime.utcnow()
            
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error removing item from design: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def update_design_colors(design_id, wall_color, floor_color, ceiling_color):
        """Update design colors"""
        try:
            design = Design.query.get(design_id)
            if not design:
                return None
            
            design.wall_color = wall_color
            design.floor_color = floor_color
            design.ceiling_color = ceiling_color
            design.updated_at = datetime.utcnow()
            
            db.session.commit()
            return design
        except Exception as e:
            print(f"Error updating design colors: {e}")
            db.session.rollback()
            return None
    
    @staticmethod
    def get_user_designs(user_id):
        """Get all designs for a user"""
        return Design.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def delete_design(design_id):
        """Delete a design"""
        try:
            design = Design.query.get(design_id)
            if not design:
                return False
            
            db.session.delete(design)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting design: {e}")
            db.session.rollback()
            return False
