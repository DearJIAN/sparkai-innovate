from flask import Blueprint, jsonify

material_bp = Blueprint('material', __name__)


@material_bp.route('/', methods=['GET'])
def get_materials():
    return jsonify({'message': '材料列表接口'}), 200


@material_bp.route('/upload', methods=['POST'])
def upload_material():
    return jsonify({'message': '材料上传接口'}), 200
