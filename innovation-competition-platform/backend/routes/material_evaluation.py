import os
import json
import uuid
from datetime import datetime
from flask import Blueprint, request, send_file
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.response import success, error
from models.material_evaluation import MaterialEvaluation
from services.material_evaluation_service import generate_evaluation
from services.material_report_pdf import generate_report_pdf

material_evaluation_bp = Blueprint('material_evaluation', __name__)

ALLOWED_EXTENSIONS = {'pdf'}
ALLOWED_MIME = {'application/pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024

PPT_KEYWORDS_LIST = [
    "痛点", "用户", "市场", "规模", "竞品", "商业模式", "盈利", "技术路线", "创新点",
    "团队", "落地", "试点", "融资", "计划", "里程碑", "风险", "优势", "专利", "数据", "案例"
]

REPORT_KEYWORDS_LIST = [
    "项目背景", "行业痛点", "用户需求", "市场规模", "竞品分析", "商业模式", "收入来源",
    "成本结构", "技术路线", "创新点", "实施计划", "里程碑", "团队分工", "风险分析",
    "财务预测", "社会价值", "推广策略", "调研数据", "专利", "成果转化"
]


def _count_keywords(text, eval_type):
    keywords = PPT_KEYWORDS_LIST if eval_type == "ppt" else REPORT_KEYWORDS_LIST
    count = 0
    for kw in keywords:
        count += text.count(kw)
    return count


def _parse_pdf_basic(filepath):
    info = {"page_count": 0, "text_length": 0, "text": ""}
    try:
        import pypdf
        reader = pypdf.PdfReader(filepath)
        info["page_count"] = len(reader.pages)
        text_parts = []
        for page in reader.pages:
            t = page.extract_text() or ""
            text_parts.append(t)
        full_text = "\n".join(text_parts)
        info["text"] = full_text
        info["text_length"] = len(full_text)
    except Exception:
        try:
            import fitz
            doc = fitz.open(filepath)
            info["page_count"] = doc.page_count
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text() or "")
            full_text = "\n".join(text_parts)
            info["text"] = full_text
            info["text_length"] = len(full_text)
            doc.close()
        except Exception:
            pass
    return info


@material_evaluation_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_material():
    if 'file' not in request.files:
        return error('请选择要上传的文件')

    file = request.files['file']
    evaluation_type = request.form.get('evaluation_type', '').strip()

    if not evaluation_type or evaluation_type not in ('ppt', 'report'):
        return error('评估类型无效，请选择PPT评估或报告评估')

    if file.filename == '':
        return error('请选择要上传的文件')

    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if ext not in ALLOWED_EXTENSIONS:
        return error('当前仅支持PDF文件，请将材料导出为PDF后重新上传')

    if file.mimetype and file.mimetype not in ALLOWED_MIME:
        return error('当前仅支持PDF文件，请将材料导出为PDF后重新上传')

    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)
    if file_size > MAX_FILE_SIZE:
        return error('文件大小超过限制（最大50MB）')

    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'material_evaluation')
    os.makedirs(upload_dir, exist_ok=True)

    safe_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_name)
    file.save(file_path)

    pdf_info = _parse_pdf_basic(file_path)
    keyword_hits = _count_keywords(pdf_info["text"], evaluation_type) if pdf_info["text"] else 0

    evaluation = MaterialEvaluation(
        user_id=user_id,
        evaluation_type=evaluation_type,
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        page_count=pdf_info["page_count"],
        keyword_hits=keyword_hits,
        status='uploaded'
    )
    db.session.add(evaluation)
    db.session.commit()

    return success({
        'id': evaluation.id,
        'file_name': evaluation.file_name,
        'evaluation_type': evaluation.evaluation_type,
        'file_size': evaluation.file_size,
        'page_count': evaluation.page_count,
        'status': evaluation.status
    }, '上传成功')


@material_evaluation_bp.route('/tasks/<int:task_id>/analyze', methods=['POST'])
@jwt_required()
def start_analysis(task_id):
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    evaluation = MaterialEvaluation.query.filter_by(id=task_id, user_id=user_id).first()
    if not evaluation:
        return error('评估任务不存在', 404, 404)
    if evaluation.status not in ('uploaded', 'failed'):
        return error('当前任务状态不允许开始评估')

    evaluation.status = 'analyzing'
    evaluation.progress = 0
    db.session.commit()

    return success({'id': evaluation.id, 'status': evaluation.status}, '评估任务已开始')


@material_evaluation_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task_status(task_id):
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    evaluation = MaterialEvaluation.query.filter_by(id=task_id, user_id=user_id).first()
    if not evaluation:
        return error('评估任务不存在', 404, 404)

    return success(evaluation.to_dict())


@material_evaluation_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_analysis(task_id):
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    evaluation = MaterialEvaluation.query.filter_by(id=task_id, user_id=user_id).first()
    if not evaluation:
        return error('评估任务不存在', 404, 404)
    if evaluation.status != 'analyzing':
        return error('当前任务状态不允许完成评估')

    result = generate_evaluation(evaluation.evaluation_type, evaluation.keyword_hits)

    evaluation.total_score = result["total_score"]
    evaluation.level = result["level"]
    evaluation.core_comment = result["core_comment"]
    evaluation.dimension_scores_json = json.dumps(result["dimension_scores"], ensure_ascii=False)
    evaluation.advantages_json = json.dumps(result["advantages"], ensure_ascii=False)
    evaluation.problems_json = json.dumps(result["problems"], ensure_ascii=False)
    evaluation.suggestions_json = json.dumps(result["suggestions"], ensure_ascii=False)
    evaluation.next_actions_json = json.dumps(result["next_actions"], ensure_ascii=False)
    evaluation.status = 'completed'
    evaluation.progress = 100
    evaluation.completed_at = datetime.utcnow()

    try:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'material_evaluation', 'reports')
        pdf_path = generate_report_pdf(evaluation, output_dir)
        evaluation.pdf_path = pdf_path
        print(f"PDF report generated successfully: {pdf_path}")
    except Exception as e:
        import traceback
        print(f"PDF generation error (will retry on download): {e}")
        traceback.print_exc()

    db.session.commit()

    return success(evaluation.to_dict(), '评估完成')


@material_evaluation_bp.route('/reports/<int:task_id>', methods=['GET'])
@jwt_required()
def get_report(task_id):
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    evaluation = MaterialEvaluation.query.filter_by(id=task_id, user_id=user_id).first()
    if not evaluation:
        return error('评估报告不存在', 404, 404)
    if evaluation.status != 'completed':
        return error('评估尚未完成', 400)

    return success(evaluation.to_dict())


@material_evaluation_bp.route('/reports/<int:task_id>/pdf', methods=['GET'])
@jwt_required()
def download_report_pdf(task_id):
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    evaluation = MaterialEvaluation.query.filter_by(id=task_id, user_id=user_id).first()
    if not evaluation:
        return error('评估报告不存在', 404, 404)
    if evaluation.status != 'completed':
        return error('评估尚未完成', 400)

    if evaluation.pdf_path and os.path.exists(evaluation.pdf_path):
        return send_file(evaluation.pdf_path, as_attachment=True,
                         download_name=f"AI评估报告_{evaluation.evaluation_type}_{evaluation.id}.pdf",
                         mimetype='application/pdf')

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'material_evaluation', 'reports')
    try:
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = generate_report_pdf(evaluation, output_dir)
        if not pdf_path or not os.path.exists(pdf_path):
            return error('PDF生成失败，请稍后重试', 500, 500)
        evaluation.pdf_path = pdf_path
        db.session.commit()
        return send_file(pdf_path, as_attachment=True,
                         download_name=f"AI评估报告_{evaluation.evaluation_type}_{evaluation.id}.pdf",
                         mimetype='application/pdf')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error(f'PDF生成失败: {str(e)}', 500, 500)


@material_evaluation_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_my_tasks():
    user_id = get_jwt_identity()
    user_id = int(user_id) if isinstance(user_id, str) and user_id.isdigit() else user_id

    eval_type = request.args.get('type', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = MaterialEvaluation.query.filter_by(user_id=user_id)
    if eval_type in ('ppt', 'report'):
        query = query.filter_by(evaluation_type=eval_type)

    query = query.order_by(MaterialEvaluation.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return success({
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })