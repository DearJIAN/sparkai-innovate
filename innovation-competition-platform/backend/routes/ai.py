from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/generate-summary', methods=['POST'])
@jwt_required()
def generate_summary():
    data = request.get_json()
    project_name = data.get('project_name', '')
    
    # TODO: 接入 AI 模型
    summary = f"这是 {project_name} 的 AI 生成简介..."
    
    return jsonify({
        'summary': summary,
        'suggestions': [
            '建议完善市场调研部分',
            '商业模式需要更清晰的盈利路径',
            '技术实现方案较为可行'
        ]
    }), 200


@ai_bp.route('/risk-analysis', methods=['POST'])
@jwt_required()
def risk_analysis():
    data = request.get_json()
    project_name = data.get('project_name', '')
    
    # TODO: 接入 AI 模型
    return jsonify({
        'risks': [
            {'type': '市场风险', 'level': '中', 'description': '市场竞争激烈'},
            {'type': '技术风险', 'level': '低', 'description': '技术方案成熟'},
            {'type': '运营风险', 'level': '高', 'description': '团队缺乏运营经验'}
        ]
    }), 200
