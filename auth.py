"""Authentication blueprint and helpers."""

from flask import Blueprint, current_app, request, jsonify, g, make_response
from functools import wraps
import datetime
import jwt
import bcrypt

from models import User, db

auth_bp = Blueprint('auth', __name__)


def encode_jwt(user_id):
    """Encode user ID into JWT token."""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }
    token = jwt.encode(payload, current_app.config['JWT_SECRET'], algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def decode_jwt(token):
    """Decode JWT token and return payload."""
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except Exception:
        return None


def auth_required(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('jwt') or request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token.split(' ', 1)[1]
        payload = decode_jwt(token) if token else None
        if not payload or not payload.get('user_id'):
            return jsonify({'message': 'Token invalid or missing'}), 401
        g.user_id = payload['user_id']
        return f(*args, **kwargs)
    return wrapper


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user."""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password=hashed)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = encode_jwt(user.id)
    resp = make_response(jsonify({'message': 'Login successful', 'username': username}))

    # Set secure=True in production with HTTPS
    resp.set_cookie('jwt', token, httponly=True, samesite='Strict')
    return resp


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user by clearing JWT cookie."""
    resp = make_response(jsonify({'message': 'Logged out successfully'}))
    resp.set_cookie('jwt', '', expires=0, httponly=True, samesite='Strict')
    return resp


@auth_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user():
    """Get current authenticated user info."""
    user = User.query.get(g.user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'username': user.username
    })
