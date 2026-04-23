"""
Database utilities and helper functions
"""
import logging
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DatabaseUtils:
    """Database utility functions"""
    
    @staticmethod
    @contextmanager
    def session_scope(session):
        """Provide a transactional scope for database operations"""
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            session.rollback()
            raise
        finally:
            session.close()
    
    @staticmethod
    def paginate(query, page: int = 1, per_page: int = 20):
        """Paginate query results"""
        if page < 1:
            page = 1
        if per_page < 1:
            per_page = 20
        if per_page > 100:
            per_page = 100
        
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    @staticmethod
    def bulk_insert(db, objects: List[Any], batch_size: int = 100):
        """Bulk insert objects into database"""
        try:
            for i in range(0, len(objects), batch_size):
                batch = objects[i:i + batch_size]
                db.session.bulk_insert_mappings(
                    type(batch[0]),
                    [obj.__dict__ for obj in batch]
                )
                db.session.commit()
            logger.info(f"Inserted {len(objects)} objects in batches of {batch_size}")
        except SQLAlchemyError as e:
            logger.error(f"Bulk insert error: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
    
    @staticmethod
    def soft_delete(db, obj: Any, deleted_at_column: str = 'deleted_at'):
        """Soft delete an object (mark as deleted without removing from DB)"""
        try:
            if hasattr(obj, deleted_at_column):
                from datetime import datetime
                setattr(obj, deleted_at_column, datetime.utcnow())
                db.session.commit()
                logger.info(f"Soft deleted {obj.__class__.__name__} with id {obj.id}")
            else:
                logger.warning(f"Object does not support soft delete: {obj.__class__.__name__}")
        except SQLAlchemyError as e:
            logger.error(f"Soft delete error: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
    
    @staticmethod
    def update_object(db, obj: Any, data: Dict[str, Any]):
        """Update object attributes and save"""
        try:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            logger.info(f"Updated {obj.__class__.__name__} with id {obj.id}")
            return obj
        except SQLAlchemyError as e:
            logger.error(f"Update error: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
    
    @staticmethod
    def get_or_create(db, model: type, **kwargs) -> tuple:
        """Get or create model instance"""
        try:
            instance = db.session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance, False
            
            instance = model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance, True
        except SQLAlchemyError as e:
            logger.error(f"Get or create error: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
    
    @staticmethod
    def delete_by_id(db, model: type, obj_id: int) -> bool:
        """Delete object by id"""
        try:
            obj = db.session.query(model).get(obj_id)
            if obj:
                db.session.delete(obj)
                db.session.commit()
                logger.info(f"Deleted {model.__name__} with id {obj_id}")
                return True
            return False
        except SQLAlchemyError as e:
            logger.error(f"Delete error: {str(e)}", exc_info=True)
            db.session.rollback()
            raise
