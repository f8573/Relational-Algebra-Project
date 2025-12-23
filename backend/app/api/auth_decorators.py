"""JWT token verification utilities."""

import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User


def verify_token(f):
    """Decorator to verify JWT token and attach user to request context."""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Allow preflight CORS requests to pass through without auth
        if request.method == 'OPTIONS':
            return ('', 200)
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except IndexError:
                current_app.logger.warning(
                    "Invalid Authorization header format from %s: %s",
                    request.remote_addr,
                    request.headers.get('Authorization')
                )
                return jsonify({'status': 'error', 'message': 'Invalid token format'}), 401
        
        if not token:
            current_app.logger.info(
                "Missing authorization token for request from %s to %s",
                request.remote_addr,
                request.path
            )
            return jsonify({'status': 'error', 'message': 'Missing authorization token'}), 401
        
        try:
            # Do not log the full token; log a short fingerprint for tracing
            token_fingerprint = token[:8] + '...'
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], 
                               algorithms=[current_app.config['JWT_ALGORITHM']])
            user_id = payload.get('user_id')
            user = User.query.get(user_id)
            if not user:
                current_app.logger.warning(
                    "Token verified but user not found (user_id=%s) from %s (token=%s)",
                    user_id,
                    request.remote_addr,
                    token_fingerprint
                )
                return jsonify({'status': 'error', 'message': 'User not found'}), 401
            
            # Attach user to request context
            request.user = user
            request.token = token
            current_app.logger.debug(
                "Token verified for user_id=%s from %s (token=%s)",
                user_id,
                request.remote_addr,
                token_fingerprint
            )
        except jwt.ExpiredSignatureError:
            current_app.logger.info(
                "Expired token received from %s for %s",
                request.remote_addr,
                request.path
            )
            return jsonify({'status': 'error', 'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            current_app.logger.warning(
                "Invalid token from %s for %s: %s",
                request.remote_addr,
                request.path,
                str(e)
            )
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def require_role(*allowed_roles):
    """Decorator to check if user has one of the allowed roles in the course context."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
            
            # For now, just check if user has platform admin role
            # Course-specific role checks should be done in the route
            if not allowed_roles or request.user.is_platform_admin:
                return f(*args, **kwargs)
            
            return jsonify({'status': 'error', 'message': 'Insufficient permissions'}), 403
        return decorated
    return decorator
