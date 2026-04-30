from flask import Blueprint, request
from datetime import datetime
from models.competition import Competition
from models.competition_track import CompetitionTrack
from models.competition_registration import CompetitionRegistration
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import require_roles
from utils.response import success, error

competition_bp = Blueprint('competition', __name__)

COMPETITION_STATUS = ['draft', 'active', 'ended', 'archived']


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


# ==================== 管理员接口 ====================

@competition_bp.route('/competitions', methods=['GET'])
@jwt_required()
def get_competitions():
    """获取比赛列表（管理员）"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    status = request.args.get('status', '').strip()

    query = Competition.query
    if status:
        query = query.filter_by(status=status)

    competitions = query.order_by(Competition.created_at.desc()).all()

    return success({
        'competitions': [c.to_dict() for c in competitions],
        'total': len(competitions)
    })


@competition_bp.route('/competitions', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_competition():
    """创建比赛"""
    data = request.get_json()
    if not data or not data.get('name'):
        return error('比赛名称不能为空', code=400, status_code=400)

    start_time = None
    end_time = None
    if data.get('start_time'):
        try:
            start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00').replace('+00:00', ''))
        except ValueError:
            pass
    if data.get('end_time'):
        try:
            end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00').replace('+00:00', ''))
        except ValueError:
            pass

    competition = Competition(
        name=data.get('name', '').strip(),
        description=data.get('description', '').strip() or None,
        start_time=start_time,
        end_time=end_time,
        status=data.get('status', 'draft')
    )

    db.session.add(competition)
    db.session.commit()

    return success({
        'competition': competition.to_dict()
    }, message='比赛创建成功', code=201)


@competition_bp.route('/competitions/<int:competition_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_competition(competition_id):
    """更新比赛"""
    competition = Competition.query.get(competition_id)
    if not competition:
        return error('比赛不存在', code=404, status_code=404)

    data = request.get_json()

    if 'name' in data:
        competition.name = data['name'].strip()
    if 'description' in data:
        competition.description = data['description'].strip() or None
    if 'status' in data and data['status'] in COMPETITION_STATUS:
        competition.status = data['status']
    if 'start_time' in data:
        if data['start_time']:
            try:
                competition.start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00').replace('+00:00', ''))
            except ValueError:
                pass
        else:
            competition.start_time = None
    if 'end_time' in data:
        if data['end_time']:
            try:
                competition.end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00').replace('+00:00', ''))
            except ValueError:
                pass
        else:
            competition.end_time = None

    db.session.commit()

    return success({
        'competition': competition.to_dict()
    }, message='比赛更新成功')


@competition_bp.route('/competitions/<int:competition_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_competition(competition_id):
    """删除比赛"""
    competition = Competition.query.get(competition_id)
    if not competition:
        return error('比赛不存在', code=404, status_code=404)

    db.session.delete(competition)
    db.session.commit()

    return success(message='比赛删除成功')


# ==================== 公开接口（竞赛广场） ====================

@competition_bp.route('/public/competitions', methods=['GET'])
def get_public_competitions():
    """获取可报名竞赛列表（公开接口）"""

    keyword = request.args.get('keyword', '').strip()
    category = request.args.get('category', '').strip()
    level = request.args.get('level', '').strip()
    status = request.args.get('status', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    query = Competition.query.filter(Competition.status.in_(['active', 'ended']))

    if keyword:
        query = query.filter(
            db.or_(
                Competition.name.contains(keyword),
                Competition.organizer.contains(keyword)
            )
        )

    if category:
        query = query.filter_by(category=category)

    if level:
        query = query.filter_by(level=level)

    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Competition.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    competitions = pagination.items

    return success({
        'competitions': [c.to_dict() for c in competitions],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@competition_bp.route('/public/competitions/<int:competition_id>', methods=['GET'])
def get_public_competition_detail(competition_id):
    """获取竞赛详情（公开接口）"""
    competition = Competition.query.get(competition_id)
    if not competition:
        return error('竞赛不存在', code=404, status_code=404)

    # 增加浏览量
    competition.view_count = (competition.view_count or 0) + 1
    db.session.commit()

    data = competition.to_dict()
    data['tracks'] = [t.to_dict() for t in competition.tracks]
    data['has_registered'] = False

    return success(data)


@competition_bp.route('/public/competitions/<int:competition_id>/tracks', methods=['GET'])
def get_competition_tracks(competition_id):
    """获取比赛赛道列表"""
    competition = Competition.query.get(competition_id)
    if not competition:
        return error('竞赛不存在', code=404, status_code=404)

    tracks = competition.tracks.all()

    return success({
        'tracks': [t.to_dict() for t in tracks]
    })


@competition_bp.route('/public/competition-categories', methods=['GET'])
def get_competition_categories():
    """返回竞赛分类"""
    categories = [
        '创新创业',
        '人工智能',
        '数字经济',
        '乡村振兴',
        '电子商务',
        '软件开发',
        '智能制造',
        '职业规划',
        '公益实践',
        '产业命题'
    ]

    return success({
        'categories': categories
    })


# ==================== 赛道管理接口（管理员） ====================

@competition_bp.route('/competitions/<int:competition_id>/tracks', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_track(competition_id):
    """创建赛道"""
    competition = Competition.query.get(competition_id)
    if not competition:
        return error('竞赛不存在', code=404, status_code=404)

    data = request.get_json()
    if not data or not data.get('name'):
        return error('赛道名称不能为空', code=400, status_code=400)

    track = CompetitionTrack(
        competition_id=competition_id,
        name=data.get('name', '').strip(),
        description=data.get('description', '').strip() or None,
        category=data.get('category', '').strip() or None,
        team_min=data.get('team_min', 1),
        team_max=data.get('team_max', 5),
        material_requirements=data.get('material_requirements', '').strip() or None,
        status=data.get('status', 'open')
    )

    db.session.add(track)
    db.session.commit()

    return success({
        'track': track.to_dict()
    }, message='赛道创建成功', code=201)
