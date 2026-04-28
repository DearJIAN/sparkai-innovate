from flask import Blueprint, jsonify

team_bp = Blueprint('team', __name__)


@team_bp.route('/', methods=['GET'])
def get_teams():
    return jsonify({'message': '团队列表接口'}), 200


@team_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    return jsonify({'message': f'团队详情接口 {team_id}'}), 200
