from flask import Blueprint, request
from datetime import datetime
from models.project import Project
from models.project_member import ProjectMember
from models.project_task import ProjectTask
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error

task_bp = Blueprint('task', __name__)


TASK_STATUS_LIST = ['todo', 'doing', 'done', 'delayed', 'cancelled']
TASK_PRIORITY_LIST = ['low', 'medium', 'high']


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
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    return False


def _check_task_manage_permission(project, user):
    """检查用户是否有管理任务的权限（负责人或admin）"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    return False


@task_bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@jwt_required()
def get_tasks(project_id):
    """获取项目任务列表"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_project_access(project, user):
        return error('无权查看该项目任务', code=403, status_code=403)

    # 查询参数
    status = request.args.get('status', '').strip()
    priority = request.args.get('priority', '').strip()

    query = ProjectTask.query.filter_by(project_id=project_id)

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    tasks = query.order_by(ProjectTask.created_at.desc()).all()

    # 统计
    total = ProjectTask.query.filter_by(project_id=project_id).count()
    done_count = ProjectTask.query.filter_by(project_id=project_id, status='done').count()
    doing_count = ProjectTask.query.filter_by(project_id=project_id, status='doing').count()
    todo_count = ProjectTask.query.filter_by(project_id=project_id, status='todo').count()
    delayed_count = ProjectTask.query.filter_by(project_id=project_id, status='delayed').count()

    return success({
        'tasks': [t.to_dict() for t in tasks],
        'stats': {
            'total': total,
            'done': done_count,
            'doing': doing_count,
            'todo': todo_count,
            'delayed': delayed_count,
            'completion_rate': round(done_count / total * 100, 1) if total > 0 else 0
        }
    })


@task_bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@jwt_required()
def create_task(project_id):
    """创建项目任务"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_task_manage_permission(project, user):
        return error('无权创建任务', code=403, status_code=403)

    data = request.get_json()
    if not data or not data.get('title'):
        return error('任务标题不能为空', code=400, status_code=400)

    status = data.get('status', 'todo')
    if status not in TASK_STATUS_LIST:
        status = 'todo'

    priority = data.get('priority', 'medium')
    if priority not in TASK_PRIORITY_LIST:
        priority = 'medium'

    deadline = None
    if data.get('deadline'):
        try:
            deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00').replace('+00:00', ''))
        except ValueError:
            pass

    task = ProjectTask(
        project_id=project_id,
        title=data.get('title', '').strip(),
        description=data.get('description', '').strip() or None,
        assignee_id=data.get('assignee_id') or None,
        status=status,
        priority=priority,
        deadline=deadline
    )

    db.session.add(task)
    db.session.commit()

    return success({
        'task': task.to_dict()
    }, message='任务创建成功', code=201)


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """更新任务"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    task = ProjectTask.query.get(task_id)
    if not task:
        return error('任务不存在', code=404, status_code=404)

    project = Project.query.get(task.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_task_manage_permission(project, user):
        return error('无权编辑任务', code=403, status_code=403)

    data = request.get_json()

    if 'title' in data:
        task.title = data['title'].strip()
    if 'description' in data:
        task.description = data['description'].strip() or None
    if 'assignee_id' in data:
        task.assignee_id = data['assignee_id'] or None
    if 'status' in data and data['status'] in TASK_STATUS_LIST:
        task.status = data['status']
        # 如果状态改为 done，记录完成时间
        if task.status == 'done' and not task.completed_at:
            task.completed_at = datetime.now()
        # 如果状态从 done 改回其他，清除完成时间
        if task.status != 'done':
            task.completed_at = None
    if 'priority' in data and data['priority'] in TASK_PRIORITY_LIST:
        task.priority = data['priority']
    if 'deadline' in data:
        if data['deadline']:
            try:
                task.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00').replace('+00:00', ''))
            except ValueError:
                pass
        else:
            task.deadline = None

    db.session.commit()

    return success({
        'task': task.to_dict()
    }, message='任务更新成功')


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """删除任务"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    task = ProjectTask.query.get(task_id)
    if not task:
        return error('任务不存在', code=404, status_code=404)

    project = Project.query.get(task.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_task_manage_permission(project, user):
        return error('无权删除任务', code=403, status_code=403)

    db.session.delete(task)
    db.session.commit()

    return success(message='任务删除成功')
