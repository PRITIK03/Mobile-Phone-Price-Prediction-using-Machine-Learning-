from datetime import datetime

from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text

from extensions import db
from models import PredictionHistory, User
from predict_utils import prediction_cache


utility_bp = Blueprint('utility', __name__)


@utility_bp.route('/health', methods=['GET'])
def health_check():
    db_status = True
    try:
        db.session.execute(text('SELECT 1'))
    except Exception:
        db_status = False

    return jsonify({
        'status': 'healthy' if db_status else 'unhealthy',
        'database': 'connected' if db_status else 'disconnected',
        'cache_size': len(prediction_cache),
        'models_loaded': getattr(current_app, 'models_loaded', False),
        'timestamp': datetime.now().isoformat()
    })


@utility_bp.route('/predictions/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        limit = min(per_page, 50)

        predictions = PredictionHistory.query.filter_by(user_id=user.id)\
            .order_by(PredictionHistory.created_at.desc())\
            .paginate(page=page, per_page=limit, error_out=False)

        history_data = []
        for prediction in predictions.items:
            history_data.append({
                'id': prediction.id,
                'battery_size': prediction.battery_size,
                'brand_name': prediction.brand_name,
                'memory_size': prediction.memory_size,
                'model_name': prediction.model_name,
                'lowest_price': prediction.lowest_price,
                'highest_price': prediction.highest_price,
                'release_date': prediction.release_date,
                'screen_size': prediction.screen_size,
                'created_at': prediction.created_at.isoformat()
            })

        return jsonify({
            'predictions': history_data,
            'pagination': {
                'page': page,
                'per_page': limit,
                'total': predictions.total,
                'pages': predictions.pages,
                'has_next': predictions.has_next,
                'has_prev': predictions.has_prev
            }
        })
    except Exception as e:
        print(f"Error fetching prediction history: {e}")
        return jsonify({'error': 'Failed to fetch prediction history'}), 500


@utility_bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
@jwt_required()
def delete_prediction(prediction_id):
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        prediction = PredictionHistory.query.filter_by(id=prediction_id, user_id=user.id).first()
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404

        db.session.delete(prediction)
        db.session.commit()
        return jsonify({'message': 'Prediction deleted successfully'})
    except Exception as e:
        print(f"Error deleting prediction: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete prediction'}), 500


@utility_bp.route('/predictions/stats', methods=['GET'])
@jwt_required()
def get_prediction_stats():
    try:
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        total_predictions = PredictionHistory.query.filter_by(user_id=user.id).count()
        brand_stats = db.session.query(
            PredictionHistory.brand_name,
            db.func.count(PredictionHistory.id).label('count')
        ).filter_by(user_id=user.id)\
         .group_by(PredictionHistory.brand_name)\
         .order_by(db.desc('count'))\
         .limit(5).all()

        avg_low = db.session.query(db.func.avg(PredictionHistory.lowest_price))\
            .filter_by(user_id=user.id).scalar() or 0
        avg_high = db.session.query(db.func.avg(PredictionHistory.highest_price))\
            .filter_by(user_id=user.id).scalar() or 0

        return jsonify({
            'total_predictions': total_predictions,
            'brand_preferences': [{'brand': brand, 'count': count} for brand, count in brand_stats],
            'average_price_range': {
                'lowest': round(avg_low, 2),
                'highest': round(avg_high, 2)
            }
        })
    except Exception as e:
        print(f"Error fetching prediction stats: {e}")
        return jsonify({'error': 'Failed to fetch prediction statistics'}), 500
