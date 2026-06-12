from flask import Blueprint, request
from models.project import Project
from models.project_member import ProjectMember
from models.project_file import ProjectFile
from models.project_task import ProjectTask
from models.review import Review
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error

review_bp = Blueprint('review', __name__)


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


@review_bp.route('/reviews/projects', methods=['GET'])
@jwt_required()
def get_pending_projects():
    """获取待评审项目列表（评委/管理员）"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    if not user.is_judge() and not user.is_admin():
        return error('无权访问', code=403, status_code=403)

    # 只返回 submitted 或 judging 状态的项目
    query = Project.query.filter(Project.status.in_(['submitted', 'teacher_review', 'judging', 'need_modify']))

    # 评委：排除自己已评审的项目（可选）
    if user.is_judge():
        reviewed_project_ids = db.session.query(Review.project_id).filter_by(judge_id=user.id).all()
        reviewed_project_ids = [r[0] for r in reviewed_project_ids]
        if reviewed_project_ids:
            query = query.filter(~Project.id.in_(reviewed_project_ids))

    projects = query.order_by(Project.created_at.desc()).all()

    return success({
        'projects': [p.to_dict() for p in projects],
        'total': len(projects)
    })


@review_bp.route('/reviews/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_for_review(project_id):
    """获取项目评审详情"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    if not user.is_judge() and not user.is_admin():
        return error('无权访问', code=403, status_code=403)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 获取关联数据
    members = ProjectMember.query.filter_by(project_id=project.id).all()
    files = ProjectFile.query.filter_by(project_id=project.id).all()
    tasks = ProjectTask.query.filter_by(project_id=project.id).all()

    # 获取当前评委的评审记录
    my_review = Review.query.filter_by(project_id=project.id, judge_id=user.id).first()

    result = project.to_dict()
    result['members'] = [m.to_dict() for m in members]
    result['files'] = [f.to_dict() for f in files]
    result['tasks'] = [t.to_dict() for t in tasks]
    result['my_review'] = my_review.to_dict() if my_review else None

    return success({
        'project': result
    })


@review_bp.route('/reviews/projects/<int:project_id>', methods=['POST'])
@jwt_required()
def submit_review(project_id):
    """提交评审"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    if not user.is_judge() and not user.is_admin():
        return error('只有评委可以评审', code=403, status_code=403)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 检查项目状态
    if project.status not in ['submitted', 'teacher_review', 'judging', 'need_modify', 'passed', 'rejected']:
        return error(f'当前项目状态为 {project.status}，无法评审', code=403, status_code=403)

    data = request.get_json()
    if not data:
        return error('请求数据不能为空', code=400, status_code=400)

    # 获取各项评分
    scores = {
        'innovation_score': data.get('innovation_score', 0),
        'feasibility_score': data.get('feasibility_score', 0),
        'market_score': data.get('market_score', 0),
        'team_score': data.get('team_score', 0),
        'business_score': data.get('business_score', 0),
        'technology_score': data.get('technology_score', 0),
        'presentation_score': data.get('presentation_score', 0)
    }

    # 验证评分范围 0-100
    for key, value in scores.items():
        try:
            scores[key] = float(value)
            if scores[key] < 0 or scores[key] > 100:
                return error(f'{key} 评分必须在 0-100 之间', code=400, status_code=400)
        except (ValueError, TypeError):
            scores[key] = 0

    # 计算总分
    total_score = round(sum(scores.values()) / len(scores), 2)

    # 检查是否已评审过
    existing_review = Review.query.filter_by(project_id=project_id, judge_id=user.id).first()

    if existing_review:
        # 更新评审
        for key, value in scores.items():
            setattr(existing_review, key, value)
        existing_review.total_score = total_score
        existing_review.comment = data.get('comment', '').strip() or None
    else:
        # 创建新评审
        review = Review(
            project_id=project_id,
            judge_id=user.id,
            **scores,
            total_score=total_score,
            comment=data.get('comment', '').strip() or None
        )
        db.session.add(review)

    # 如果项目状态是 submitted 或 need_modify，改为 judging
    if project.status in ['submitted', 'teacher_review', 'need_modify']:
        project.status = 'judging'

    db.session.commit()

    # 检查是否所有评委都已评审，更新项目状态
    all_reviews = Review.query.filter_by(project_id=project_id).all()
    if all_reviews:
        avg_score = round(sum(r.total_score for r in all_reviews) / len(all_reviews), 2)
        # 简单规则：平均分 >= 60 通过，否则驳回
        if len(all_reviews) >= 1:  # 至少一个评委评审
            if avg_score >= 60:
                project.status = 'passed'
            else:
                project.status = 'rejected'
        db.session.commit()

    return success({
        'review': {
            **scores,
            'total_score': total_score,
            'comment': data.get('comment', '').strip() or None
        }
    }, message='评审提交成功')


@review_bp.route('/projects/<int:project_id>/reviews', methods=['GET'])
@jwt_required()
def get_project_reviews(project_id):
    """获取项目的评审结果"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    # 权限检查
    if not _check_project_access(project, user):
        return error('无权查看', code=403, status_code=403)

    # 学生只能查看已通过/已驳回项目的评审结果
    if user.is_student() and project.leader_id == user.id:
        if project.status not in ['passed', 'rejected', 'judging']:
            return error('评审尚未完成', code=403, status_code=403)

    reviews = Review.query.filter_by(project_id=project_id).all()

    # 获取评委信息
    result = []
    for review in reviews:
        review_dict = review.to_dict()
        judge = User.query.get(review.judge_id)
        review_dict['judge'] = {
            'id': judge.id,
            'username': judge.username,
            'real_name': judge.real_name
        } if judge else None
        result.append(review_dict)

    # 计算平均分
    avg_score = None
    if reviews:
        avg_score = round(sum(r.total_score for r in reviews) / len(reviews), 2)

    return success({
        'reviews': result,
        'total': len(result),
        'average_score': avg_score
    })


@review_bp.route('/reviews/my', methods=['GET'])
@jwt_required()
def get_my_reviews():
    """获取当前评委的评审记录"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    reviews = Review.query.filter_by(judge_id=user.id).order_by(Review.created_at.desc()).all()

    result = []
    for review in reviews:
        review_dict = review.to_dict()
        project = Project.query.get(review.project_id)
        review_dict['project'] = project.to_dict() if project else None
        result.append(review_dict)

    return success({
        'reviews': result,
        'total': len(result)
    })


@review_bp.route('/reviews/all', methods=['GET'])
@jwt_required()
def get_all_reviews():
    from utils.decorators import require_roles
    user = _get_current_user()
    if not user or not user.is_admin():
        return error('权限不足', code=403, status_code=403)

    reviews = Review.query.order_by(Review.created_at.desc()).all()
    result = []
    for review in reviews:
        review_dict = review.to_dict()
        project = Project.query.get(review.project_id)
        review_dict['project'] = project.to_dict() if project else None
        judge = User.query.get(review.judge_id)
        review_dict['judge_name'] = judge.real_name or judge.username if judge else '未知'
        result.append(review_dict)

    return success({
        'reviews': result,
        'total': len(result)
    })
