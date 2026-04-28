from flask import Blueprint, jsonify

review_bp = Blueprint('review', __name__)


@review_bp.route('/', methods=['GET'])
def get_reviews():
    return jsonify({'message': '评审列表接口'}), 200


@review_bp.route('/', methods=['POST'])
def create_review():
    return jsonify({'message': '创建评审接口'}), 200
