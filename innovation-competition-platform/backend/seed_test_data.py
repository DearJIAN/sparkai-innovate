import os
from app import create_app
from extensions import db
from models.user import User
from models.project import Project
from models.competition import Competition
from datetime import datetime

app = create_app()

def seed_test_data():
    with app.app_context():
        # 获取用户
        student = User.query.filter_by(role='student').first()
        teacher = User.query.filter_by(role='teacher').first()
        judge = User.query.filter_by(role='judge').first()
        admin = User.query.filter_by(role='admin').first()
        
        if not all([student, teacher, judge]):
            print("❌ 缺少必要角色的用户，请先运行 seed.py")
            return

        # 获取一个竞赛
        comp = Competition.query.first()
        if not comp:
            print("❌ 缺少竞赛，请先运行 seed.py")
            return

        # 1. 为指导老师生成待审核的项目 (状态为 'submitted')
        audit_projects = [
            {
                'name': '量子加密通信安全网关',
                'description': '基于量子密钥分发技术的企业级安全网关。',
                'status': 'submitted',
                'category': '网络安全'
            },
            {
                'name': '碳中和智能监测系统',
                'description': '利用传感器网络和AI算法实时监测园区碳排放。',
                'status': 'submitted',
                'category': '绿色科技'
            }
        ]

        for p_data in audit_projects:
            p = Project.query.filter_by(name=p_data['name']).first()
            if not p:
                p = Project(
                    name=p_data['name'],
                    description=p_data['description'],
                    status=p_data['status'],
                    category=p_data['category'],
                    leader_id=student.id,
                    teacher_id=teacher.id,
                    competition_id=comp.id,
                    stage='development'
                )
                db.session.add(p)
                print(f"✅ 创建待审核项目: {p_data['name']} (指导老师: {teacher.username})")

        # 2. 为评委生成待评审的项目 (状态为 'judging')
        review_projects = [
            {
                'name': '垂直起降无人快递机',
                'description': '针对山区末端配送的自动驾驶无人机。',
                'status': 'judging',
                'category': '航空航天'
            },
            {
                'name': '多模态医疗大模型',
                'description': '融合医学影像与文本病例的辅助诊断系统。',
                'status': 'judging',
                'category': '人工智能'
            }
        ]

        for p_data in review_projects:
            p = Project.query.filter_by(name=p_data['name']).first()
            if not p:
                p = Project(
                    name=p_data['name'],
                    description=p_data['description'],
                    status=p_data['status'],
                    category=p_data['category'],
                    leader_id=student.id,
                    teacher_id=teacher.id,
                    competition_id=comp.id,
                    stage='proof'
                )
                db.session.add(p)
                print(f"✅ 创建待评审项目: {p_data['name']}")

        db.session.commit()
        print("Done!")

if __name__ == '__main__':
    seed_test_data()
