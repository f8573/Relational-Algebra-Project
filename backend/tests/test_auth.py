"""Tests for authentication routes and decorators."""

import json
import pytest
from datetime import datetime, timedelta
import jwt
from app import create_app
from app.extensions import db
from app.models import User, Course, CourseMembership


@pytest.fixture
def app():
    """Create and configure a Flask test app."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    """Helper to generate auth headers."""
    def _make_headers(token=None):
        headers = {'Content-Type': 'application/json'}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        return headers
    return _make_headers


@pytest.fixture
def sample_user(app):
    """Create a sample user."""
    with app.app_context():
        user = User(email='test@example.com', name='Test User')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    return user_id


@pytest.fixture
def sample_course(app, sample_user):
    """Create a sample course with user enrollment."""
    with app.app_context():
        course = Course(title='Test Course', description='A test course')
        db.session.add(course)
        db.session.commit()
        
        membership = CourseMembership(
            course_id=course.id,
            user_id=sample_user,
            role='student'
        )
        db.session.add(membership)
        db.session.commit()
        return course.id


class TestLogin:
    """Tests for /api/auth/login endpoint."""
    
    def test_login_success(self, client, sample_user, auth_headers):
        """Test successful login with valid credentials."""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'password123'}),
            headers=auth_headers()
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'token' in data
        assert data['user']['email'] == 'test@example.com'
        assert data['user']['name'] == 'Test User'
    
    def test_login_invalid_password(self, client, sample_user, auth_headers):
        """Test login with invalid password."""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com', 'password': 'wrongpassword'}),
            headers=auth_headers()
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_missing_email(self, client, auth_headers):
        """Test login with missing email."""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'password': 'password123'}),
            headers=auth_headers()
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_missing_password(self, client, auth_headers):
        """Test login with missing password."""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'test@example.com'}),
            headers=auth_headers()
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_login_user_not_found(self, client, auth_headers):
        """Test login with non-existent user."""
        response = client.post(
            '/api/auth/login',
            data=json.dumps({'email': 'nonexistent@example.com', 'password': 'password123'}),
            headers=auth_headers()
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestUser:
    """Tests for /api/auth/user endpoint."""
    
    def test_get_user_success(self, app, client, sample_user, auth_headers):
        """Test getting user info with valid token."""
        with app.app_context():
            payload = {
                'user_id': sample_user,
                'email': 'test@example.com',
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.get(
            '/api/auth/user',
            headers=auth_headers(token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['user']['email'] == 'test@example.com'
    
    def test_get_user_no_token(self, client, auth_headers):
        """Test getting user info without token."""
        response = client.get(
            '/api/auth/user',
            headers=auth_headers()
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_get_user_invalid_token(self, client, auth_headers):
        """Test getting user info with invalid token."""
        response = client.get(
            '/api/auth/user',
            headers=auth_headers('invalid.token.here')
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestRefresh:
    """Tests for /api/auth/refresh endpoint."""
    
    def test_refresh_token_success(self, app, client, sample_user, auth_headers):
        """Test refreshing token with valid token."""
        with app.app_context():
            payload = {
                'user_id': sample_user,
                'email': 'test@example.com',
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.post(
            '/api/auth/refresh',
            data=json.dumps({}),
            headers=auth_headers(token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'token' in data
    
    def test_refresh_token_no_token(self, client, auth_headers):
        """Test refreshing token without token."""
        response = client.post(
            '/api/auth/refresh',
            data=json.dumps({}),
            headers=auth_headers()
        )
        
        assert response.status_code == 401


class TestLogout:
    """Tests for /api/auth/logout endpoint."""
    
    def test_logout_success(self, app, client, sample_user, auth_headers):
        """Test logout with valid token."""
        with app.app_context():
            payload = {
                'user_id': sample_user,
                'email': 'test@example.com',
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.post(
            '/api/auth/logout',
            data=json.dumps({}),
            headers=auth_headers(token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'


class TestCourses:
    """Tests for /api/courses endpoints."""
    
    def test_list_courses(self, app, client, sample_user, sample_course, auth_headers):
        """Test listing user's courses."""
        with app.app_context():
            payload = {
                'user_id': sample_user,
                'email': 'test@example.com',
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.get(
            '/api/courses/',
            headers=auth_headers(token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert len(data['courses']) == 1
        assert data['courses'][0]['title'] == 'Test Course'
        assert data['courses'][0]['role'] == 'student'
    
    def test_get_course(self, app, client, sample_user, sample_course, auth_headers):
        """Test getting course details."""
        with app.app_context():
            payload = {
                'user_id': sample_user,
                'email': 'test@example.com',
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.get(
            f'/api/courses/{sample_course}',
            headers=auth_headers(token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['course']['title'] == 'Test Course'
        assert data['course']['role'] == 'student'
    
    def test_get_course_not_enrolled(self, app, client, auth_headers):
        """Test getting course without enrollment."""
        # Create a user not enrolled in any course
        with app.app_context():
            user = User(email='other@example.com', name='Other User')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            user_id = user.id
            
            payload = {
                'user_id': user_id,
                'email': user.email,
                'exp': datetime.utcnow() + timedelta(hours=24),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm=app.config['JWT_ALGORITHM']
            )
        
        response = client.get(
            '/api/courses/999',
            headers=auth_headers(token)
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['status'] == 'error'
