import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User
from models.competition import Competition
from models.project import Project
from models.project_member import ProjectMember
from models.project_task import ProjectTask
from models.review import Review


def seed_users():
    """创建测试用户"""
    default_users = [
        {'username': 'admin', 'password': 'admin123', 'role': 'admin', 'real_name': '管理员', 'email': 'admin@example.com'},
        {'username': 'student1', 'password': 'student123', 'role': 'student', 'real_name': '张三', 'email': 'student1@example.com'},
        {'username': 'student2', 'password': 'student123', 'role': 'student', 'real_name': '李四', 'email': 'student2@example.com'},
        {'username': 'student3', 'password': 'student123', 'role': 'student', 'real_name': '王五', 'email': 'student3@example.com'},
        {'username': 'teacher1', 'password': 'teacher123', 'role': 'teacher', 'real_name': '赵老师', 'email': 'teacher1@example.com'},
        {'username': 'teacher2', 'password': 'teacher123', 'role': 'teacher', 'real_name': '钱老师', 'email': 'teacher2@example.com'},
        {'username': 'judge1', 'password': 'judge123', 'role': 'judge', 'real_name': '孙评委', 'email': 'judge1@example.com'},
        {'username': 'judge2', 'password': 'judge123', 'role': 'judge', 'real_name': '周评委', 'email': 'judge2@example.com'},
    ]

    created_count = 0
    user_map = {}

    for user_data in default_users:
        existing = User.query.filter_by(username=user_data['username']).first()
        if existing:
            user_map[user_data['username']] = existing
            continue

        user = User(
            username=user_data['username'],
            email=user_data.get('email'),
            role=user_data['role'],
            real_name=user_data.get('real_name')
        )
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.flush()
        user_map[user_data['username']] = user
        created_count += 1
        print(f'  ✅  创建用户: {user_data["username"]} / 角色: {user_data["role"]}')

    db.session.commit()
    print(f'完成！创建 {created_count} 个新用户')
    return user_map


def seed_competitions():
    """创建测试比赛"""
    competitions_data = [
        {
            'name': '2026年"互联网+"大学生创新创业大赛',
            'description': '第九届中国国际"互联网+"大学生创新创业大赛校内选拔赛',
            'start_time': datetime(2026, 3, 1),
            'end_time': datetime(2026, 6, 30),
            'status': 'active'
        },
        {
            'name': '2026年"挑战杯"大学生创业计划竞赛',
            'description': '第十四届"挑战杯"中国大学生创业计划竞赛',
            'start_time': datetime(2026, 9, 1),
            'end_time': datetime(2026, 12, 31),
            'status': 'draft'
        }
    ]

    created_count = 0
    comp_list = []

    for comp_data in competitions_data:
        existing = Competition.query.filter_by(name=comp_data['name']).first()
        if existing:
            comp_list.append(existing)
            continue

        comp = Competition(**comp_data)
        db.session.add(comp)
        db.session.flush()
        comp_list.append(comp)
        created_count += 1
        print(f'  ✅  创建比赛: {comp_data["name"]}')

    db.session.commit()
    print(f'完成！创建 {created_count} 个新比赛')
    return comp_list


def seed_projects(user_map, competitions):
    """创建测试项目"""
    projects_data = [
        {
            'name': '智慧校园快递柜系统',
            'description': '基于物联网和人工智能技术的智能快递柜管理系统，解决校园快递最后一公里配送问题。',
            'category': '互联网+',
            'track': '高教主赛道',
            'stage': 'development',
            'status': 'passed',
            'leader': 'student1',
            'teacher': 'teacher1'
        },
        {
            'name': 'AI辅助医疗诊断平台',
            'description': '利用深度学习技术辅助医生进行疾病诊断，提高诊断效率和准确率。',
            'category': '人工智能',
            'track': '高教主赛道',
            'stage': 'proof',
            'status': 'judging',
            'leader': 'student2',
            'teacher': 'teacher2'
        },
        {
            'name': '乡村教育数字化平台',
            'description': '为偏远地区学校提供在线教育资源和远程教学服务，促进教育公平。',
            'category': '社会公益',
            'track': '青年红色筑梦之旅',
            'stage': 'idea',
            'status': 'draft',
            'leader': 'student3',
            'teacher': 'teacher1'
        },
        {
            'name': '新能源汽车充电桩共享平台',
            'description': '整合社区、商场、写字楼等场景的闲置充电桩资源，提高充电设施利用率。',
            'category': '新能源',
            'track': '产业命题赛道',
            'stage': 'market',
            'status': 'submitted',
            'leader': 'student1',
            'teacher': 'teacher2'
        }
    ]

    created_count = 0
    project_list = []

    for proj_data in projects_data:
        existing = Project.query.filter_by(name=proj_data['name']).first()
        if existing:
            project_list.append(existing)
            continue

        leader = user_map.get(proj_data['leader'])
        teacher = user_map.get(proj_data['teacher'])

        project = Project(
            name=proj_data['name'],
            description=proj_data['description'],
            category=proj_data['category'],
            track=proj_data['track'],
            stage=proj_data['stage'],
            status=proj_data['status'],
            leader_id=leader.id if leader else None,
            teacher_id=teacher.id if teacher else None,
            competition_id=competitions[0].id if competitions else None
        )
        db.session.add(project)
        db.session.flush()
        project_list.append(project)
        created_count += 1
        print(f'  ✅  创建项目: {proj_data["name"]}')

    db.session.commit()
    print(f'完成！创建 {created_count} 个新项目')
    return project_list


def seed_members(user_map, projects):
    """创建项目成员"""
    members_data = [
        {'project_idx': 0, 'user': 'student1', 'role': '负责人', 'responsibility': '整体统筹、技术开发'},
        {'project_idx': 0, 'user': 'student2', 'role': '成员', 'responsibility': '前端开发、UI设计'},
        {'project_idx': 1, 'user': 'student2', 'role': '负责人', 'responsibility': '算法设计、模型训练'},
        {'project_idx': 1, 'user': 'student3', 'role': '成员', 'responsibility': '数据标注、测试'},
        {'project_idx': 2, 'user': 'student3', 'role': '负责人', 'responsibility': '产品策划、运营'},
        {'project_idx': 3, 'user': 'student1', 'role': '负责人', 'responsibility': '商务拓展、市场推广'},
    ]

    created_count = 0

    for member_data in members_data:
        project = projects[member_data['project_idx']]
        user = user_map.get(member_data['user'])

        if not project or not user:
            continue

        existing = ProjectMember.query.filter_by(
            project_id=project.id, user_id=user.id
        ).first()
        if existing:
            continue

        member = ProjectMember(
            project_id=project.id,
            user_id=user.id,
            member_name=user.real_name or user.username,
            role_in_project=member_data['role'],
            responsibility=member_data['responsibility']
        )
        db.session.add(member)
        created_count += 1

    db.session.commit()
    print(f'完成！创建 {created_count} 个新成员')


def seed_tasks(projects):
    """创建项目任务"""
    tasks_data = [
        {'project_idx': 0, 'title': '完成需求分析文档', 'status': 'done', 'priority': 'high'},
        {'project_idx': 0, 'title': '设计数据库模型', 'status': 'done', 'priority': 'high'},
        {'project_idx': 0, 'title': '开发后端 API', 'status': 'doing', 'priority': 'high'},
        {'project_idx': 0, 'title': '开发前端页面', 'status': 'doing', 'priority': 'medium'},
        {'project_idx': 0, 'title': '编写测试用例', 'status': 'todo', 'priority': 'medium'},
        {'project_idx': 1, 'title': '收集医疗数据集', 'status': 'done', 'priority': 'high'},
        {'project_idx': 1, 'title': '训练 AI 模型', 'status': 'doing', 'priority': 'high'},
        {'project_idx': 1, 'title': '模型效果评估', 'status': 'todo', 'priority': 'high'},
    ]

    created_count = 0

    for task_data in tasks_data:
        project = projects[task_data['project_idx']]
        if not project:
            continue

        task = ProjectTask(
            project_id=project.id,
            title=task_data['title'],
            status=task_data['status'],
            priority=task_data['priority']
        )
        db.session.add(task)
        created_count += 1

    db.session.commit()
    print(f'完成！创建 {created_count} 个新任务')


def seed_reviews(user_map, projects):
    """创建评审记录"""
    reviews_data = [
        {
            'project_idx': 0,
            'judge': 'judge1',
            'innovation_score': 85,
            'feasibility_score': 80,
            'market_score': 75,
            'team_score': 90,
            'business_score': 70,
            'technology_score': 85,
            'presentation_score': 80,
            'comment': '项目思路清晰，技术实现较为成熟，建议加强商业模式设计。'
        },
        {
            'project_idx': 0,
            'judge': 'judge2',
            'innovation_score': 80,
            'feasibility_score': 85,
            'market_score': 80,
            'team_score': 85,
            'business_score': 75,
            'technology_score': 80,
            'presentation_score': 85,
            'comment': '团队执行力强，产品原型完成度高，市场前景良好。'
        },
        {
            'project_idx': 1,
            'judge': 'judge1',
            'innovation_score': 90,
            'feasibility_score': 70,
            'market_score': 85,
            'team_score': 80,
            'business_score': 65,
            'technology_score': 90,
            'presentation_score': 75,
            'comment': '技术创新性强，但商业模式需要进一步完善，建议考虑与医院合作。'
        }
    ]

    created_count = 0

    for review_data in reviews_data:
        project = projects[review_data['project_idx']]
        judge = user_map.get(review_data['judge'])

        if not project or not judge:
            continue

        existing = Review.query.filter_by(
            project_id=project.id, judge_id=judge.id
        ).first()
        if existing:
            continue

        scores = {
            'innovation_score': review_data['innovation_score'],
            'feasibility_score': review_data['feasibility_score'],
            'market_score': review_data['market_score'],
            'team_score': review_data['team_score'],
            'business_score': review_data['business_score'],
            'technology_score': review_data['technology_score'],
            'presentation_score': review_data['presentation_score']
        }
        total_score = round(sum(scores.values()) / len(scores), 2)

        review = Review(
            project_id=project.id,
            judge_id=judge.id,
            **scores,
            total_score=total_score,
            comment=review_data['comment']
        )
        db.session.add(review)
        created_count += 1

    db.session.commit()
    print(f'完成！创建 {created_count} 个新评审')


def main():
    app = create_app()

    with app.app_context():
        print('=' * 50)
        print('开始初始化测试数据')
        print('=' * 50)
        print()

        print('1. 创建用户...')
        user_map = seed_users()
        print()

        print('2. 创建比赛...')
        competitions = seed_competitions()
        print()

        print('3. 创建项目...')
        projects = seed_projects(user_map, competitions)
        print()

        print('4. 创建成员...')
        seed_members(user_map, projects)
        print()

        print('5. 创建任务...')
        seed_tasks(projects)
        print()

        print('6. 创建评审...')
        seed_reviews(user_map, projects)
        print()

        print('=' * 50)
        print('测试数据初始化完成！')
        print('=' * 50)
        print()
        print('演示账号：')
        print('  admin      / admin123      (管理员)')
        print('  student1   / student123    (学生-项目负责人)')
        print('  student2   / student123    (学生-项目负责人)')
        print('  student3   / student123    (学生-项目负责人)')
        print('  teacher1   / teacher123    (指导老师)')
        print('  teacher2   / teacher123    (指导老师)')
        print('  judge1     / judge123      (评委)')
        print('  judge2     / judge123      (评委)')


if __name__ == '__main__':
    main()
