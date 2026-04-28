from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User


ROLE_HIERARCHY = {
    'student': 1,
    'teacher': 2,
    'judge': 3,
    'admin': 4
}


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({'code': 401, 'message': '登录已过期，请重新登录', 'data': None}), 401
        return fn(*args, **kwargs)
    return wrapper


def require_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'code': 401, 'message': '登录已过期，请重新登录', 'data': None}), 401

            user = _get_current_user()

            if not user:
                return jsonify({'code': 404, 'message': '用户不存在', 'data': None}), 404

            if user.role not in roles:
                return jsonify({
                    'code': 403,
                    'message': f'权限不足，需要角色: {", ".join(roles)}',
                    'data': None
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_min_role(min_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({'code': 401, 'message': '登录已过期，请重新登录', 'data': None}), 401

            user = _get_current_user()

            if not user:
                return jsonify({'code': 404, 'message': '用户不存在', 'data': None}), 404

            user_level = ROLE_HIERARCHY.get(user.role, 0)
            min_level = ROLE_HIERARCHY.get(min_role, 0)

            if user_level < min_level:
                return jsonify({
                    'code': 403,
                    'message': f'权限不足，需要 {min_role} 及以上角色',
                    'data': None
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
