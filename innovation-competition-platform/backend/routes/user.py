from flask import Blueprint, jsonify
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import require_roles

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_users():
    users = User.query.all()
    return jsonify({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    }), 200


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # 只能查看自己或管理员查看所有人
    if current_user_id != user_id and not User.query.get(current_user_id).is_admin():
        return jsonify({'message': '权限不足'}), 403
    
    return jsonify({'user': user.to_dict()}), 200
