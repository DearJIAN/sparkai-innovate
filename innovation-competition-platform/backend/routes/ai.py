from flask import Blueprint, request
from models.user import User
from models.project import Project
from models.ai_record import AiRecord
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error
from services.ai_service import (
    generate_project_summary,
    generate_business_advice,
    generate_risk_analysis
)

ai_bp = Blueprint('ai', __name__)


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


@ai_bp.route('/project-summary', methods=['POST'])
@jwt_required()
def project_summary():
    """生成项目简介"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }

    # 调用 AI 服务
    result = generate_project_summary(project_info)

    # 记录 AI 使用
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='summary',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()

    return success({
        'result': result,
        'type': 'summary'
    })


@ai_bp.route('/business-plan-advice', methods=['POST'])
@jwt_required()
def business_plan_advice():
    """生成商业计划书建议"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }

    # 调用 AI 服务
    result = generate_business_advice(project_info)

    # 记录 AI 使用
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='business_advice',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()

    return success({
        'result': result,
        'type': 'business_advice'
    })


@ai_bp.route('/risk-analysis', methods=['POST'])
@jwt_required()
def risk_analysis():
    """生成风险分析"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_info = {
        'name': data.get('project_name', ''),
        'description': data.get('description', ''),
        'category': data.get('category', ''),
        'track': data.get('track', '')
    }

    # 调用 AI 服务
    result = generate_risk_analysis(project_info)

    # 记录 AI 使用
    record = AiRecord(
        user_id=user.id,
        project_id=data.get('project_id'),
        type='risk_analysis',
        prompt=str(project_info),
        result=result
    )
    db.session.add(record)
    db.session.commit()

    return success({
        'result': result,
        'type': 'risk_analysis'
    })


@ai_bp.route('/records', methods=['GET'])
@jwt_required()
def get_records():
    """获取当前用户的 AI 使用记录"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    records = AiRecord.query.filter_by(user_id=user.id).order_by(AiRecord.created_at.desc()).all()

    return success({
        'records': [r.to_dict() for r in records],
        'total': len(records)
    })
