from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import require_roles

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_stats():
    return jsonify({
        'total_projects': 0,
        'total_users': 0,
        'pending_reviews': 0,
        'completed_reviews': 0
    }), 200


@dashboard_bp.route('/trends', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_trends():
    return jsonify({
        'months': ['1月', '2月', '3月', '4月', '5月', '6月'],
        'project_counts': [0, 0, 0, 0, 0, 0]
    }), 200
