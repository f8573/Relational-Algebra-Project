"""Auth routes."""
from flask import Blueprint, jsonify, request, current_app
from app.models import User
from app.extensions import db
from .auth_decorators import verify_token
import jwt
from datetime import datetime, timedelta

bp = Blueprint("auth", __name__)


@bp.route('/login', methods=['POST'])
def login():
    """Login endpoint: accepts email/password, returns JWT token."""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({
            "status": "error",
            "message": "Missing email or password"
        }), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({
            "status": "error",
            "message": "Invalid email or password"
        }), 401

        # Log successful login (do not log password)
        current_app.logger.info(
            "User login success: user_id=%s email=%s from %s",
            user.id,
            user.email,
            request.remote_addr
        )
        # Record audit event for login
        try:
            from app.models import AuditLog
            AuditLog.record(actor_id=user.id, event_type='login', resource_type='user', resource_id=user.id, ip=request.remote_addr, ua=request.headers.get('User-Agent'))
        except Exception:
            current_app.logger.exception('Failed to record login audit')

    # Determine token lifetime based on 'remember' flag
    remember = bool(data.get('remember')) if isinstance(data, dict) else False

    # Generate JWT token
    payload = {
        'user_id': user.id,
        'email': user.email,
        'iat': datetime.utcnow(),
        'remember': bool(remember)
    }
    if remember:
        # 30 days expiration
        payload['exp'] = datetime.utcnow() + timedelta(days=30)
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], 
                      algorithm=current_app.config['JWT_ALGORITHM'])

    return jsonify({
        "status": "success",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_platform_admin": user.is_platform_admin
        }
    }), 200


@bp.route('/register', methods=['POST'])
def register():
    """Create a new user account. No email verification for demo purposes."""
    data = request.get_json() or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password')
    name = data.get('name')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'email and password required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'user already exists'}), 400

    user = User(email=email, name=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'success', 'user': {'id': user.id, 'email': user.email, 'name': user.name}}), 201


@bp.route('/user', methods=['GET'])
@verify_token
def get_user():
    """Get current user info from token."""
    user = request.user
    
    return jsonify({
        "status": "success",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_platform_admin": user.is_platform_admin,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    }), 200


@bp.route('/user', methods=['PUT'])
@verify_token
def update_user():
    """Update current user's profile (name)."""
    user = request.user
    data = request.get_json() or {}
    name = data.get('name')
    if name is not None:
        user.name = name
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'success', 'user': {'id': user.id, 'email': user.email, 'name': user.name}}), 200


@bp.route('/user/password', methods=['POST'])
@verify_token
def change_password():
    """Change current user's password. For demo, no current-password verification required.

    Request JSON: { 'new_password': '...' }
    """
    user = request.user
    data = request.get_json() or {}
    newpw = data.get('new_password')
    if not newpw:
        return jsonify({'status': 'error', 'message': 'new_password required'}), 400
    user.set_password(newpw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'password changed'}), 200


@bp.route('/refresh', methods=['POST'])
@verify_token
def refresh():
    """Refresh JWT token for current user."""
    user = request.user
    
    # Generate new token
    # Refresh token: preserve "remember" preference from original token if present
    try:
        orig_payload = jwt.decode(request.token, current_app.config['SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']], options={"verify_exp": False})
    except Exception:
        orig_payload = {}

    remember = bool(orig_payload.get('remember'))
    payload = {
        'user_id': user.id,
        'email': user.email,
        'iat': datetime.utcnow(),
        'remember': bool(remember)
    }
    if remember:
        payload['exp'] = datetime.utcnow() + timedelta(days=30)

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])
    
    return jsonify({
        "status": "success",
        "token": token
    }), 200


@bp.route('/logout', methods=['POST'])
@verify_token
def logout():
    """Logout endpoint (mainly for client-side cleanup)."""
    # In a real app, you might invalidate the token on the server
    # For now, just acknowledge the logout request
    return jsonify({
        "status": "success",
        "message": "Logged out successfully"
    }), 200
