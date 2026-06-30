from app import create_app
from extensions import db
from models.project import Project
from models.user import User
from datetime import datetime

app = create_app()

with app.app_context():
    # Find student 1 and teacher 1
    student = User.query.filter_by(username='student1').first()
    teacher = User.query.filter_by(username='teacher1').first()
    
    if not student or not teacher:
        print("Required users not found.")
        exit(1)
        
    mock_projects = [
        Project(
            name='AI驱动的个性化学习平台',
            description='通过大数据分析和人工智能算法，为学生提供定制化的学习路径和资源推荐。',
            category='科技创新',
            track='人工智能',
            stage='idea',
            leader_id=student.id,
            teacher_id=teacher.id,
            status='submitted',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Project(
            name='基于物联网的智慧农业监测系统',
            description='利用物联网传感器实时采集农作物生长环境数据，并提供自动化的灌溉与施肥控制方案。',
            category='现代农业',
            track='物联网',
            stage='development',
            leader_id=student.id,
            teacher_id=teacher.id,
            status='submitted',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        ),
        Project(
            name='校园二手物品信用交易圈',
            description='建立基于校园真实身份认证的二手交易平台，引入信用评分机制，保障交易安全。',
            category='电子商务',
            track='数字经济',
            stage='proof',
            leader_id=student.id,
            teacher_id=teacher.id,
            status='submitted',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    ]
    
    for p in mock_projects:
        db.session.add(p)
    
    db.session.commit()
    print("Mock projects created successfully!")
