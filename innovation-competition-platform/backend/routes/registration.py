from flask import Blueprint, request
from datetime import datetime
from models.competition import Competition
from models.competition_track import CompetitionTrack
from models.competition_registration import CompetitionRegistration
from models.registration_member import RegistrationMember
from models.registration_material import RegistrationMaterial
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import require_roles
from utils.response import success, error

registration_bp = Blueprint('registration', __name__)

REGISTRATION_STATUS = ['draft', 'submitted', 'approved', 'rejected', 'withdrawn']


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


# ==================== 学生报名接口 ====================

@registration_bp.route('/registrations', methods=['POST'])
@jwt_required()
@require_roles('student')
def create_registration():
    """创建报名草稿"""
    user = _get_current_user()
    data = request.get_json()

    if not data or not data.get('competition_id') or not data.get('track_id'):
        return error('竞赛ID和赛道ID不能为空', code=400, status_code=400)

    competition = Competition.query.get(data['competition_id'])
    if not competition:
        return error('竞赛不存在', code=404, status_code=404)

    track = CompetitionTrack.query.get(data['track_id'])
    if not track:
        return error('赛道不存在', code=404, status_code=404)

    # 检查是否已报名
    existing = CompetitionRegistration.query.filter_by(
        competition_id=data['competition_id'],
        leader_id=user.id
    ).first()
    if existing:
        return error('您已报名该竞赛', code=400, status_code=400)

    registration = CompetitionRegistration(
        competition_id=data['competition_id'],
        track_id=data['track_id'],
        project_id=data.get('project_id'),
        leader_id=user.id,
        team_name=data.get('team_name', ''),
        school=data.get('school', ''),
        college=data.get('college', ''),
        major=data.get('major', ''),
        teacher_name=data.get('teacher_name', ''),
        teacher_phone=data.get('teacher_phone', ''),
        contact_phone=data.get('contact_phone', ''),
        contact_email=data.get('contact_email', ''),
        status='draft'
    )

    db.session.add(registration)
    db.session.commit()

    return success({
        'registration': registration.to_dict()
    }, message='报名草稿创建成功', code=201)


@registration_bp.route('/registrations/<int:registration_id>', methods=['GET'])
@jwt_required()
@require_roles('student')
def get_registration(registration_id):
    """查看报名详情"""
    user = _get_current_user()
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.leader_id != user.id:
        return error('无权查看该报名', code=403, status_code=403)

    return success(registration.to_detail_dict())


@registration_bp.route('/registrations/<int:registration_id>', methods=['PUT'])
@jwt_required()
@require_roles('student')
def update_registration(registration_id):
    """更新报名信息"""
    user = _get_current_user()
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.leader_id != user.id:
        return error('无权修改该报名', code=403, status_code=403)

    if registration.status == 'submitted':
        return error('已提交的报名不能修改', code=400, status_code=400)

    data = request.get_json()

    if 'track_id' in data:
        registration.track_id = data['track_id']
    if 'project_id' in data:
        registration.project_id = data['project_id']
    if 'team_name' in data:
        registration.team_name = data['team_name']
    if 'school' in data:
        registration.school = data['school']
    if 'college' in data:
        registration.college = data['college']
    if 'major' in data:
        registration.major = data['major']
    if 'teacher_name' in data:
        registration.teacher_name = data['teacher_name']
    if 'teacher_phone' in data:
        registration.teacher_phone = data['teacher_phone']
    if 'contact_phone' in data:
        registration.contact_phone = data['contact_phone']
    if 'contact_email' in data:
        registration.contact_email = data['contact_email']

    db.session.commit()

    return success({
        'registration': registration.to_dict()
    }, message='报名信息更新成功')


@registration_bp.route('/registrations/<int:registration_id>/members', methods=['POST'])
@jwt_required()
@require_roles('student')
def add_member(registration_id):
    """添加队员"""
    user = _get_current_user()
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    data = request.get_json()
    if not data or not data.get('name'):
        return error('队员姓名不能为空', code=400, status_code=400)

    member = RegistrationMember(
        registration_id=registration_id,
        name=data.get('name', '').strip(),
        student_no=data.get('student_no', '').strip() or None,
        college=data.get('college', '').strip() or None,
        major=data.get('major', '').strip() or None,
        phone=data.get('phone', '').strip() or None,
        email=data.get('email', '').strip() or None,
        role_in_team=data.get('role_in_team', 'member')
    )

    db.session.add(member)
    db.session.commit()

    return success({
        'member': member.to_dict()
    }, message='队员添加成功', code=201)


@registration_bp.route('/registration-members/<int:member_id>', methods=['PUT'])
@jwt_required()
@require_roles('student')
def update_member(member_id):
    """编辑队员"""
    user = _get_current_user()
    member = RegistrationMember.query.get(member_id)

    if not member:
        return error('队员不存在', code=404, status_code=404)

    registration = CompetitionRegistration.query.get(member.registration_id)
    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    data = request.get_json()

    if 'name' in data:
        member.name = data['name']
    if 'student_no' in data:
        member.student_no = data['student_no']
    if 'college' in data:
        member.college = data['college']
    if 'major' in data:
        member.major = data['major']
    if 'phone' in data:
        member.phone = data['phone']
    if 'email' in data:
        member.email = data['email']
    if 'role_in_team' in data:
        member.role_in_team = data['role_in_team']

    db.session.commit()

    return success({
        'member': member.to_dict()
    }, message='队员信息更新成功')


@registration_bp.route('/registration-members/<int:member_id>', methods=['DELETE'])
@jwt_required()
@require_roles('student')
def delete_member(member_id):
    """删除队员"""
    user = _get_current_user()
    member = RegistrationMember.query.get(member_id)

    if not member:
        return error('队员不存在', code=404, status_code=404)

    registration = CompetitionRegistration.query.get(member.registration_id)
    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    db.session.delete(member)
    db.session.commit()

    return success(message='队员删除成功')


@registration_bp.route('/registrations/<int:registration_id>/materials', methods=['POST'])
@jwt_required()
@require_roles('student')
def upload_material(registration_id):
    """上传报名材料"""
    import os
    import uuid
    import werkzeug
    from flask import current_app

    user = _get_current_user()
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    if 'file' not in request.files:
        return error('没有文件被上传', code=400, status_code=400)
        
    file = request.files['file']
    if file.filename == '':
        return error('没有选择文件', code=400, status_code=400)

    material_type = request.form.get('material_type')
    if not material_type:
        return error('材料类型不能为空', code=400, status_code=400)

    # 安全处理文件名
    original_name = file.filename
    safe_name = werkzeug.utils.secure_filename(original_name)
    if not safe_name or safe_name.startswith('.'):
        safe_name = original_name.replace('/', '_').replace('\\', '_').replace('..', '_')
    ext = safe_name.rsplit('.', 1)[1].lower() if '.' in safe_name else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else f"{uuid.uuid4().hex}"

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    reg_folder = os.path.join(upload_folder, f'registration_{registration_id}')
    os.makedirs(reg_folder, exist_ok=True)
    
    file_path = os.path.join(reg_folder, unique_name)
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    material = RegistrationMaterial(
        registration_id=registration_id,
        uploader_id=user.id,
        material_type=material_type,
        file_name=unique_name,
        original_name=original_name,
        file_path=file_path,
        file_type=ext,
        file_size=file_size
    )

    db.session.add(material)
    db.session.commit()

    return success({
        'material': material.to_dict()
    }, message='材料上传成功', code=201)


@registration_bp.route('/registration-materials/<int:material_id>', methods=['DELETE'])
@jwt_required()
@require_roles('student')
def delete_material(material_id):
    """删除报名材料"""
    user = _get_current_user()
    material = RegistrationMaterial.query.get(material_id)

    if not material:
        return error('材料不存在', code=404, status_code=404)

    registration = CompetitionRegistration.query.get(material.registration_id)
    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    db.session.delete(material)
    db.session.commit()

    return success(message='材料删除成功')


@registration_bp.route('/registrations/<int:registration_id>/submit', methods=['POST'])
@jwt_required()
@require_roles('student')
def submit_registration(registration_id):
    """提交报名"""
    user = _get_current_user()
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.leader_id != user.id:
        return error('无权操作', code=403, status_code=403)

    if registration.status != 'draft':
        return error('只能提交草稿状态的报名', code=400, status_code=400)

    # 校验必填信息
    if not registration.team_name:
        return error('队伍名称不能为空', code=400, status_code=400)

    registration.status = 'submitted'
    registration.submitted_at = datetime.now()

    # 更新竞赛报名数
    competition = Competition.query.get(registration.competition_id)
    if competition:
        competition.registration_count = (competition.registration_count or 0) + 1

    db.session.commit()

    return success({
        'registration': registration.to_dict()
    }, message='报名提交成功')


@registration_bp.route('/my-registrations', methods=['GET'])
@jwt_required()
@require_roles('student')
def get_my_registrations():
    """查看我的报名"""
    user = _get_current_user()

    registrations = CompetitionRegistration.query.filter_by(
        leader_id=user.id
    ).order_by(CompetitionRegistration.created_at.desc()).all()

    result = []
    for r in registrations:
        d = r.to_dict()
        comp = Competition.query.get(r.competition_id)
        track = CompetitionTrack.query.get(r.track_id)
        d['competitionName'] = comp.name if comp else ''
        d['trackName'] = track.name if track else ''
        d['poster_url'] = comp.poster_url if comp else ''
        d['memberCount'] = r.members.count()
        d['materialCount'] = r.materials.count()
        d['createdAt'] = d['created_at'].split('T')[0] if d['created_at'] else ''
        result.append(d)

    return success({
        'registrations': result
    })


# ==================== 管理员接口 ====================

@registration_bp.route('/admin/registrations', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_admin_registrations():
    """获取所有报名记录"""
    competition_id = request.args.get('competition_id', type=int)
    status = request.args.get('status', '').strip()
    keyword = request.args.get('keyword', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    query = CompetitionRegistration.query

    if competition_id:
        query = query.filter_by(competition_id=competition_id)

    if status:
        query = query.filter_by(status=status)

    if keyword:
        query = query.filter(
            db.or_(
                CompetitionRegistration.team_name.contains(keyword),
                CompetitionRegistration.school.contains(keyword)
            )
        )

    pagination = query.order_by(CompetitionRegistration.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    registrations = pagination.items
    result = []
    for r in registrations:
        d = r.to_detail_dict()
        comp = Competition.query.get(r.competition_id)
        track = CompetitionTrack.query.get(r.track_id)
        d['competitionName'] = comp.name if comp else ''
        d['trackName'] = track.name if track else ''
        d['leaderName'] = d['leader']['name'] if d.get('leader') else ''
        d['memberCount'] = len(d.get('members', []))
        d['materialCount'] = len(d.get('materials', []))
        d['submittedAt'] = d['submitted_at'].split('T')[0] if d.get('submitted_at') else ''
        result.append(d)

    return success({
        'registrations': result,
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@registration_bp.route('/admin/registrations/<int:registration_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_admin_registration_detail(registration_id):
    """查看报名详情（管理员）"""
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    return success(registration.to_detail_dict())


@registration_bp.route('/admin/registrations/<int:registration_id>/approve', methods=['POST'])
@jwt_required()
@require_roles('admin')
def approve_registration(registration_id):
    """审核通过报名"""
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.status != 'submitted':
        return error('只能审核已提交的报名', code=400, status_code=400)

    registration.status = 'approved'
    db.session.commit()

    return success({
        'registration': registration.to_dict()
    }, message='报名审核通过')


@registration_bp.route('/admin/registrations/<int:registration_id>/reject', methods=['POST'])
@jwt_required()
@require_roles('admin')
def reject_registration(registration_id):
    """驳回报名"""
    registration = CompetitionRegistration.query.get(registration_id)

    if not registration:
        return error('报名记录不存在', code=404, status_code=404)

    if registration.status != 'submitted':
        return error('只能审核已提交的报名', code=400, status_code=400)

    data = request.get_json()
    remark = data.get('remark', '') if data else ''

    registration.status = 'rejected'
    registration.remark = remark
    db.session.commit()

    return success({
        'registration': registration.to_dict()
    }, message='报名已驳回')


@registration_bp.route('/admin/registrations/statistics', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_registration_statistics():
    """报名统计数据"""
    total = CompetitionRegistration.query.count()
    draft = CompetitionRegistration.query.filter_by(status='draft').count()
    submitted = CompetitionRegistration.query.filter_by(status='submitted').count()
    approved = CompetitionRegistration.query.filter_by(status='approved').count()
    rejected = CompetitionRegistration.query.filter_by(status='rejected').count()

    return success({
        'total': total,
        'draft': draft,
        'submitted': submitted,
        'approved': approved,
        'rejected': rejected
    })
