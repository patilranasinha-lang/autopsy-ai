from app.repositories.base_repository import BaseRepository
from app.models import Report


class ReportRepository(BaseRepository):
    def __init__(self):
        super().__init__(Report)
        
    def get_by_user_id(self, user_id: int, page: int = 1, per_page: int = 20) -> dict:
        pagination = Report.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': pagination.items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }
