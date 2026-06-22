import logging
from typing import Optional, Dict
from app.repositories import ReportRepository
from app.models import Report

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self):
        self.report_repo = ReportRepository()
        
    def create_report(self, user_id: int, report_type: str, report_data: Dict) -> Report:
        report = Report(
            user_id=user_id,
            report_type=report_type,
            report_data=report_data
        )
        self.report_repo.create(report)
        
        logger.info(f'Report created for user {user_id}: {report_type}')
        return report
        
    def get_all_reports(self, page: int = 1, per_page: int = 20):
        return self.report_repo.get_all(page, per_page)
        
    def get_reports_by_user_id(self, user_id: int, page: int = 1, per_page: int = 20):
        return self.report_repo.get_by_user_id(user_id, page, per_page)
        
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        return self.report_repo.get_by_id(report_id)
