from flask import Blueprint, jsonify, request as req
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import require_roles
from utils.response import success, error

user_bp = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return success({
        'users': [user.to_dict() for user in users],
        'total': len(users)
    })


@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    if current_user_id != user_id and not User.query.get(current_user_id).is_admin():
        return error('权限不足', code=403, status_code=403)
    return success({'user': user.to_dict()})


@user_bp.route('/', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_user():
    data = req.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return error('用户名和密码为必填项', code=400, status_code=400)
    if User.query.filter_by(username=data['username']).first():
        return error('用户名已存在', code=400, status_code=400)
    if data.get('email') and User.query.filter_by(email=data['email']).first():
        return error('邮箱已被注册', code=400, status_code=400)
    user = User(
        username=data['username'],
        real_name=data.get('real_name', ''),
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        role=data.get('role', 'student'),
        college=data.get('college', ''),
        major=data.get('major', ''),
        is_active=data.get('is_active', True)
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return success({'user': user.to_dict()}, code=201)


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = req.get_json()
    if not data:
        return error('无数据', code=400, status_code=400)
    if data.get('email') and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return error('邮箱已被注册', code=400, status_code=400)
    for field in ['real_name', 'email', 'phone', 'role', 'college', 'major']:
        if field in data:
            setattr(user, field, data[field])
    if 'is_active' in data:
        user.is_active = data['is_active']
    if data.get('password'):
        user.set_password(data['password'])
    db.session.commit()
    return success({'user': user.to_dict()})


@user_bp.route('/<int:user_id>/toggle-status', methods=['POST'])
@jwt_required()
@require_roles('admin')
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return success({'user': user.to_dict()})


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id == user_id:
        return error('不能删除自己', code=400, status_code=400)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return success(message='用户已删除')
