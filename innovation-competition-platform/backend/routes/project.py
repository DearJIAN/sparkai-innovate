from flask import Blueprint, request
from sqlalchemy import or_
from models.project import Project
from models.project_member import ProjectMember
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error

project_bp = Blueprint('project', __name__)


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def _check_project_access(project, user):
    """检查用户是否有权访问项目"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    if project.teacher_id == user.id:
        return True
    # 检查是否是项目成员
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    return False


@project_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    """获取项目列表（按角色过滤）"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    # 查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    keyword = request.args.get('keyword', '').strip()
    status = request.args.get('status', '').strip()
    stage = request.args.get('stage', '').strip()
    track = request.args.get('track', '').strip()

    # 基础查询
    query = Project.query

    # 按角色过滤
    if user.is_student():
        # 学生：自己负责或参与的项目
        member_project_ids = db.session.query(ProjectMember.project_id).filter_by(user_id=user.id).all()
        member_project_ids = [m[0] for m in member_project_ids]
        query = query.filter(
            or_(
                Project.leader_id == user.id,
                Project.id.in_(member_project_ids) if member_project_ids else False
            )
        )
    elif user.is_teacher():
        # 教师：自己指导的项目
        query = query.filter(Project.teacher_id == user.id)
    elif user.is_judge():
        # 评委：已提交或评审中的项目
        query = query.filter(Project.status.in_(['submitted', 'teacher_review', 'judging', 'passed', 'rejected']))
    # admin 不过滤，查看所有

    # 关键字搜索
    if keyword:
        query = query.filter(Project.name.contains(keyword))

    # 状态过滤
    if status:
        query = query.filter(Project.status == status)

    # 阶段过滤
    if stage:
        query = query.filter(Project.stage == stage)

    # 赛道过滤
    if track:
        query = query.filter(Project.track == track)

    # 排序和分页
    query = query.order_by(Project.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'projects': [project.to_dict() for project in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@project_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    """创建项目（仅学生）"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    if not user.is_student() and not user.is_admin():
        return error('只有学生可以创建项目', code=403, status_code=403)

    data = request.get_json()
    if not data or not data.get('name'):
        return error('项目名称不能为空', code=400, status_code=400)

    project = Project(
        name=data.get('name', '').strip(),
        description=data.get('description', '').strip() or None,
        category=data.get('category', '').strip() or None,
        track=data.get('track', '').strip() or None,
        stage='idea',
        status='draft',
        leader_id=user.id,
        teacher_id=data.get('teacher_id') or None,
        competition_id=data.get('competition_id') or None
    )

    db.session.add(project)
    db.session.commit()

    return success({
        'project': project.to_dict()
    }, message='项目创建成功', code=201)


@project_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """查看项目详情"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查
    if not _check_project_access(project, user):
        return error('无权查看该项目', code=403, status_code=403)

    # 获取关联数据
    members = ProjectMember.query.filter_by(project_id=project.id).all()
    files_count = ProjectMember.query.filter_by(project_id=project.id).count()
    tasks_count = ProjectMember.query.filter_by(project_id=project.id).count()

    result = project.to_dict()
    result['members'] = [m.to_dict() for m in members]
    result['files_count'] = files_count
    result['tasks_count'] = tasks_count

    return success({
        'project': result
    })


@project_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """编辑项目"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或 admin
    if project.leader_id != user.id and not user.is_admin():
        return error('无权编辑该项目', code=403, status_code=403)

    # 已进入评审阶段的项目不允许随意修改核心信息
    if project.status in ['judging', 'passed', 'rejected'] and not user.is_admin():
        return error('该项目已进入评审阶段，无法修改', code=403, status_code=403)

    data = request.get_json()

    # 可编辑字段
    editable_fields = ['name', 'description', 'category', 'track', 'stage', 'teacher_id', 'competition_id']
    for field in editable_fields:
        if field in data:
            value = data[field]
            if isinstance(value, str):
                value = value.strip() or None
            setattr(project, field, value)

    db.session.commit()

    return success({
        'project': project.to_dict()
    }, message='项目更新成功')


@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """删除项目（仅 draft 状态）"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或 admin
    if project.leader_id != user.id and not user.is_admin():
        return error('无权删除该项目', code=403, status_code=403)

    # 只有 draft 状态允许删除
    if project.status != 'draft':
        return error('只有草稿状态的项目可以删除', code=403, status_code=403)

    db.session.delete(project)
    db.session.commit()

    return success(message='项目删除成功')


@project_bp.route('/<int:project_id>/submit', methods=['POST'])
@jwt_required()
def submit_project(project_id):
    """提交项目进入评审"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查：项目负责人或 admin
    if project.leader_id != user.id and not user.is_admin():
        return error('无权提交该项目', code=403, status_code=403)

    # 只有 draft 或 need_modify 状态可以提交
    if project.status not in ['draft', 'need_modify']:
        return error(f'当前状态为 {project.status}，无法提交', code=403, status_code=403)

    project.status = 'submitted'
    db.session.commit()

    return success({
        'project': project.to_dict()
    }, message='项目提交成功，等待审核')
