from flask import Blueprint, request
from models.project import Project
from models.project_member import ProjectMember
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error

member_bp = Blueprint('member', __name__)


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def _check_project_manage_permission(project, user):
    """检查用户是否有项目管理权限（负责人或admin）"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    return False


@member_bp.route('/projects/<int:project_id>/members', methods=['GET'])
@jwt_required()
def get_members(project_id):
    """获取项目成员列表"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目相关人可查看
    if not _check_project_access(project, user):
        return error('无权查看该项目成员', code=403, status_code=403)

    members = ProjectMember.query.filter_by(project_id=project_id).all()
    return success({
        'members': [m.to_dict() for m in members]
    })


@member_bp.route('/projects/<int:project_id>/members', methods=['POST'])
@jwt_required()
def add_member(project_id):
    """新增项目成员"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或admin
    if not _check_project_manage_permission(project, user):
        return error('无权管理该项目成员', code=403, status_code=403)

    data = request.get_json()
    if not data or not data.get('member_name'):
        return error('成员姓名不能为空', code=400, status_code=400)

    member = ProjectMember(
        project_id=project_id,
        user_id=data.get('user_id') or None,
        member_name=data.get('member_name', '').strip(),
        role_in_project=data.get('role_in_project', '').strip() or None,
        responsibility=data.get('responsibility', '').strip() or None
    )

    db.session.add(member)
    db.session.commit()

    return success({
        'member': member.to_dict()
    }, message='成员添加成功', code=201)


@member_bp.route('/members/<int:member_id>', methods=['PUT'])
@jwt_required()
def update_member(member_id):
    """编辑成员信息"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    member = ProjectMember.query.get(member_id)
    if not member:
        return error('成员不存在', code=404, status_code=404)

    project = Project.query.get(member.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或admin
    if not _check_project_manage_permission(project, user):
        return error('无权编辑该成员', code=403, status_code=403)

    data = request.get_json()

    if 'member_name' in data:
        member.member_name = data['member_name'].strip()
    if 'role_in_project' in data:
        member.role_in_project = data['role_in_project'].strip() or None
    if 'responsibility' in data:
        member.responsibility = data['responsibility'].strip() or None
    if 'user_id' in data:
        member.user_id = data['user_id'] or None

    db.session.commit()

    return success({
        'member': member.to_dict()
    }, message='成员更新成功')


@member_bp.route('/members/<int:member_id>', methods=['DELETE'])
@jwt_required()
def delete_member(member_id):
    """删除成员"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    member = ProjectMember.query.get(member_id)
    if not member:
        return error('成员不存在', code=404, status_code=404)

    project = Project.query.get(member.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或admin
    if not _check_project_manage_permission(project, user):
        return error('无权删除该成员', code=403, status_code=403)

    # 教师不能随意删除学生成员（只有查看权限）
    if user.is_teacher() and not user.is_admin():
        return error('指导老师无权删除成员', code=403, status_code=403)

    db.session.delete(member)
    db.session.commit()

    return success(message='成员删除成功')


def _check_project_access(project, user):
    """检查用户是否有权访问项目"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    if project.teacher_id == user.id:
        return True
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    return False
