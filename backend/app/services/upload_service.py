import logging
from typing import Optional
from app.repositories import UploadRepository
from app.models import Upload
from app import db

logger = logging.getLogger(__name__)


class UploadService:
    def __init__(self):
        self.upload_repo = UploadRepository()
        
    def create_upload(self, user_id: int, file_name: str, file_type: str, file_size: int) -> Upload:
        upload = Upload(
            user_id=user_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size
        )
        self.upload_repo.create(upload)
        
        logger.info(f'Upload created for user {user_id}: {file_name}')
        return upload
        
    def get_all_uploads(self, page: int = 1, per_page: int = 20):
        return self.upload_repo.get_all(page, per_page)
        
    def get_uploads_by_user_id(self, user_id: int, page: int = 1, per_page: int = 20):
        return self.upload_repo.get_by_user_id(user_id, page, per_page)
        
    def get_upload_by_id(self, upload_id: int) -> Optional[Upload]:
        return self.upload_repo.get_by_id(upload_id)
        
    def update_upload_status(self, upload_id: int, status: str) -> Optional[Upload]:
        upload = self.upload_repo.get_by_id(upload_id)
        if not upload:
            return None
        upload.processing_status = status
        db.session.commit()
        
        logger.info(f'Upload {upload_id} status updated to {status}')
        return upload
