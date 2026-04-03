from backend.models import db, Furniture
import logging

logger = logging.getLogger(__name__)

SAMPLE_FURNITURE = [
    # Bedrooms
    {'name': 'Queen Bed', 'category': 'Beds', 'room_type': 'bedroom', 'length': 5, 'width': 3, 'height': 2.5, 'price': 599, 'material': 'Wood', 'style': 'modern', 'color': 'Brown'},
    {'name': 'Wooden Wardrobe', 'category': 'Wardrobes', 'room_type': 'bedroom', 'length': 2, 'width': 0.6, 'height': 6, 'price': 899, 'material': 'Wood', 'style': 'classic', 'color': 'Dark Brown'},
    {'name': 'Bedside Table', 'category': 'Tables', 'room_type': 'bedroom', 'length': 0.6, 'width': 0.5, 'height': 1.5, 'price': 149, 'material': 'Wood', 'style': 'modern', 'color': 'Natural'},
    {'name': 'Desk Lamp', 'category': 'Lighting', 'room_type': 'bedroom', 'length': 0.3, 'width': 0.3, 'height': 1.5, 'price': 49, 'material': 'Metal', 'style': 'minimal', 'color': 'Black'},
    
    # Kitchens
    {'name': 'Kitchen Island', 'category': 'Tables', 'room_type': 'kitchen', 'length': 1.5, 'width': 0.9, 'height': 0.9, 'price': 799, 'material': 'Wood', 'style': 'modern', 'color': 'White'},
    {'name': 'Dining Table', 'category': 'Tables', 'room_type': 'kitchen', 'length': 1.8, 'width': 1, 'height': 0.75, 'price': 499, 'material': 'Wood', 'style': 'modern', 'color': 'Oak'},
    {'name': 'Kitchen Cabinet', 'category': 'Cabinets', 'room_type': 'kitchen', 'length': 0.6, 'width': 0.6, 'height': 2.2, 'price': 349, 'material': 'Wood', 'style': 'modern', 'color': 'White'},
    {'name': 'Pendant Light', 'category': 'Lighting', 'room_type': 'kitchen', 'length': 0.4, 'width': 0.4, 'height': 1, 'price': 79, 'material': 'Metal', 'style': 'modern', 'color': 'Chrome'},
    
    # Living Room / Hall
    {'name': 'L-Shaped Sofa', 'category': 'Sofas', 'room_type': 'hall', 'length': 3, 'width': 1.5, 'height': 0.85, 'price': 1299, 'material': 'Fabric', 'style': 'modern', 'color': 'Gray'},
    {'name': '3-Seater Sofa', 'category': 'Sofas', 'room_type': 'hall', 'length': 2.5, 'width': 1, 'height': 0.85, 'price': 799, 'material': 'Fabric', 'style': 'modern', 'color': 'Beige'},
    {'name': 'Coffee Table', 'category': 'Tables', 'room_type': 'hall', 'length': 1.2, 'width': 0.8, 'height': 0.45, 'price': 299, 'material': 'Glass', 'style': 'modern', 'color': 'Clear'},
    {'name': 'Reclining Chair', 'category': 'Chairs', 'room_type': 'hall', 'length': 0.9, 'width': 1, 'height': 0.95, 'price': 449, 'material': 'Leather', 'style': 'modern', 'color': 'Black'},
    {'name': 'Ceiling Light', 'category': 'Lighting', 'room_type': 'hall', 'length': 0.4, 'width': 0.4, 'height': 0.5, 'price': 129, 'material': 'Metal', 'style': 'modern', 'color': 'Gold'},
    {'name': 'Area Rug', 'category': 'Carpets', 'room_type': 'hall', 'length': 2.5, 'width': 1.8, 'height': 0.05, 'price': 199, 'material': 'Wool', 'style': 'modern', 'color': 'Gray'},
    
    # Office
    {'name': 'Executive Desk', 'category': 'Tables', 'room_type': 'office', 'length': 1.6, 'width': 0.8, 'height': 0.75, 'price': 599, 'material': 'Wood', 'style': 'classic', 'color': 'Dark Brown'},
    {'name': 'Office Chair', 'category': 'Chairs', 'room_type': 'office', 'length': 0.7, 'width': 0.7, 'height': 0.9, 'price': 399, 'material': 'Mesh', 'style': 'modern', 'color': 'Black'},
    {'name': 'Bookshelf', 'category': 'Cabinets', 'room_type': 'office', 'length': 0.9, 'width': 0.35, 'height': 2.2, 'price': 299, 'material': 'Wood', 'style': 'modern', 'color': 'Light Oak'},
    {'name': 'Desk Lamp', 'category': 'Lighting', 'room_type': 'office', 'length': 0.3, 'width': 0.3, 'height': 1.5, 'price': 69, 'material': 'Metal', 'style': 'modern', 'color': 'Silver'},
]

class FurnitureService:
    @staticmethod
    def init_sample_furniture():
        """Initialize database with sample furniture"""
        try:
            # Check if furniture already exists
            if Furniture.query.first():
                return True
            
            for item in SAMPLE_FURNITURE:
                furniture = Furniture(
                    name=item['name'],
                    category=item['category'],
                    room_type=item['room_type'],
                    length=item['length'],
                    width=item['width'],
                    height=item['height'],
                    price=item['price'],
                    material=item['material'],
                    style=item['style'],
                    color=item['color'],
                    image_url=f"/images/furniture/{item['name'].lower().replace(' ', '-')}.png",
                    description=f"{item['material']} {item['name']} in {item['style']} style",
                    is_custom=False
                )
                db.session.add(furniture)
            
            db.session.commit()
            logger.info(f"Initialized {len(SAMPLE_FURNITURE)} sample furniture items")
            return True
        except Exception as e:
            logger.error(f"Error initializing sample furniture: {str(e)}", exc_info=True)
            db.session.rollback()
            return False
    
    @staticmethod
    def get_furniture_by_room(room_type):
        """Get all furniture for a specific room type"""
        return Furniture.query.filter_by(room_type=room_type).all()
    
    @staticmethod
    def get_furniture_by_category(category):
        """Get furniture by category"""
        return Furniture.query.filter_by(category=category).all()
    
    @staticmethod
    def get_all_furniture():
        """Get all furniture items"""
        return Furniture.query.all()
    
    @staticmethod
    def search_furniture(query, room_type=None):
        """Search furniture by name or category"""
        base_query = Furniture.query.filter(
            db.or_(
                Furniture.name.ilike(f'%{query}%'),
                Furniture.category.ilike(f'%{query}%')
            )
        )
        
        if room_type:
            base_query = base_query.filter_by(room_type=room_type)
        
        return base_query.all()
