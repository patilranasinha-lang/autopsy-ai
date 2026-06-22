import pytest
from app.services import UserService, UploadService, ReportService
from app.models import User


def test_user_service_create(app):
    """Test UserService.create_user"""
    with app.app_context():
        service = UserService()
        user = service.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'


def test_user_service_duplicate_username(app):
    """Test UserService.create_user with duplicate username"""
    with app.app_context():
        service = UserService()
        service.create_user(
            username='testuser',
            email='test1@example.com',
            password='testpass123'
        )
        
        with pytest.raises(ValueError, match='Username already exists'):
            service.create_user(
                username='testuser',
                email='test2@example.com',
                password='testpass123'
            )


def test_upload_service_create(app):
    """Test UploadService.create_upload"""
    with app.app_context():
        user_service = UserService()
        upload_service = UploadService()
        
        user = user_service.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        upload = upload_service.create_upload(
            user_id=user.id,
            file_name='test.csv',
            file_type='text/csv',
            file_size=1024
        )
        assert upload.file_name == 'test.csv'
        assert upload.processing_status == 'pending'


def test_upload_service_get_by_user_id(app):
    """Test UploadService.get_uploads_by_user_id"""
    with app.app_context():
        user_service = UserService()
        upload_service = UploadService()
        
        user = user_service.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        for i in range(3):
            upload_service.create_upload(
                user_id=user.id,
                file_name=f'test{i}.csv',
                file_type='text/csv',
                file_size=1024
            )
        
        result = upload_service.get_uploads_by_user_id(user.id, page=1, per_page=10)
        assert result['total'] == 3


def test_report_service_create(app):
    """Test ReportService.create_report"""
    with app.app_context():
        user_service = UserService()
        report_service = ReportService()
        
        user = user_service.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        report = report_service.create_report(
            user_id=user.id,
            report_type='analysis',
            report_data={'key': 'value'}
        )
        assert report.report_type == 'analysis'


def test_report_service_get_by_user_id(app):
    """Test ReportService.get_reports_by_user_id"""
    with app.app_context():
        user_service = UserService()
        report_service = ReportService()
        
        user = user_service.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        for i in range(2):
            report_service.create_report(
                user_id=user.id,
                report_type=f'type{i}',
                report_data={'data': f'report{i}'}
            )
        
        result = report_service.get_reports_by_user_id(user.id, page=1, per_page=10)
        assert result['total'] == 2
