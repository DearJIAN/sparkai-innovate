from flask import Blueprint
from sqlalchemy import func
from models.user import User
from models.project import Project
from models.project_file import ProjectFile
from models.review import Review
from models.ai_record import AiRecord
from models.competition import Competition
from extensions import db
from flask_jwt_extended import jwt_required
from utils.decorators import require_roles
from utils.response import success, error

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_stats():
    """获取管理员看板统计数据"""
    # 用户统计
    total_users = User.query.count()
    user_by_role = db.session.query(User.role, func.count(User.id)).group_by(User.role).all()
    user_role_stats = {r[0]: r[1] for r in user_by_role}

    # 项目统计
    total_projects = Project.query.count()
    submitted_projects = Project.query.filter(Project.status.in_(['submitted', 'teacher_review', 'judging'])).count()
    passed_projects = Project.query.filter_by(status='passed').count()
    rejected_projects = Project.query.filter_by(status='rejected').count()
    need_modify_projects = Project.query.filter_by(status='need_modify').count()
    draft_projects = Project.query.filter_by(status='draft').count()

    # 项目阶段分布
    stage_stats = db.session.query(Project.stage, func.count(Project.id)).group_by(Project.stage).all()
    stage_distribution = {s[0]: s[1] for s in stage_stats}

    # 项目赛道分布
    track_stats = db.session.query(Project.track, func.count(Project.id)).group_by(Project.track).all()
    track_distribution = {t[0] or '未分类': t[1] for t in track_stats}

    # 文件统计
    total_files = ProjectFile.query.count()

    # 评审统计
    total_reviews = Review.query.count()

    # 比赛统计
    total_competitions = Competition.query.count()
    active_competitions = Competition.query.filter_by(status='active').count()

    # AI 使用统计
    total_ai_records = AiRecord.query.count()

    return success({
        'users': {
            'total': total_users,
            'by_role': user_role_stats
        },
        'projects': {
            'total': total_projects,
            'draft': draft_projects,
            'submitted': submitted_projects,
            'passed': passed_projects,
            'rejected': rejected_projects,
            'need_modify': need_modify_projects,
            'by_stage': stage_distribution,
            'by_track': track_distribution
        },
        'files': total_files,
        'reviews': total_reviews,
        'competitions': {
            'total': total_competitions,
            'active': active_competitions
        },
        'ai_records': total_ai_records
    })


@dashboard_bp.route('/recent', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_recent():
    """获取最近的数据"""
    # 最近创建的项目
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()

    # 最近上传的文件
    recent_files = ProjectFile.query.order_by(ProjectFile.created_at.desc()).limit(5).all()
    for f in recent_files:
        f.uploader_name = User.query.get(f.uploader_id).real_name or User.query.get(f.uploader_id).username

    # 最近的评审
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
    for r in recent_reviews:
        r.project_name = Project.query.get(r.project_id).name
        r.judge_name = User.query.get(r.judge_id).real_name or User.query.get(r.judge_id).username

    return success({
        'projects': [p.to_dict() for p in recent_projects],
        'files': [{
            'id': f.id,
            'original_name': f.original_name,
            'project_id': f.project_id,
            'uploader_name': f.uploader_name,
            'created_at': f.created_at.isoformat() if f.created_at else None
        } for f in recent_files],
        'reviews': [{
            'id': r.id,
            'project_id': r.project_id,
            'project_name': r.project_name,
            'judge_name': r.judge_name,
            'total_score': r.total_score,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in recent_reviews]
    })
