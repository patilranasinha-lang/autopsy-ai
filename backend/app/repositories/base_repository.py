from typing import Type, List, Optional, Any
from app import db
from sqlalchemy.orm import Query


class BaseRepository:
    def __init__(self, model: Type[db.Model]):
        self.model = model
    
    def get_all(self, page: int = 1, per_page: int = 20) -> dict:
        """Paginated get all"""
        pagination = self.model.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
        
    def get_by_id(self, id: int) -> Optional[Any]:
        return self.model.query.get(id)
        
    def create(self, instance: Optional[db.Model] = None, **kwargs) -> Any:
        if instance:
            db.session.add(instance)
        else:
            instance = self.model(**kwargs)
            db.session.add(instance)
        db.session.commit()
        return instance
        
    def update(self, id: int, **kwargs) -> Optional[Any]:
        instance = self.get_by_id(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        db.session.commit()
        return instance
        
    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if not instance:
            return False
        db.session.delete(instance)
        db.session.commit()
        return True
