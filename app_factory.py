from flask import Flask
from datetime import timedelta
import os
import pickle

from extensions import db, bcrypt, jwt, cors
from auth_routes import auth_bp
from prediction_routes import predictions_bp
from utility_routes import utility_bp
from web_routes import web_bp


def load_models():
    regressor = None
    classifier = None
    label_encoder = None

    try:
        with open('models/regressor.pkl', 'rb') as f:
            regressor = pickle.load(f)
    except FileNotFoundError:
        print('Warning: regressor.pkl not found. Please ensure model files are in the models directory.')

    try:
        with open('models/classifier.pkl', 'rb') as f:
            classifier = pickle.load(f)
    except FileNotFoundError:
        print('Warning: classifier.pkl not found. Please ensure model files are in the models directory.')

    try:
        with open('models/label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
    except FileNotFoundError:
        print('Warning: label_encoder.pkl not found. Please ensure model files are in the models directory.')

    return regressor, classifier, label_encoder


def create_app():
    app = Flask(__name__)

    database_url = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
    if database_url.startswith('sqlite'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 10,
            'max_overflow': 20,
            'pool_timeout': 30,
        }
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 20,
            'max_overflow': 30,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'pool_timeout': 30,
            'echo': False,
        }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev_secret_key_change_in_production')
    app.config['TOKEN_EXPIRES_DELTA'] = timedelta(hours=1)

    cors.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    regressor, classifier, label_encoder = load_models()
    models_loaded = all([regressor, classifier, label_encoder])
    mock_mode = os.environ.get('MOCK_MODE', '1' if not models_loaded else '0') == '1'

    app.regressor = regressor
    app.classifier = classifier
    app.label_encoder = label_encoder
    app.models_loaded = models_loaded
    app.MOCK_MODE = mock_mode

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(predictions_bp, url_prefix='/api')
    app.register_blueprint(utility_bp, url_prefix='/api')
    app.register_blueprint(web_bp)

    return app
