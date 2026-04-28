from flask import Blueprint, jsonify

task_bp = Blueprint('task', __name__)


@task_bp.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'message': '任务列表接口'}), 200


@task_bp.route('/', methods=['POST'])
def create_task():
    return jsonify({'message': '创建任务接口'}), 200
