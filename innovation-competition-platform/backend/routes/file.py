import os
import uuid
import werkzeug
from flask import Blueprint, request, send_from_directory, current_app
from models.project import Project
from models.project_member import ProjectMember
from models.project_file import ProjectFile
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error

file_bp = Blueprint('file', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    # 图片
    'jpg', 'jpeg', 'png', 'gif', 'webp',
    # 文档
    'doc', 'docx', 'pdf', 'txt',
    # PPT
    'ppt', 'pptx',
    # 表格
    'xls', 'xlsx',
    # 视频
    'mp4', 'mov', 'avi',
    # 压缩包
    'zip', 'rar'
}

# 文件类型映射
FILE_TYPE_MAP = {
    'jpg': 'image', 'jpeg': 'image', 'png': 'image', 'gif': 'image', 'webp': 'image',
    'doc': 'document', 'docx': 'document', 'pdf': 'document', 'txt': 'document',
    'ppt': 'ppt', 'pptx': 'ppt',
    'xls': 'spreadsheet', 'xlsx': 'spreadsheet',
    'mp4': 'video', 'mov': 'video', 'avi': 'video',
    'zip': 'archive', 'rar': 'archive'
}

# 材料类型映射
MATERIAL_TYPES = [
    '项目申报书',
    '商业计划书',
    '路演PPT',
    '项目图片',
    '演示视频',
    '调研报告',
    '其他附件'
]


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_filename(filename):
    """安全的文件名处理"""
    # 保存原始文件名（用于展示）
    original_name = filename
    # 使用 werkzeug 的安全文件名函数处理存储名（去除路径穿越风险）
    safe_name = werkzeug.utils.secure_filename(filename)
    # 如果 werkzeug 把中文去掉了，就用原始文件名（但替换掉危险字符）
    if not safe_name or safe_name.startswith('.'):
        safe_name = filename.replace('/', '_').replace('\\', '_').replace('..', '_')
    # 生成唯一文件名用于存储
    ext = safe_name.rsplit('.', 1)[1].lower() if '.' in safe_name else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else f"{uuid.uuid4().hex}"
    return unique_name, original_name


def get_file_type(ext):
    """根据扩展名获取文件类型"""
    return FILE_TYPE_MAP.get(ext.lower(), 'other')


def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes is None:
        return '0 B'
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def _get_current_user():
    """获取当前登录用户"""
    user_id = get_jwt_identity()
    if user_id is None:
        return None
    return User.query.get(int(user_id))


def _check_project_access(project, user):
    """检查用户是否有权访问项目"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    if project.teacher_id == user.id:
        return True
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    return False


def _check_upload_permission(project, user):
    """检查用户是否有上传权限（负责人或成员）"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    member = ProjectMember.query.filter_by(project_id=project.id, user_id=user.id).first()
    if member:
        return True
    return False


def _check_delete_permission(file, project, user):
    """检查用户是否有删除权限（上传者、负责人、admin）"""
    if user.is_admin():
        return True
    if project.leader_id == user.id:
        return True
    if file.uploader_id == user.id:
        return True
    return False


@file_bp.route('/projects/<int:project_id>/files', methods=['GET'])
@jwt_required()
def get_files(project_id):
    """获取项目文件列表"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_project_access(project, user):
        return error('无权查看该项目文件', code=403, status_code=403)

    # 获取查询参数
    material_type = request.args.get('material_type')
    file_type = request.args.get('file_type')

    query = ProjectFile.query.filter_by(project_id=project_id)

    if material_type:
        query = query.filter_by(material_type=material_type)
    if file_type:
        query = query.filter_by(file_type=file_type)

    files = query.order_by(ProjectFile.created_at.desc()).all()

    return success({
        'files': [f.to_dict() for f in files],
        'total': len(files)
    })


@file_bp.route('/projects/<int:project_id>/files', methods=['POST'])
@jwt_required()
def upload_file(project_id):
    """上传项目文件"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project = Project.query.get(project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_upload_permission(project, user):
        return error('无权上传文件到该项目', code=403, status_code=403)

    # 检查是否有文件
    if 'file' not in request.files:
        return error('请选择要上传的文件', code=400, status_code=400)

    file = request.files['file']
    if file.filename == '':
        return error('请选择要上传的文件', code=400, status_code=400)

    # 检查文件类型
    if not allowed_file(file.filename):
        return error('不支持的文件类型', code=400, status_code=400)

    # 获取材料类型
    material_type = request.form.get('material_type', '其他附件')
    if material_type not in MATERIAL_TYPES:
        material_type = '其他附件'

    # 安全处理文件名
    unique_name, original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''

    # 创建项目上传目录
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    project_folder = os.path.join(upload_folder, f'project_{project_id}')
    os.makedirs(project_folder, exist_ok=True)

    # 保存文件
    file_path = os.path.join(project_folder, unique_name)
    file.save(file_path)

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 创建数据库记录
    project_file = ProjectFile(
        project_id=project_id,
        uploader_id=user.id,
        file_name=unique_name,
        original_name=original_name,
        file_path=file_path,
        file_type=get_file_type(ext),
        file_size=file_size,
        material_type=material_type
    )

    db.session.add(project_file)
    db.session.commit()

    return success({
        'file': project_file.to_dict()
    }, message='文件上传成功', code=201)


@file_bp.route('/files/<int:file_id>/download', methods=['GET'])
@jwt_required()
def download_file(file_id):
    """下载文件"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project_file = ProjectFile.query.get(file_id)
    if not project_file:
        return error('文件不存在', code=404, status_code=404)

    project = Project.query.get(project_file.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_project_access(project, user):
        return error('无权下载该文件', code=403, status_code=403)

    # 检查文件是否存在
    if not os.path.exists(project_file.file_path):
        return error('文件已丢失', code=404, status_code=404)

    # 获取文件目录和文件名
    directory = os.path.dirname(project_file.file_path)
    filename = project_file.file_name

    return send_from_directory(
        directory,
        filename,
        as_attachment=True,
        download_name=project_file.original_name
    )


@file_bp.route('/files/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    """删除文件"""
    user = _get_current_user()
    if not user:
        return error('用户不存在', code=401, status_code=401)

    project_file = ProjectFile.query.get(file_id)
    if not project_file:
        return error('文件不存在', code=404, status_code=404)

    project = Project.query.get(project_file.project_id)
    if not project:
        return error('项目不存在', code=404, status_code=404)

    if not _check_delete_permission(project_file, project, user):
        return error('无权删除该文件', code=403, status_code=403)

    # 删除物理文件
    if os.path.exists(project_file.file_path):
        try:
            os.remove(project_file.file_path)
        except OSError:
            pass

    # 删除数据库记录
    db.session.delete(project_file)
    db.session.commit()

    return success(message='文件删除成功')
