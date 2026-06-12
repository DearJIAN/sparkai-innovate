import os
from app import create_app
from extensions import db
from models.project import Project
from models.project_file import ProjectFile
from services.document_parser import parse_project_files
from services.vector_store import index_documents, index_exists

app = create_app()

def seed_indexes():
    with app.app_context():
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        projects = Project.query.filter(Project.name.in_([
            '量子加密通信安全网关',
            '碳中和智能监测系统',
            '垂直起降无人快递机',
            '多模态医疗大模型'
        ])).all()

        for project in projects:
            print(f"🔄 正在为项目 [{project.name}] 建立索引...")
            
            try:
                # 获取文件列表
                project_files = ProjectFile.query.filter_by(project_id=project.id).all()
                if not project_files:
                    print(f"⚠️ 未找到项目文件")
                    continue

                # 解析并索引
                docs = parse_project_files(project_files, upload_folder)
                if docs:
                    count = index_documents('project', project.id, docs)
                    print(f"✅ 索引完成: {count} 个片段")
                else:
                    print(f"⚠️ 未找到可解析的文档内容")
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"❌ 索引失败: {e}")

        print("Done!")

if __name__ == '__main__':
    seed_indexes()
