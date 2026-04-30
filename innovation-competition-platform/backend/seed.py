import os
import sys
from datetime import datetime, timedelta
import random

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User
from models.competition import Competition
from models.competition_track import CompetitionTrack
from models.competition_registration import CompetitionRegistration
from models.registration_member import RegistrationMember
from models.project import Project
from models.project_member import ProjectMember
from models.project_task import ProjectTask
from models.review import Review

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("PIL library not found, please install Pillow to generate posters.")

def generate_poster(comp_id, text, category):
    """生成简单的竞赛海报图片"""
    # 确保存储路径存在
    poster_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'competition_posters')
    os.makedirs(poster_dir, exist_ok=True)
    
    filename = f"poster_{comp_id}.png"
    filepath = os.path.join(poster_dir, filename)
    
    # 根据分类选择背景色
    colors = {
        '创新创业': '#3498db',
        '数字经济': '#9b59b6',
        '人工智能': '#e74c3c',
        '乡村振兴': '#2ecc71',
        '电子商务': '#f39c12',
        '软件开发': '#34495e',
        '智能制造': '#16a085',
        '职业规划': '#2980b9',
        '公益实践': '#c0392b',
        '产业命题': '#8e44ad',
        '默认': '#7f8c8d'
    }
    bg_color = colors.get(category, colors['默认'])
    
    try:
        # 创建图片 800x360
        img = Image.new('RGB', (800, 360), color=bg_color)
        d = ImageDraw.Draw(img)
        
        # 尝试使用默认字体或者内置字体，由于环境可能没有复杂中文字体，我们做个简单的回退
        try:
            # 尝试加载常见中文字体
            font_title = ImageFont.truetype("msyh.ttc", 36)
            font_sub = ImageFont.truetype("msyh.ttc", 24)
        except Exception:
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
        
        # 绘制文本 (简单居中，由于Pillow的textbbox有点复杂，这里简写坐标)
        d.text((50, 120), text, fill=(255, 255, 255), font=font_title)
        d.text((50, 180), f"类别: {category}", fill=(255, 255, 255), font=font_sub)
        d.text((50, 220), "创新·创业·创造", fill=(240, 240, 240), font=font_sub)
        
        img.save(filepath)
        return f"/uploads/competition_posters/{filename}"
    except Exception as e:
        print(f"海报生成失败: {e}")
        return None

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
    """生成逼真的竞赛数据 10 个"""
    competitions_data = [
        {
            'name': '2026 大学生创新创业计划训练赛',
            'description': '本次大赛旨在激发大学生创新创业热情，培养创新创业能力，选拔优秀创新创业项目。',
            'organizer': '校团委创新创业中心',
            'category': '创新创业',
            'level': '校级',
            'registration_start': datetime.now() - timedelta(days=10),
            'registration_end': datetime.now() + timedelta(days=30),
            'competition_start': datetime.now() + timedelta(days=40),
            'competition_end': datetime.now() + timedelta(days=90),
            'status': 'active',
            'tags': '创新创业,训练赛,校级',
            'target_audience': '全校在读本科生、研究生',
            'requirements': '1. 参赛项目紧密结合现实需求；2. 只能选择一个赛道报名参赛。',
            'awards': '一等奖3名，二等奖6名，三等奖10名',
            'schedule': '报名截止：30天后，初赛评审：45天后，决赛：60天后',
            'tracks': [
                {'name': '创意组', 'description': '具有较好的创意和较为成型的产品原型。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、路演PPT'},
                {'name': '创业组', 'description': '已完成工商登记注册，且获投资不超过1轮次。', 'team_min': 3, 'team_max': 5, 'material_requirements': '计划书、PPT、营业执照'},
                {'name': '成长组', 'description': '已完成工商登记注册，且获投资2轮次以上。', 'team_min': 3, 'team_max': 5, 'material_requirements': '计划书、PPT、营业执照、报表'}
            ]
        },
        {
            'name': '2026 数字经济与商业模式创新挑战赛',
            'description': '聚焦数字经济时代商业模式创新，探索平台经济、智慧零售、数据运营等新兴业态。',
            'organizer': '经济管理学院',
            'category': '数字经济',
            'level': '省级',
            'registration_start': datetime.now() - timedelta(days=20),
            'registration_end': datetime.now() + timedelta(days=10),
            'competition_start': datetime.now() + timedelta(days=20),
            'competition_end': datetime.now() + timedelta(days=60),
            'status': 'active',
            'tags': '数字经济,商业模式,省级',
            'target_audience': '全省高校在读学生',
            'requirements': '1. 需围绕数字经济主题；2. 需具备商业模式创新要素。',
            'awards': '特等奖1名，一等奖3名，二等奖8名',
            'schedule': '报名开始：上月，报名截止：下月，决赛：8月',
            'tracks': [
                {'name': '平台经济', 'description': '新型商业模式创新。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、数据分析报告'},
                {'name': '智慧零售', 'description': '新零售创新模式。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、市场调研报告'},
                {'name': '数据运营', 'description': '数据精细化运营方案。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、数据可视化报告'}
            ]
        },
        {
            'name': '2026 AI 应用创新设计大赛',
            'description': '推动人工智能技术深度融合，探索AI+教育、AI+医疗等应用场景。',
            'organizer': '计算机学院',
            'category': '人工智能',
            'level': '校级',
            'registration_start': datetime.now() - timedelta(days=5),
            'registration_end': datetime.now() + timedelta(days=45),
            'competition_start': datetime.now() + timedelta(days=50),
            'competition_end': datetime.now() + timedelta(days=100),
            'status': 'active',
            'tags': '人工智能,AI应用,校级',
            'target_audience': '全校在读学生，鼓励跨专业组队',
            'requirements': '1. 使用人工智能技术；2. 提交原型系统。',
            'awards': '金奖2名，银奖4名，铜奖8名',
            'schedule': '报名截止：下月末，初评：9月，答辩：10月',
            'tracks': [
                {'name': 'AI+教育', 'description': '智能教学AI应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '代码、视频、文档'},
                {'name': 'AI+医疗', 'description': 'AI医疗应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '代码、视频、文档'},
                {'name': 'AI+制造', 'description': '智能质检应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '代码、视频、文档'},
                {'name': 'AI+办公', 'description': 'AI智能办公。', 'team_min': 2, 'team_max': 5, 'material_requirements': '代码、视频、文档'}
            ]
        },
        {
            'name': '2026 乡村振兴公益创业实践赛',
            'description': '鼓励大学生深入农村基层开展乡村振兴创新创业实践。',
            'organizer': '社会工作学院',
            'category': '乡村振兴',
            'level': '省级',
            'registration_start': datetime.now() - timedelta(days=30),
            'registration_end': datetime.now() - timedelta(days=1),
            'competition_start': datetime.now() + timedelta(days=5),
            'competition_end': datetime.now() + timedelta(days=40),
            'status': 'active',
            'tags': '乡村振兴,公益,省级',
            'target_audience': '全省高校在读学生',
            'requirements': '1. 服务乡村振兴；2. 有实际落地计划。',
            'awards': '一等奖2名，二等奖5名，三等奖10名',
            'schedule': '报名已截止，初赛本月，决赛下月',
            'tracks': [
                {'name': '农产品品牌', 'description': '农产品电商化。', 'team_min': 3, 'team_max': 6, 'material_requirements': '商业计划书、设计方案'},
                {'name': '文旅融合', 'description': '乡村旅游经济。', 'team_min': 3, 'team_max': 6, 'material_requirements': '商业计划书、规划方案'},
                {'name': '公益服务', 'description': '教育帮扶等项目。', 'team_min': 3, 'team_max': 6, 'material_requirements': '项目计划书、服务方案'}
            ]
        },
        {
            'name': '2026 校园电子商务运营挑战赛',
            'description': '校园电商运营能力挑战。',
            'organizer': '商学院',
            'category': '电子商务',
            'level': '校级',
            'registration_start': datetime.now() + timedelta(days=10),
            'registration_end': datetime.now() + timedelta(days=30),
            'competition_start': datetime.now() + timedelta(days=40),
            'competition_end': datetime.now() + timedelta(days=60),
            'status': 'upcoming',
            'tags': '电子商务,运营,校级',
            'target_audience': '全校在读学生',
            'requirements': '1. 实际运营电商账号；2. 提交数据报告。',
            'awards': '冠军1名，亚军2名，季军3名',
            'schedule': '即将开始报名',
            'tracks': [
                {'name': '直播电商', 'description': '平台直播销售。', 'team_min': 3, 'team_max': 5, 'material_requirements': '直播报告、素材'},
                {'name': '内容营销', 'description': '短视频内容营销。', 'team_min': 3, 'team_max': 5, 'material_requirements': '作品集、数据分析'}
            ]
        },
        {
            'name': '2026 软件工程创新项目挑战赛',
            'description': '锻炼软件工程综合开发能力，包含Web、移动端及工具类项目开发。',
            'organizer': '软件学院',
            'category': '软件开发',
            'level': '校级',
            'registration_start': datetime.now() - timedelta(days=15),
            'registration_end': datetime.now() + timedelta(days=15),
            'competition_start': datetime.now() + timedelta(days=20),
            'competition_end': datetime.now() + timedelta(days=50),
            'status': 'active',
            'tags': '软件工程,开发,校级',
            'target_audience': '计算机、软件相关专业学生',
            'requirements': '需提交可用系统源码。',
            'awards': '一等奖3名，二等奖6名，三等奖10名',
            'schedule': '报名进行中，下月评审',
            'tracks': [
                {'name': 'Web应用', 'description': '网站或SaaS系统', 'team_min': 2, 'team_max': 5, 'material_requirements': '源码、说明书'},
                {'name': '移动应用', 'description': '安卓/iOS应用开发', 'team_min': 2, 'team_max': 5, 'material_requirements': '源码、安装包'},
                {'name': 'AIGC工具', 'description': '大语言模型集成工具', 'team_min': 2, 'team_max': 5, 'material_requirements': '源码、使用文档'}
            ]
        },
        {
            'name': '2026 智能制造与物联网应用赛',
            'description': '探索智能硬件与物联网平台的综合应用。',
            'organizer': '机电工程学院',
            'category': '智能制造',
            'level': '省级',
            'registration_start': datetime.now() - timedelta(days=5),
            'registration_end': datetime.now() + timedelta(days=25),
            'competition_start': datetime.now() + timedelta(days=35),
            'competition_end': datetime.now() + timedelta(days=70),
            'status': 'active',
            'tags': '物联网,智能硬件,省级',
            'target_audience': '工科专业在读学生',
            'requirements': '1. 设计硬件原型；2. 连接云平台。',
            'awards': '特等奖1名，一等奖3名，二等奖5名',
            'schedule': '报名进行中，复赛在秋季',
            'tracks': [
                {'name': '智能硬件', 'description': '创新型硬件设备设计。', 'team_min': 3, 'team_max': 5, 'material_requirements': '设计图纸、视频'},
                {'name': '工业互联网', 'description': '工业场景物联网应用。', 'team_min': 3, 'team_max': 5, 'material_requirements': '系统架构、原型演示'}
            ]
        },
        {
            'name': '2026 大学生职业规划与就业能力大赛',
            'description': '提升大学生职业规划意识和求职能力。',
            'organizer': '就业指导中心',
            'category': '职业规划',
            'level': '校级',
            'registration_start': datetime.now() - timedelta(days=40),
            'registration_end': datetime.now() - timedelta(days=10),
            'competition_start': datetime.now() - timedelta(days=5),
            'competition_end': datetime.now() + timedelta(days=10),
            'status': 'active',
            'tags': '职业规划,就业,校级',
            'target_audience': '全校在读学生',
            'requirements': '提交个人简历及职业规划书。',
            'awards': '一等奖5名，二等奖10名，三等奖20名',
            'schedule': '报名结束，正处于决赛阶段',
            'tracks': [
                {'name': '成长赛道', 'description': '适合大一、大二学生。', 'team_min': 1, 'team_max': 1, 'material_requirements': '职业规划书'},
                {'name': '就业赛道', 'description': '适合大三、大四及研究生。', 'team_min': 1, 'team_max': 1, 'material_requirements': '个人简历、求职意向书'}
            ]
        },
        {
            'name': '2026 青年红色筑梦公益项目赛',
            'description': '结合红色文化与社会公益，打造具有社会价值的项目。',
            'organizer': '校团委',
            'category': '公益实践',
            'level': '国家级模拟',
            'registration_start': datetime.now() - timedelta(days=20),
            'registration_end': datetime.now() + timedelta(days=20),
            'competition_start': datetime.now() + timedelta(days=30),
            'competition_end': datetime.now() + timedelta(days=80),
            'status': 'active',
            'tags': '公益,红色文旅',
            'target_audience': '全国高校在读学生',
            'requirements': '聚焦红色文化或老区发展。',
            'awards': '金奖、银奖、铜奖若干',
            'schedule': '报名进行中，全国总决赛在年底',
            'tracks': [
                {'name': '红色文旅', 'description': '红色文化旅游资源开发。', 'team_min': 3, 'team_max': 7, 'material_requirements': '策划方案'},
                {'name': '社区服务', 'description': '老旧社区志愿服务。', 'team_min': 3, 'team_max': 7, 'material_requirements': '服务记录、总结报告'}
            ]
        },
        {
            'name': '2026 企业真实命题创新挑战赛',
            'description': '由知名企业发布真实业务需求，学生组队提供解决方案。',
            'organizer': '创新创业学院及合作企业',
            'category': '产业命题',
            'level': '企业命题',
            'registration_start': datetime.now() - timedelta(days=5),
            'registration_end': datetime.now() + timedelta(days=40),
            'competition_start': datetime.now() + timedelta(days=50),
            'competition_end': datetime.now() + timedelta(days=90),
            'status': 'active',
            'tags': '企业命题,实战',
            'target_audience': '全校各专业学生',
            'requirements': '针对具体企业命题给出可行方案。',
            'awards': '企业提供奖金及实习offer',
            'schedule': '报名刚开始',
            'tracks': [
                {'name': '智慧校园系统研发', 'description': '腾讯公司提供命题。', 'team_min': 3, 'team_max': 5, 'material_requirements': '解决方案设计'},
                {'name': '绿色低碳供应链优化', 'description': '京东物流提供命题。', 'team_min': 3, 'team_max': 5, 'material_requirements': '优化方案模型'},
                {'name': '企业数字化转型', 'description': '华为提供命题。', 'team_min': 3, 'team_max': 5, 'material_requirements': '转型白皮书'}
            ]
        }
    ]

    created_count = 0
    comp_list = []

    for comp_data in competitions_data:
        existing = Competition.query.filter_by(name=comp_data['name']).first()
        if existing:
            comp_list.append(existing)
            continue

        tracks_data = comp_data.pop('tracks', [])

        comp = Competition(**comp_data)
        db.session.add(comp)
        db.session.flush()
        
        # 生成海报
        poster_url = generate_poster(comp.id, comp.name[:12]+'...', comp.category)
        if poster_url:
            comp.poster_url = poster_url
            
        comp_list.append(comp)
        created_count += 1
        print(f'  ✅  创建竞赛: {comp_data["name"]}')

        # 创建赛道
        for track_data in tracks_data:
            track = CompetitionTrack(
                competition_id=comp.id,
                **track_data
            )
            db.session.add(track)

    db.session.commit()
    print(f'完成！创建 {created_count} 个新竞赛')
    return comp_list


def seed_projects(user_map, competitions):
    """创建测试项目"""
    projects_data = [
        {'name': '智慧校园快递柜系统', 'description': '基于物联网的快递管理。', 'category': '互联网+', 'track': '高教主赛道', 'stage': 'development', 'status': 'passed', 'leader': 'student1', 'teacher': 'teacher1', 'progress': 85},
        {'name': 'AI辅助医疗诊断平台', 'description': '深度学习辅助诊断。', 'category': '人工智能', 'track': '高教主赛道', 'stage': 'proof', 'status': 'judging', 'leader': 'student2', 'teacher': 'teacher2', 'progress': 60},
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
            competition_id=competitions[0].id if competitions else None,
            progress=proj_data.get('progress', 0)
        )
        db.session.add(project)
        db.session.flush()
        project_list.append(project)
        created_count += 1

    db.session.commit()
    return project_list


def seed_registrations(user_map, competitions):
    """生成包含队伍和队员的报名记录"""
    students = [u for u in user_map.values() if u.role == 'student']
    if not students:
        return

    # 包含 draft, submitted, approved, rejected 状态
    registrations_data = [
        {'student': 'student1', 'comp_idx': 0, 'track_idx': 0, 'status': 'draft'},
        {'student': 'student1', 'comp_idx': 1, 'track_idx': 1, 'status': 'submitted'},
        {'student': 'student1', 'comp_idx': 2, 'track_idx': 0, 'status': 'approved'},
        {'student': 'student2', 'comp_idx': 0, 'track_idx': 1, 'status': 'rejected', 'remark': '计划书内容不符合赛道要求'},
        {'student': 'student2', 'comp_idx': 3, 'track_idx': 2, 'status': 'submitted'},
        {'student': 'student3', 'comp_idx': 4, 'track_idx': 0, 'status': 'draft'},
        {'student': 'student3', 'comp_idx': 5, 'track_idx': 0, 'status': 'approved'},
        {'student': 'student1', 'comp_idx': 6, 'track_idx': 0, 'status': 'submitted'},
    ]

    created_count = 0

    for reg_data in registrations_data:
        student = user_map.get(reg_data['student'])
        if not student:
            continue

        comp = competitions[reg_data['comp_idx'] % len(competitions)]
        tracks = comp.tracks.all()
        if not tracks:
            continue
        track = tracks[reg_data['track_idx'] % len(tracks)]

        existing = CompetitionRegistration.query.filter_by(competition_id=comp.id, leader_id=student.id).first()
        if existing:
            continue

        registration = CompetitionRegistration(
            competition_id=comp.id,
            track_id=track.id,
            leader_id=student.id,
            team_name=f'{student.real_name or student.username}的创新团队',
            school='创新创业示范大学',
            college='计算机学院',
            major='软件工程',
            teacher_name='测试导师',
            teacher_phone='13800000000',
            contact_phone='13900000000',
            contact_email=f'{student.username}@example.com',
            status=reg_data['status'],
            remark=reg_data.get('remark'),
            submitted_at=datetime.now() if reg_data['status'] != 'draft' else None
        )
        db.session.add(registration)
        db.session.flush()
        created_count += 1

        # 添加默认队长作为队员
        leader_member = RegistrationMember(
            registration_id=registration.id,
            name=student.real_name,
            student_no=f'202400{student.id}',
            college='计算机学院',
            major='软件工程',
            role_in_team='leader'
        )
        db.session.add(leader_member)

        # 随机添加2个其他队员
        for i in range(2):
            member = RegistrationMember(
                registration_id=registration.id,
                name=f'队员A{i+1}',
                student_no=f'2026{1000+i}{created_count}',
                college='相关学院',
                major='相关专业',
                role_in_team='member'
            )
            db.session.add(member)

        # 状态不是 draft 就增加竞赛的报名数量
        if reg_data['status'] != 'draft':
            comp.registration_count = (comp.registration_count or 0) + 1

    db.session.commit()
    print(f'完成！创建 {created_count} 条报名记录')

def main():
    app = create_app()

    with app.app_context():
        print('=' * 50)
        print('开始初始化测试数据')
        print('=' * 50)
        
        user_map = seed_users()
        competitions = seed_competitions()
        projects = seed_projects(user_map, competitions)
        seed_registrations(user_map, competitions)
        
        print('=' * 50)
        print('测试数据初始化完成！')
        print('演示账号：admin / student1 / teacher1 / judge1, 密码均为 用户名+123')

if __name__ == '__main__':
    main()
