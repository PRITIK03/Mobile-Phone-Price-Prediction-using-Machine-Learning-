from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token

from extensions import db, bcrypt
from models import User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400
    if len(username) < 3 or len(username) > 50:
        return jsonify({'error': 'Username must be 3-50 characters.'}), 400
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters.'}), 400
    if not username.replace('_', '').replace('-', '').isalnum():
        return jsonify({'error': 'Username can only contain letters, numbers, underscores, and hyphens.'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409

    try:
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Registration failed. Please try again.'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Username and password required.'}), 400

    if hasattr(login, '_attempts'):
        login._attempts = getattr(login, '_attempts', 0) + 1
        if login._attempts > 5:
            return jsonify({'error': 'Too many failed attempts. Please try again later.'}), 429
    else:
        login._attempts = 1

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid credentials.'}), 401

    login._attempts = 0
    access_token = create_access_token(identity=username, expires_delta=current_app.config.get('TOKEN_EXPIRES_DELTA'))
    return jsonify({'access_token': access_token}), 200
