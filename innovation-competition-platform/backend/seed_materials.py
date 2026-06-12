import os
import shutil
import uuid
from app import create_app
from extensions import db
from models.project import Project
from models.project_file import ProjectFile
from models.user import User

app = create_app()

def seed_materials():
    with app.app_context():
        # 获取一个学生作为上传者
        student = User.query.filter_by(role='student').first()
        if not student:
            print("❌ 找不到学生用户")
            return

        upload_root = os.path.join(os.getcwd(), 'uploads')
        os.makedirs(upload_root, exist_ok=True)

        mapping = [
            {'name': '量子加密通信安全网关', 'src': 'temp_quantum.txt', 'orig': '量子加密安全网关_商业计划书.txt', 'type': 'business_plan'},
            {'name': '碳中和智能监测系统', 'src': 'temp_carbon.txt', 'orig': '碳中和智能监测系统计_说明.txt', 'type': 'business_plan'},
            {'name': '垂直起降无人快递机', 'src': 'temp_drone.txt', 'orig': 'eVTOL无人快递机项目说明.txt', 'type': 'technical_doc'},
            {'name': '多模态医疗大模型', 'src': 'temp_medical.txt', 'orig': '多模态医疗模型架构设计.txt', 'type': 'research_report'}
        ]

        for item in mapping:
            project = Project.query.filter_by(name=item['name']).first()
            if not project:
                print(f"⚠️ 找不到项目: {item['name']}, 跳过")
                continue
            
            # 删除旧的文件记录和文件操作（简单起见，这里只删DB记录，磁盘文件由新的覆盖或保留无碍）
            ProjectFile.query.filter_by(project_id=project.id).delete()
            db.session.commit()
            print(f"🧹 已重置项目 [{item['name']}] 的文件记录")

            # 准备目标文件夹
            project_dir = os.path.join(upload_root, f'project_{project.id}')
            os.makedirs(project_dir, exist_ok=True)

            # 生成唯一文件名
            ext = item['orig'].split('.')[-1]
            unique_name = f"{uuid.uuid4().hex}.{ext}"
            dest_path = os.path.join(project_dir, unique_name)

            # 复制文件
            src_path = os.path.join(upload_root, item['src'])
            if os.path.exists(src_path):
                shutil.copy(src_path, dest_path)
                file_size = os.path.getsize(dest_path)

                # 记录到数据库
                pf = ProjectFile(
                    project_id=project.id,
                    uploader_id=student.id,
                    file_name=unique_name,
                    original_name=item['orig'],
                    file_path=dest_path, # 数据库通常存储相对路径或绝对路径，视配置而定。由于 backend/app.py 可能有对应配置，此处使用绝对路径或相对路径需要谨慎。
                    file_type=ext,
                    file_size=file_size,
                    material_type=item['type']
                )
                db.session.add(pf)
                print(f"✅ 为项目 [{item['name']}] 上传了文件: {item['orig']}")
            else:
                print(f"❌ 源文件不存在: {src_path}")

        db.session.commit()
        print("Done!")

if __name__ == '__main__':
    seed_materials()
