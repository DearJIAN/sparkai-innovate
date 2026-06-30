import os
import json
import logging
from datetime import datetime

from flask import Blueprint, request
from models.user import User
from models.project import Project
from models.project_file import ProjectFile
from models.project_member import ProjectMember
from models.registration_material import RegistrationMaterial
from models.competition_registration import CompetitionRegistration
from models.competition import Competition
from models.agent_task import AgentTask
from models.agent_material_index import AgentMaterialIndex
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error
from utils.decorators import require_min_role, require_roles
from services.document_parser import parse_project_files, parse_registration_materials
from services.vector_store import index_documents, search_documents, index_exists, get_index_info
from services.ai_prompt_service import (
    material_qa as _material_qa,
    bp_check as _bp_check,
    roadshow_generate as _roadshow_generate,
    review_assist as _review_assist,
    competition_recommend as _competition_recommend,
    smart_navigate as _smart_navigate,
    project_idea_generate as _project_idea_generate,
    mock_defense as _mock_defense,
    batch_review_assist as _batch_review_assist,
    smart_feedback_generate as _smart_feedback_generate,
    review_draft_generate as _review_draft_generate,
    score_consistency_check as _score_consistency_check,
)

logger = logging.getLogger(__name__)

agent_bp = Blueprint('agent', __name__)


def _get_current_user():
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def _get_upload_folder():
    return os.environ.get('UPLOAD_FOLDER') or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'uploads'
    )


def _check_project_access(project, user):
    if user.role == 'admin':
        return True
    if project.leader_id == user.id:
        return True
    if hasattr(project, 'teacher_id') and project.teacher_id == user.id:
        return True
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    if user.role == 'judge' and project.status != 'draft':
        return True
    return False


def _check_capability_access(user, capability, project=None):
    if user.role == 'admin':
        return True, None

    if capability == 'review_assist':
        if user.role not in ('teacher', 'judge', 'admin'):
            return False, '评审辅助仅限教师、评委和管理员使用'
        if project and user.role == 'judge' and project.status == 'draft':
            return False, '评委不能评审草稿状态的项目'

    if capability == 'competition_recommend':
        if user.role not in ('student', 'admin'):
            return False, '智能竞赛推荐仅限学生使用'

    if capability == 'roadshow':
        if user.role == 'judge':
            return False, '评委无法使用路演稿生成'

    if capability == 'project_idea':
        if user.role not in ('student', 'admin'):
            return False, '项目创意生成仅限学生使用'

    if capability == 'mock_defense':
        if user.role not in ('student', 'teacher', 'admin'):
            return False, '模拟路演答辩仅限学生和教师使用'

    if project and not _check_project_access(project, user):
        return False, '您没有权限访问该项目'

    return True, None


def _create_task(user_id, capability, input_params, project_id=None, registration_id=None):
    task = AgentTask(
        user_id=user_id,
        project_id=project_id,
        registration_id=registration_id,
        capability=capability,
        input_params=json.dumps(input_params, ensure_ascii=False) if input_params else None,
        status='pending',
    )
    db.session.add(task)
    db.session.commit()
    return task


def _complete_task(task, result, error_msg=None):
    task.status = 'completed' if not error_msg else 'failed'
    task.result = result if not error_msg else None
    task.error_message = error_msg
    task.completed_at = datetime.now()
    db.session.commit()


def _get_project_info_text(project):
    if not project:
        return ''
    parts = []
    if project.name:
        parts.append(f'项目名称：{project.name}')
    if project.description:
        parts.append(f'项目描述：{project.description}')
    if hasattr(project, 'category') and project.category:
        parts.append(f'项目类别：{project.category}')
    if hasattr(project, 'innovation_point') and project.innovation_point:
        parts.append(f'创新点：{project.innovation_point}')
    if hasattr(project, 'target_market') and project.target_market:
        parts.append(f'目标市场：{project.target_market}')
    return '\n'.join(parts)


@agent_bp.route('/index-materials', methods=['POST'])
@jwt_required()
def index_materials():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    source_type = data.get('source_type', 'project')
    force_reindex = data.get('force_reindex', False)

    if source_type not in ('project', 'registration'):
        return error('source_type 必须为 project 或 registration')

    project_id = data.get('project_id')
    registration_id = data.get('registration_id')

    if source_type == 'project':
        if not project_id:
            return error('参数缺失：project_id')
        project = Project.query.get(project_id)
        if not project:
            return error('项目不存在', code=404, status_code=404)
        if not _check_project_access(project, user):
            return error('您没有权限访问该项目', code=403, status_code=403)

        files = ProjectFile.query.filter_by(project_id=project_id).all()
        if not files:
            return error('该项目暂无上传文件')

        parsed_results = parse_project_files(files, _get_upload_folder())

        source_id = project_id
        index_info = get_index_info('project', source_id)

        if index_info['exists'] and not force_reindex:
            return success({
                'indexed_files': sum(1 for r in parsed_results if r['status'] == 'success'),
                'skipped_files': sum(1 for r in parsed_results if r['status'] != 'success'),
                'skipped_details': [{'file_name': r['file_name'], 'reason': r['reason']} for r in parsed_results if r['status'] != 'success'],
                'engine': index_info.get('engine', 'unknown'),
                'message': '索引已存在，如需重新索引请设置 force_reindex=true',
            })

        result = index_documents('project', source_id, parsed_results)

    elif source_type == 'registration':
        if not registration_id:
            return error('参数缺失：registration_id')
        registration = CompetitionRegistration.query.get(registration_id)
        if not registration:
            return error('报名记录不存在', code=404, status_code=404)

        materials = RegistrationMaterial.query.filter_by(registration_id=registration_id).all()
        if not materials:
            return error('该报名暂无上传材料')

        parsed_results = parse_registration_materials(materials, _get_upload_folder())

        source_id = registration_id
        index_info = get_index_info('registration', source_id)

        if index_info['exists'] and not force_reindex:
            return success({
                'indexed_files': sum(1 for r in parsed_results if r['status'] == 'success'),
                'skipped_files': sum(1 for r in parsed_results if r['status'] != 'success'),
                'skipped_details': [{'file_name': r['file_name'], 'reason': r['reason']} for r in parsed_results if r['status'] != 'success'],
                'engine': index_info.get('engine', 'unknown'),
                'message': '索引已存在，如需重新索引请设置 force_reindex=true',
            })

        result = index_documents('registration', source_id, parsed_results)

    if result['success']:
        for r_parsed in parsed_results:
            if r_parsed['status'] == 'success':
                existing = AgentMaterialIndex.query.filter_by(
                    source_type=source_type,
                    source_id=r_parsed['file_id'],
                ).first()
                if existing:
                    existing.status = 'indexed'
                    existing.indexed_at = datetime.now()
                    existing.index_path = result.get('index_path', '')
                else:
                    db.session.add(AgentMaterialIndex(
                        source_type=source_type,
                        source_id=r_parsed['file_id'],
                        project_id=project_id if source_type == 'project' else None,
                        registration_id=registration_id if source_type == 'registration' else None,
                        status='indexed',
                        index_path=result.get('index_path', ''),
                        indexed_at=datetime.now(),
                    ))
        db.session.commit()

    return success({
        'indexed_files': result.get('indexed_chunks', 0),
        'skipped_files': len(result.get('skipped_details', [])),
        'skipped_details': result.get('skipped_details', []),
        'engine': result.get('engine', 'none'),
        'message': result.get('message', ''),
    })


@agent_bp.route('/material-qa', methods=['POST'])
@jwt_required()
def material_qa():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    question = data.get('question', '').strip()
    project_id = data.get('project_id')
    registration_id = data.get('registration_id')
    top_k = data.get('top_k', 4)

    if not question:
        return error('参数缺失：question')
    if not project_id and not registration_id:
        return error('参数缺失：project_id 或 registration_id')

    project = None
    if project_id:
        project = Project.query.get(project_id)
        if not project:
            return error('项目不存在', code=404, status_code=404)
        if not _check_project_access(project, user):
            return error('您没有权限访问该项目', code=403, status_code=403)

    allowed, msg = _check_capability_access(user, 'material_qa', project)
    if not allowed:
        return error(msg, code=403, status_code=403)

    task = _create_task(user.id, 'material_qa', data, project_id, registration_id)

    try:
        search_result = None
        if registration_id:
            if not index_exists('registration', registration_id):
                return error('该报名材料尚未建立索引，请先调用 /api/agent/index-materials', code=400)
            search_result = search_documents('registration', registration_id, question, top_k)
        elif project_id:
            if not index_exists('project', project_id):
                return error('该项目材料尚未建立索引，请先调用 /api/agent/index-materials', code=400)
            search_result = search_documents('project', project_id, question, top_k)

        project_info_text = _get_project_info_text(project)
        result = _material_qa(question, project, search_result, project_info_text)

        _complete_task(task, json.dumps(result, ensure_ascii=False))

        return success({
            'answer': result['answer'],
            'sources': result.get('sources', []),
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'材料问答失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'材料问答失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/bp-check', methods=['POST'])
@jwt_required()
def bp_check():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')
    registration_id = data.get('registration_id')

    if not project_id and not registration_id:
        return error('参数缺失：project_id 或 registration_id')

    project = None
    if project_id:
        project = Project.query.get(project_id)
        if not project:
            return error('项目不存在', code=404, status_code=404)
        if not _check_project_access(project, user):
            return error('您没有权限访问该项目', code=403, status_code=403)

    allowed, msg = _check_capability_access(user, 'bp_check', project)
    if not allowed:
        return error(msg, code=403, status_code=403)

    task = _create_task(user.id, 'bp_check', data, project_id, registration_id)

    try:
        search_result = None
        if registration_id:
            search_result = search_documents('registration', registration_id, '商业计划书 完整性 分析', 6)
        elif project_id:
            search_result = search_documents('project', project_id, '商业计划书 完整性 分析', 6)

        project_info_text = _get_project_info_text(project)
        result = _bp_check(project, search_result, project_info_text)

        _complete_task(task, json.dumps(result, ensure_ascii=False))

        return success({
            'report': result['report'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'商业计划书体检失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'商业计划书体检失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/roadshow', methods=['POST'])
@jwt_required()
def roadshow():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')
    duration = data.get('duration', 3)
    style = data.get('style', 'formal')

    if not project_id:
        return error('参数缺失：project_id')
    if duration not in (3, 5, 8):
        return error('duration 只支持 3、5 或 8')
    if style not in ('formal', 'passionate', 'concise', 'story'):
        return error('style 只支持 formal / passionate / concise / story')

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)
    if not _check_project_access(project, user):
        return error('您没有权限访问该项目', code=403, status_code=403)

    allowed, msg = _check_capability_access(user, 'roadshow', project)
    if not allowed:
        return error(msg, code=403, status_code=403)

    task = _create_task(user.id, 'roadshow', data, project_id)

    try:
        search_result = None
        if index_exists('project', project_id):
            search_result = search_documents('project', project_id, '路演 项目介绍 创新点 商业模式', 6)

        project_info_text = _get_project_info_text(project)
        result = _roadshow_generate(project, search_result, duration, style, project_info_text)

        _complete_task(task, json.dumps(result, ensure_ascii=False))

        return success({
            'script': result['script'],
            'word_count': result['word_count'],
            'estimated_minutes': result['estimated_minutes'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'路演稿生成失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'路演稿生成失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/review-assist', methods=['POST'])
@jwt_required()
@require_min_role('teacher')
def review_assist():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')

    if not project_id:
        return error('参数缺失：project_id')

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)
    if not _check_project_access(project, user):
        return error('您没有权限访问该项目', code=403, status_code=403)

    allowed, msg = _check_capability_access(user, 'review_assist', project)
    if not allowed:
        return error(msg, code=403, status_code=403)

    task = _create_task(user.id, 'review_assist', data, project_id)

    try:
        search_result = None
        if index_exists('project', project_id):
            search_result = search_documents('project', project_id, '评审 创新 可行性 市场 团队 商业', 6)

        project_info_text = _get_project_info_text(project)
        result = _review_assist(project, search_result, project_info_text)

        _complete_task(task, json.dumps(result, ensure_ascii=False))

        return success({
            'analysis': result['analysis'],
            'disclaimer': result['disclaimer'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'评审辅助失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'评审辅助失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/competition-recommend', methods=['POST'])
@jwt_required()
def competition_recommend():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')

    if not project_id:
        return error('参数缺失：project_id')

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)
    if not _check_project_access(project, user):
        return error('您没有权限访问该项目', code=403, status_code=403)

    allowed, msg = _check_capability_access(user, 'competition_recommend', project)
    if not allowed:
        return error(msg, code=403, status_code=403)

    task = _create_task(user.id, 'competition_recommend', data, project_id)

    try:
        competitions = Competition.query.filter(
            Competition.status.in_(['registration', 'upcoming', 'ongoing'])
        ).all()

        comp_data = []
        for comp in competitions:
            cd = {'name': comp.name}
            if comp.description:
                cd['description'] = comp.description
            if comp.category:
                cd['category'] = comp.category
            if comp.status:
                cd['status'] = comp.status
            if hasattr(comp, 'registration_start') and comp.registration_start:
                cd['registration_start'] = str(comp.registration_start)
            if hasattr(comp, 'registration_end') and comp.registration_end:
                cd['registration_end'] = str(comp.registration_end)
            tracks = Competition.query.filter_by(id=comp.id).first()
            if hasattr(tracks, 'tracks') and tracks.tracks:
                cd['tracks'] = tracks.tracks
            comp_data.append(cd)

        project_info_text = _get_project_info_text(project)
        result = _competition_recommend(project, comp_data, project_info_text)

        _complete_task(task, json.dumps(result, ensure_ascii=False))

        return success({
            'recommendation': result['recommendation'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'竞赛推荐失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'竞赛推荐失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    capability = request.args.get('capability')

    query = AgentTask.query.filter_by(user_id=user.id)
    if capability:
        query = query.filter_by(capability=capability)
    query = query.order_by(AgentTask.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'tasks': [t.to_dict() for t in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages,
    })


@agent_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    task = AgentTask.query.get(task_id)
    if not task:
        return error('任务不存在', code=404, status_code=404)

    if task.user_id != user.id and user.role != 'admin':
        return error('无权访问该任务', code=403, status_code=403)

    return success(task.to_dict())


@agent_bp.route('/navigate', methods=['POST'])
@jwt_required()
def smart_navigate():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return error('参数缺失：message')

    try:
        result = _smart_navigate(message, user.role)
        return success(result)
    except Exception as e:
        logger.error(f'智能引航失败: {e}')
        return error(f'智能引航失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/project-idea', methods=['POST'])
@jwt_required()
def project_idea():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    allowed, msg = _check_capability_access(user, 'project_idea')
    if not allowed:
        return error(msg, code=403, status_code=403)

    data = request.get_json()
    competition_name = data.get('competition_name', '')
    competition_category = data.get('competition_category', '')
    track = data.get('track', '')
    skills = data.get('skills', '')
    interests = data.get('interests', '')

    task = _create_task(user.id, 'project_idea', data)

    try:
        result = _project_idea_generate(competition_name, competition_category, track, skills, interests)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'ideas': result['ideas'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'项目创意生成失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'项目创意生成失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/mock-defense', methods=['POST'])
@jwt_required()
def mock_defense():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    allowed, msg = _check_capability_access(user, 'mock_defense')
    if not allowed:
        return error(msg, code=403, status_code=403)

    data = request.get_json()
    project_id = data.get('project_id')
    question_type = data.get('question_type', 'general')

    if question_type not in ('general', 'technical', 'business', 'tough'):
        return error('question_type 只支持 general / technical / business / tough')

    project = None
    search_result = None
    if project_id:
        project = Project.query.get(project_id)
        if not project:
            return error('项目不存在', code=404, status_code=404)
        if not _check_project_access(project, user):
            return error('您没有权限访问该项目', code=403, status_code=403)
        if index_exists('project', project_id):
            search_result = search_documents('project', project_id, '路演答辩 创新点 可行性 市场 团队', 6)

    task = _create_task(user.id, 'mock_defense', data, project_id)

    try:
        project_info_text = _get_project_info_text(project)
        result = _mock_defense(project, search_result, question_type, project_info_text)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'defense': result['defense'],
            'question_type': result['question_type'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'模拟答辩失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'模拟答辩失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/batch-review', methods=['POST'])
@jwt_required()
@require_min_role('teacher')
def batch_review():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_ids = data.get('project_ids', [])

    projects_info = []
    if project_ids:
        for pid in project_ids[:10]:
            p = Project.query.get(pid)
            if p and _check_project_access(p, user):
                projects_info.append({
                    'name': p.name,
                    'description': p.description or '',
                    'category': getattr(p, 'category', '') or '',
                    'status': p.status,
                    'leader': getattr(p, 'leader_id', ''),
                })
    else:
        if user.role == 'teacher':
            projects = Project.query.filter_by(teacher_id=user.id).limit(10).all()
        else:
            projects = Project.query.limit(10).all()
        for p in projects:
            projects_info.append({
                'name': p.name,
                'description': p.description or '',
                'category': getattr(p, 'category', '') or '',
                'status': p.status,
                'leader': getattr(p, 'leader_id', ''),
            })

    task = _create_task(user.id, 'batch_review', data)

    try:
        result = _batch_review_assist(projects_info)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'report': result['report'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'批量审核失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'批量审核失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/smart-feedback', methods=['POST'])
@jwt_required()
@require_min_role('teacher')
def smart_feedback():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')
    feedback_type = data.get('feedback_type', 'modify')

    if feedback_type not in ('modify', 'approve', 'reject'):
        return error('feedback_type 只支持 modify / approve / reject')
    if not project_id:
        return error('参数缺失：project_id')

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)
    if not _check_project_access(project, user):
        return error('您没有权限访问该项目', code=403, status_code=403)

    task = _create_task(user.id, 'smart_feedback', data, project_id)

    try:
        search_result = None
        if index_exists('project', project_id):
            search_result = search_documents('project', project_id, '审核 反馈 修改 建议', 4)
        project_info_text = _get_project_info_text(project)
        result = _smart_feedback_generate(project, search_result, feedback_type, project_info_text)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'feedback': result['feedback'],
            'feedback_type': result['feedback_type'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'智能反馈生成失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'智能反馈生成失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/review-draft', methods=['POST'])
@jwt_required()
@require_min_role('judge')
def review_draft():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    project_id = data.get('project_id')
    scoring_dimensions = data.get('scoring_dimensions')

    if not project_id:
        return error('参数缺失：project_id')

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)
    if not _check_project_access(project, user):
        return error('您没有权限访问该项目', code=403, status_code=403)

    task = _create_task(user.id, 'review_draft', data, project_id)

    try:
        search_result = None
        if index_exists('project', project_id):
            search_result = search_documents('project', project_id, '评审 创新 可行性 市场 团队 商业', 6)
        project_info_text = _get_project_info_text(project)
        result = _review_draft_generate(project, search_result, scoring_dimensions, project_info_text)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'draft': result['draft'],
            'dimensions': result['dimensions'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'评审意见草稿生成失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'评审意见草稿生成失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/score-check', methods=['POST'])
@jwt_required()
@require_min_role('judge')
def score_check():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    data = request.get_json()
    review_data = data.get('review_data')

    if not review_data:
        return error('参数缺失：review_data')

    task = _create_task(user.id, 'score_check', data)

    try:
        result = _score_consistency_check(review_data)
        _complete_task(task, json.dumps(result, ensure_ascii=False))
        return success({
            'report': result['report'],
            'is_fallback': result.get('is_fallback', False),
            'task_id': task.id,
        })
    except Exception as e:
        logger.error(f'评分一致性检查失败: {e}')
        _complete_task(task, None, str(e))
        return error(f'评分一致性检查失败: {str(e)[:200]}', code=500, status_code=500)


@agent_bp.route('/capabilities', methods=['GET'])
@jwt_required()
def get_capabilities():
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    all_capabilities = [
        {'key': 'material_qa', 'name': 'AI 材料问答', 'roles': ['student', 'teacher', 'judge', 'admin'], 'icon': 'Document', 'description': '基于项目材料进行智能问答'},
        {'key': 'bp_check', 'name': '商业计划书体检', 'roles': ['student', 'teacher', 'judge', 'admin'], 'icon': 'DataAnalysis', 'description': '检查商业计划书完整性和质量'},
        {'key': 'roadshow', 'name': '路演稿生成', 'roles': ['student', 'teacher', 'admin'], 'icon': 'Microphone', 'description': '生成结构化路演演讲稿'},
        {'key': 'review_assist', 'name': '评审辅助', 'roles': ['teacher', 'judge', 'admin'], 'icon': 'Star', 'description': '辅助评审人员了解项目全貌'},
        {'key': 'competition_recommend', 'name': '智能竞赛推荐', 'roles': ['student', 'admin'], 'icon': 'Trophy', 'description': '根据项目推荐适合的竞赛'},
        {'key': 'smart_navigate', 'name': '智能引航', 'roles': ['student', 'teacher', 'judge', 'admin'], 'icon': 'Compass', 'description': '模糊指令理解与页面跳转'},
        {'key': 'project_idea', 'name': '项目创意生成', 'roles': ['student', 'admin'], 'icon': 'MagicStick', 'description': '基于竞赛和技能生成项目创意'},
        {'key': 'mock_defense', 'name': '模拟路演答辩', 'roles': ['student', 'teacher', 'admin'], 'icon': 'ChatDotRound', 'description': 'AI扮演评委进行模拟答辩'},
        {'key': 'batch_review', 'name': '批量审核助手', 'roles': ['teacher', 'admin'], 'icon': 'List', 'description': '批量分析待审核项目'},
        {'key': 'smart_feedback', 'name': '智能反馈生成', 'roles': ['teacher', 'admin'], 'icon': 'EditPen', 'description': '生成项目审核反馈意见'},
        {'key': 'review_draft', 'name': '评审意见草稿', 'roles': ['judge', 'admin'], 'icon': 'DocumentCopy', 'description': '生成评审意见草稿'},
        {'key': 'score_check', 'name': '评分一致性检查', 'roles': ['judge', 'admin'], 'icon': 'Checked', 'description': '检查评分与评价是否一致'},
    ]

    user_capabilities = [c for c in all_capabilities if user.role in c['roles']]

    return success({
        'capabilities': user_capabilities,
        'role': user.role,
    })
