from flask import jsonify


def success(data=None, message='操作成功', code=200):
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return jsonify(response), code


def error(message='操作失败', code=400, status_code=400):
    response = {
        'code': code,
        'message': message,
        'data': None
    }
    return jsonify(response), status_code
