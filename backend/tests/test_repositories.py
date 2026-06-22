import pytest
from app.repositories import UserRepository, UploadRepository, ReportRepository
from app.models import User


def test_user_repository_create(app):
    """Test UserRepository.create"""
    with app.app_context():
        repo = UserRepository()
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        repo.create(user)
        
        found = repo.get_by_id(user.id)
        assert found is not None
        assert found.username == 'testuser'


def test_user_repository_get_by_username(app):
    """Test UserRepository.get_by_username"""
    with app.app_context():
        repo = UserRepository()
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        repo.create(user)
        
        found = repo.get_by_username('testuser')
        assert found is not None
        assert found.email == 'test@example.com'


def test_user_repository_get_by_email(app):
    """Test UserRepository.get_by_email"""
    with app.app_context():
        repo = UserRepository()
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        repo.create(user)
        
        found = repo.get_by_email('test@example.com')
        assert found is not None
        assert found.username == 'testuser'


def test_upload_repository_create(app):
    """Test UploadRepository.create"""
    with app.app_context():
        user_repo = UserRepository()
        upload_repo = UploadRepository()
        
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        user_repo.create(user)
        
        from app.models import Upload
        upload = Upload(
            user_id=user.id,
            file_name='test.csv',
            file_type='text/csv',
            file_size=1024
        )
        upload_repo.create(upload)
        
        found = upload_repo.get_by_id(upload.id)
        assert found is not None
        assert found.file_name == 'test.csv'


def test_upload_repository_get_by_user_id(app):
    """Test UploadRepository.get_by_user_id"""
    with app.app_context():
        user_repo = UserRepository()
        upload_repo = UploadRepository()
        
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        user_repo.create(user)
        
        from app.models import Upload
        for i in range(3):
            upload = Upload(
                user_id=user.id,
                file_name=f'test{i}.csv',
                file_type='text/csv',
                file_size=1024
            )
            upload_repo.create(upload)
        
        result = upload_repo.get_by_user_id(user.id, page=1, per_page=10)
        assert result['total'] == 3


def test_report_repository_create(app):
    """Test ReportRepository.create"""
    with app.app_context():
        user_repo = UserRepository()
        report_repo = ReportRepository()
        
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        user_repo.create(user)
        
        from app.models import Report
        report = Report(
            user_id=user.id,
            report_type='analysis',
            report_data={'key': 'value'}
        )
        report_repo.create(report)
        
        found = report_repo.get_by_id(report.id)
        assert found is not None
        assert found.report_type == 'analysis'


def test_report_repository_get_by_user_id(app):
    """Test ReportRepository.get_by_user_id"""
    with app.app_context():
        user_repo = UserRepository()
        report_repo = ReportRepository()
        
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpass123')
        user_repo.create(user)
        
        from app.models import Report
        for i in range(2):
            report = Report(
                user_id=user.id,
                report_type=f'type{i}',
                report_data={'data': f'report{i}'}
            )
            report_repo.create(report)
        
        result = report_repo.get_by_user_id(user.id, page=1, per_page=10)
        assert result['total'] == 2
