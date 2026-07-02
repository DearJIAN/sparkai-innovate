from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.response import success, error

auth_bp = Blueprint('auth', __name__)

VALID_ROLES = {'student', 'teacher', 'judge', 'admin'}


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return error('用户名和密码不能为空', code=400, status_code=400)

    username = data.get('username', '').strip()
    password = data.get('password', '')
    email = data.get('email', '').strip() or None
    role = data.get('role', 'student')

    if len(username) < 3:
        return error('用户名至少3个字符', code=400, status_code=400)

    if len(password) < 6:
        return error('密码至少6个字符', code=400, status_code=400)

    if role not in VALID_ROLES:
        return error(f'角色只能是: {", ".join(VALID_ROLES)}', code=400, status_code=400)

    if User.query.filter_by(username=username).first():
        return error('用户名已存在', code=409, status_code=409)

    if email and User.query.filter_by(email=email).first():
        return error('邮箱已被注册', code=409, status_code=409)

    user = User(
        username=username,
        email=email,
        role=role,
        real_name=data.get('real_name', '').strip() or None,
        phone=data.get('phone', '').strip() or None,
        college=data.get('college', '').strip() or None,
        major=data.get('major', '').strip() or None
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return success(
        data={'user': user.to_dict()},
        message='注册成功',
        code=201
    )


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return error('用户名和密码不能为空', code=400, status_code=400)

    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = User.query.filter_by(username=username).first()

    if not user:
        return error('用户名或密码错误', code=401, status_code=401)

    if not user.check_password(password):
        return error('用户名或密码错误', code=401, status_code=401)

    if not user.is_active:
        return error('账号已被禁用，请联系管理员', code=403, status_code=403)

    access_token = create_access_token(identity=str(user.id))

    return success(
        data={
            'token': access_token,
            'user': user.to_dict()
        },
        message='登录成功',
        code=200
    )


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)

    if not user:
        return error('用户不存在', code=404, status_code=404)

    return success(
        data={'user': user.to_dict()},
        message='获取成功',
        code=200
    )


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return success(message='登出成功', code=200)
