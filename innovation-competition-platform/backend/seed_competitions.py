import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.competition import Competition
from models.competition_track import CompetitionTrack
from models.competition_registration import CompetitionRegistration
from models.registration_member import RegistrationMember
from models.user import User


def seed_competitions():
    """生成逼真的竞赛数据"""
    competitions_data = [
        {
            'name': '2026 大学生创新创业计划训练赛',
            'description': '本次大赛旨在激发大学生创新创业热情，培养创新创业能力，选拔优秀创新创业项目。参赛项目应紧密结合经济社会各领域现实需求，充分体现高校在新工科、新医科、新农科、新文科建设方面取得的成果。',
            'organizer': '校团委创新创业中心',
            'category': '创新创业',
            'level': '校级',
            'registration_start': datetime(2026, 3, 1),
            'registration_end': datetime(2026, 5, 30),
            'competition_start': datetime(2026, 6, 1),
            'competition_end': datetime(2026, 9, 30),
            'status': 'active',
            'tags': '创新创业,训练赛,校级',
            'target_audience': '全校在读本科生、研究生',
            'requirements': '1. 参赛项目能够紧密结合经济社会各领域现实需求；2. 参赛项目应弘扬正能量，践行社会主义核心价值观；3. 参赛项目只能选择一个符合要求的赛道报名参赛。',
            'awards': '一等奖3名（奖金5000元+证书），二等奖6名（奖金3000元+证书），三等奖10名（奖金1000元+证书），优秀奖20名（证书+纪念品），最佳创意奖2名（奖金2000元+证书）',
            'schedule': '报名开始：2026-03-01，报名截止：2026-05-30，初赛评审：2026-06-15，决赛路演：2026-07-10，结果公示：2026-07-20',
            'tracks': [
                {'name': '创意组', 'description': '参赛项目具有较好的创意和较为成型的产品原型或服务模式，在2026年5月30日前尚未完成工商登记注册。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、路演PPT'},
                {'name': '创业组', 'description': '参赛项目在2026年5月30日前已完成工商登记注册，且获机构或个人股权投资不超过1轮次。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、路演PPT、营业执照'},
                {'name': '成长组', 'description': '参赛项目在2026年5月30日前已完成工商登记注册，且获机构或个人股权投资2轮次以上。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、路演PPT、营业执照、财务报表'}
            ]
        },
        {
            'name': '2026 数字经济与商业模式创新挑战赛',
            'description': '聚焦数字经济时代商业模式创新，探索平台经济、智慧零售、数据运营等新兴业态，培养数字经济领域创新创业人才。',
            'organizer': '经济管理学院',
            'category': '数字经济',
            'level': '省级',
            'registration_start': datetime(2026, 2, 15),
            'registration_end': datetime(2026, 5, 20),
            'competition_start': datetime(2026, 6, 1),
            'competition_end': datetime(2026, 8, 31),
            'status': 'active',
            'tags': '数字经济,商业模式,省级',
            'target_audience': '全省高校在读学生',
            'requirements': '1. 参赛项目需围绕数字经济主题；2. 项目需具备商业模式创新要素；3. 团队人数3-5人。',
            'awards': '特等奖1名（奖金10000元），一等奖3名（奖金5000元），二等奖8名（奖金2000元），三等奖15名（奖金1000元）',
            'schedule': '报名开始：2026-02-15，报名截止：2026-05-20，初赛：2026-06-10，复赛：2026-07-15，决赛：2026-08-20',
            'tracks': [
                {'name': '平台经济', 'description': '基于互联网平台的新型商业模式创新。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、数据分析报告'},
                {'name': '智慧零售', 'description': '新零售、无人零售、社交电商等创新模式。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、市场调研报告'},
                {'name': '数据运营', 'description': '基于大数据分析的精细化运营方案。', 'team_min': 3, 'team_max': 5, 'material_requirements': '商业计划书、数据可视化报告'}
            ]
        },
        {
            'name': '2026 AI 应用创新设计大赛',
            'description': '推动人工智能技术与各行业深度融合，鼓励学生探索AI+教育、AI+医疗、AI+制造、AI+办公等创新应用场景。',
            'organizer': '计算机学院',
            'category': '人工智能',
            'level': '校级',
            'registration_start': datetime(2026, 3, 10),
            'registration_end': datetime(2026, 6, 15),
            'competition_start': datetime(2026, 7, 1),
            'competition_end': datetime(2026, 10, 31),
            'status': 'active',
            'tags': '人工智能,AI应用,校级',
            'target_audience': '全校在读学生，鼓励跨专业组队',
            'requirements': '1. 项目需使用人工智能技术；2. 需提交可运行的原型系统；3. 鼓励使用开源大模型。',
            'awards': '金奖2名（奖金8000元），银奖4名（奖金4000元），铜奖8名（奖金2000元），创新奖10名（奖金1000元）',
            'schedule': '报名开始：2026-03-10，报名截止：2026-06-15，作品提交：2026-07-20，初评：2026-08-10，终评答辩：2026-09-15',
            'tracks': [
                {'name': 'AI+教育', 'description': '智能教学、个性化学习、教育评估等AI教育应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '项目代码、演示视频、技术文档'},
                {'name': 'AI+医疗', 'description': '医学影像分析、智能诊断、健康管理等AI医疗应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '项目代码、演示视频、技术文档'},
                {'name': 'AI+制造', 'description': '智能质检、预测性维护、生产优化等AI制造应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '项目代码、演示视频、技术文档'},
                {'name': 'AI+办公', 'description': '智能写作、文档处理、会议助手等AI办公应用。', 'team_min': 2, 'team_max': 5, 'material_requirements': '项目代码、演示视频、技术文档'}
            ]
        },
        {
            'name': '2026 乡村振兴公益创业实践赛',
            'description': '响应国家乡村振兴战略号召，鼓励大学生深入农村基层，围绕农产品品牌、文旅融合、乡村治理、公益服务等领域开展创新创业实践。',
            'organizer': '社会工作学院',
            'category': '乡村振兴',
            'level': '省级',
            'registration_start': datetime(2026, 2, 1),
            'registration_end': datetime(2026, 7, 1),
            'competition_start': datetime(2026, 7, 15),
            'competition_end': datetime(2026, 11, 30),
            'status': 'active',
            'tags': '乡村振兴,公益,省级',
            'target_audience': '全省高校在读学生',
            'requirements': '1. 项目需服务乡村振兴；2. 需有实际落地计划；3. 鼓励与乡村建立合作关系。',
            'awards': '一等奖2名（奖金6000元+孵化支持），二等奖5名（奖金3000元），三等奖10名（奖金1500元），优秀组织奖若干',
            'schedule': '报名开始：2026-02-01，报名截止：2026-07-01，初赛：2026-07-20，实地调研：2026-08，决赛：2026-10-15',
            'tracks': [
                {'name': '农产品品牌', 'description': '农产品品牌化、电商化、供应链优化。', 'team_min': 3, 'team_max': 6, 'material_requirements': '商业计划书、品牌设计方案'},
                {'name': '文旅融合', 'description': '乡村旅游、文化体验、民宿经济。', 'team_min': 3, 'team_max': 6, 'material_requirements': '商业计划书、文旅规划方案'},
                {'name': '乡村治理', 'description': '数字化乡村治理、智慧村务、社区服务。', 'team_min': 3, 'team_max': 6, 'material_requirements': '解决方案、系统原型'},
                {'name': '公益服务', 'description': '教育帮扶、医疗支援、养老服务等公益项目。', 'team_min': 3, 'team_max': 6, 'material_requirements': '项目计划书、服务方案'}
            ]
        },
        {
            'name': '2026 校园电子商务运营挑战赛',
            'description': '以校园电商为场景，锻炼学生电商运营能力，包括直播电商、跨境电商、内容营销、私域运营等方向。',
            'organizer': '商学院',
            'category': '电子商务',
            'level': '校级',
            'registration_start': datetime(2026, 3, 1),
            'registration_end': datetime(2026, 4, 30),
            'competition_start': datetime(2026, 5, 1),
            'competition_end': datetime(2026, 6, 30),
            'status': 'active',
            'tags': '电子商务,运营,校级',
            'target_audience': '全校在读学生',
            'requirements': '1. 需实际运营电商账号或店铺；2. 提交运营数据报告；3. 团队人数3-5人。',
            'awards': '冠军1名（奖金3000元），亚军2名（奖金2000元），季军3名（奖金1000元），最佳运营奖5名',
            'schedule': '报名开始：2026-03-01，报名截止：2026-04-30，运营实战：2026-05-01至2026-06-15，评审答辩：2026-06-25',
            'tracks': [
                {'name': '直播电商', 'description': '通过直播平台进行商品销售和品牌推广。', 'team_min': 3, 'team_max': 5, 'material_requirements': '直播数据报告、视频素材'},
                {'name': '跨境电商', 'description': '通过跨境电商平台进行国际贸易。', 'team_min': 3, 'team_max': 5, 'material_requirements': '运营数据报告、市场分析'},
                {'name': '内容营销', 'description': '通过短视频、图文等内容进行产品营销。', 'team_min': 3, 'team_max': 5, 'material_requirements': '内容作品集、数据分析报告'},
                {'name': '私域运营', 'description': '社群运营、会员管理、用户裂变等私域流量运营。', 'team_min': 3, 'team_max': 5, 'material_requirements': '运营方案、用户增长数据'}
            ]
        },
        {
            'name': '2026 软件工程创新项目挑战赛',
            'description': '面向软件工程领域的创新项目竞赛，鼓励学生运用新技术、新方法解决实际问题，提升软件工程实践能力。',
            'organizer': '软件学院',
            'category': '软件开发',
            'level': '校级',
            'registration_start': datetime(2026, 4, 1),
            'registration_end': datetime(2026, 6, 30),
            'competition_start': datetime(2026, 7, 1),
            'competition_end': datetime(2026, 10, 15),
            'status': 'active',
            'tags': '软件开发,工程实践,校级',
            'target_audience': '全校在读学生',
            'requirements': '1. 需提交可运行的软件系统；2. 代码需开源或提供演示；3. 需提交技术文档。',
            'awards': '最佳项目奖3名（奖金5000元），优秀项目奖6名（奖金2000元），技术创新奖5名（奖金1000元）',
            'schedule': '报名开始：2026-04-01，报名截止：2026-06-30，作品提交：2026-08-15，初评：2026-09-01，终评：2026-10-01',
            'tracks': [
                {'name': 'Web应用', 'description': '基于Web技术的创新应用开发。', 'team_min': 2, 'team_max': 4, 'material_requirements': '源代码、部署文档、演示视频'},
                {'name': '移动应用', 'description': 'iOS、Android或跨平台移动应用开发。', 'team_min': 2, 'team_max': 4, 'material_requirements': '源代码、安装包、演示视频'},
                {'name': '数据可视化', 'description': '大数据可视化、信息图表、交互式展示。', 'team_min': 2, 'team_max': 4, 'material_requirements': '源代码、数据集、演示视频'},
                {'name': 'AIGC工具', 'description': '基于生成式AI的内容创作工具。', 'team_min': 2, 'team_max': 4, 'material_requirements': '源代码、模型说明、演示视频'}
            ]
        },
        {
            'name': '2026 智能制造与物联网应用赛',
            'description': '聚焦智能制造和物联网技术，探索工业互联网、智能硬件、数字孪生等前沿应用，推动制造业数字化转型。',
            'organizer': '机械工程学院',
            'category': '智能制造',
            'level': '省级',
            'registration_start': datetime(2026, 3, 15),
            'registration_end': datetime(2026, 6, 30),
            'competition_start': datetime(2026, 7, 15),
            'competition_end': datetime(2026, 11, 15),
            'status': 'active',
            'tags': '智能制造,物联网,省级',
            'target_audience': '全省高校在读学生',
            'requirements': '1. 项目需涉及智能制造或物联网技术；2. 鼓励硬件原型展示；3. 团队人数3-6人。',
            'awards': '一等奖2名（奖金8000元+企业实习机会），二等奖5名（奖金4000元），三等奖10名（奖金2000元）',
            'schedule': '报名开始：2026-03-15，报名截止：2026-06-30，初赛：2026-07-30，复赛：2026-09-15，决赛：2026-11-01',
            'tracks': [
                {'name': '智能硬件', 'description': '智能传感器、嵌入式系统、机器人等硬件创新。', 'team_min': 3, 'team_max': 6, 'material_requirements': '硬件原型、设计文档、演示视频'},
                {'name': '工业互联网', 'description': '工业数据采集、设备监控、生产管理系统。', 'team_min': 3, 'team_max': 6, 'material_requirements': '系统原型、技术文档、演示视频'},
                {'name': '物联网应用', 'description': '智慧城市、智慧农业、智慧物流等物联网场景应用。', 'team_min': 3, 'team_max': 6, 'material_requirements': '系统原型、技术文档、演示视频'},
                {'name': '数字孪生', 'description': '工厂数字孪生、设备仿真、虚拟调试等应用。', 'team_min': 3, 'team_max': 6, 'material_requirements': '仿真模型、技术文档、演示视频'}
            ]
        },
        {
            'name': '2026 大学生职业规划与就业能力大赛',
            'description': '提升大学生职业规划意识和就业竞争力，通过简历制作、模拟面试、职业测评等环节，帮助学生明确职业发展方向。',
            'organizer': '学生就业指导中心',
            'category': '职业规划',
            'level': '校级',
            'registration_start': datetime(2026, 3, 1),
            'registration_end': datetime(2026, 5, 15),
            'competition_start': datetime(2026, 5, 20),
            'competition_end': datetime(2026, 6, 30),
            'status': 'active',
            'tags': '职业规划,就业,校级',
            'target_audience': '全校在读学生',
            'requirements': '1. 需提交个人简历；2. 参加模拟面试；3. 完成职业测评。',
            'awards': '最佳规划奖5名（奖金2000元+名企内推），优秀简历奖10名（奖金500元），面试达人奖10名',
            'schedule': '报名开始：2026-03-01，报名截止：2026-05-15，初赛（简历筛选）：2026-05-20，复赛（模拟面试）：2026-06-05，决赛：2026-06-20',
            'tracks': [
                {'name': '成长赛道', 'description': '面向低年级学生，侧重职业探索和规划。', 'team_min': 1, 'team_max': 1, 'material_requirements': '职业规划书、简历'},
                {'name': '就业赛道', 'description': '面向应届毕业生，侧重求职技能提升。', 'team_min': 1, 'team_max': 1, 'material_requirements': '简历、求职信'},
                {'name': '创业赛道', 'description': '面向有创业意向的学生，侧重创业能力评估。', 'team_min': 1, 'team_max': 3, 'material_requirements': '创业计划书、简历'}
            ]
        },
        {
            'name': '2026 青年红色筑梦公益项目赛',
            'description': '传承红色基因，弘扬公益精神，鼓励大学生深入革命老区、贫困地区开展公益创业实践，用青春力量助力社会发展。',
            'organizer': '校团委',
            'category': '公益实践',
            'level': '国家级模拟',
            'registration_start': datetime(2026, 2, 20),
            'registration_end': datetime(2026, 7, 31),
            'competition_start': datetime(2026, 8, 1),
            'competition_end': datetime(2026, 12, 15),
            'status': 'active',
            'tags': '公益,红色筑梦,国家级',
            'target_audience': '全国高校在读学生',
            'requirements': '1. 项目需具有公益属性；2. 需服务革命老区或贫困地区；3. 需提交实践计划。',
            'awards': '金奖3名（奖金10000元+证书），银奖6名（奖金5000元+证书），铜奖12名（奖金2000元+证书），优秀项目奖30名',
            'schedule': '报名开始：2026-02-20，报名截止：2026-07-31，初赛：2026-08-15，实践阶段：2026-09至2026-10，决赛：2026-11-20',
            'tracks': [
                {'name': '红色文旅', 'description': '红色旅游资源开发、红色文化传播。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、实践方案'},
                {'name': '社区服务', 'description': '社区治理、便民服务、邻里互助。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、服务方案'},
                {'name': '教育帮扶', 'description': '乡村教育支援、留守儿童关爱。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、教学方案'},
                {'name': '乡村公益', 'description': '乡村医疗、养老、环保等公益项目。', 'team_min': 3, 'team_max': 5, 'material_requirements': '项目计划书、公益方案'}
            ]
        },
        {
            'name': '2026 企业真实命题创新挑战赛',
            'description': '由知名企业发布真实业务命题，学生团队承接命题并提供创新解决方案，优秀方案有机会获得企业采纳和孵化支持。',
            'organizer': '校企合作办公室',
            'category': '产业命题',
            'level': '企业命题',
            'registration_start': datetime(2026, 3, 1),
            'registration_end': datetime(2026, 6, 30),
            'competition_start': datetime(2026, 7, 1),
            'competition_end': datetime(2026, 10, 31),
            'status': 'active',
            'tags': '产业命题,企业,真实需求',
            'target_audience': '全校在读学生',
            'requirements': '1. 需选择企业发布的命题；2. 需与企业导师对接；3. 方案需具有可实施性。',
            'awards': '最佳方案奖4名（奖金10000元+企业实习），优秀方案奖8名（奖金3000元），创新方案奖12名（奖金1000元）',
            'schedule': '报名开始：2026-03-01，报名截止：2026-06-30，方案提交：2026-08-15，初评：2026-09-01，企业答辩：2026-10-10',
            'tracks': [
                {'name': '智慧校园', 'description': '校园服务数字化、智能化解决方案。', 'team_min': 3, 'team_max': 5, 'material_requirements': '解决方案、系统原型'},
                {'name': '绿色低碳', 'description': '碳减排、新能源、循环经济等绿色解决方案。', 'team_min': 3, 'team_max': 5, 'material_requirements': '解决方案、可行性报告'},
                {'name': '企业数字化', 'description': '企业数字化转型、流程优化、管理工具。', 'team_min': 3, 'team_max': 5, 'material_requirements': '解决方案、系统原型'},
                {'name': '用户增长', 'description': '用户获取、留存、转化的增长策略。', 'team_min': 3, 'team_max': 5, 'material_requirements': '增长方案、数据分析报告'}
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


def seed_registrations(users, competitions):
    """生成报名记录"""
    # 获取学生用户
    students = [u for u in users.values() if u.role == 'student']
    if not students:
        print('没有学生用户，跳过报名数据生成')
        return

    registrations_data = [
        {'student_idx': 0, 'comp_idx': 0, 'track_idx': 0, 'status': 'draft'},
        {'student_idx': 0, 'comp_idx': 1, 'track_idx': 1, 'status': 'submitted'},
        {'student_idx': 1, 'comp_idx': 2, 'track_idx': 0, 'status': 'approved'},
        {'student_idx': 1, 'comp_idx': 3, 'track_idx': 2, 'status': 'submitted'},
        {'student_idx': 2, 'comp_idx': 4, 'track_idx': 0, 'status': 'draft'},
        {'student_idx': 0, 'comp_idx': 5, 'track_idx': 1, 'status': 'rejected'},
        {'student_idx': 1, 'comp_idx': 6, 'track_idx': 2, 'status': 'submitted'},
        {'student_idx': 2, 'comp_idx': 7, 'track_idx': 0, 'status': 'approved'},
        {'student_idx': 0, 'comp_idx': 8, 'track_idx': 1, 'status': 'draft'},
        {'student_idx': 1, 'comp_idx': 9, 'track_idx': 3, 'status': 'submitted'},
    ]

    created_count = 0

    for reg_data in registrations_data:
        student = students[reg_data['student_idx'] % len(students)]
        comp = competitions[reg_data['comp_idx'] % len(competitions)]
        tracks = comp.tracks.all()

        if not tracks:
            continue

        track = tracks[reg_data['track_idx'] % len(tracks)]

        existing = CompetitionRegistration.query.filter_by(
            competition_id=comp.id,
            leader_id=student.id
        ).first()
        if existing:
            continue

        registration = CompetitionRegistration(
            competition_id=comp.id,
            track_id=track.id,
            leader_id=student.id,
            team_name=f'{student.real_name or student.username}的团队',
            school='示例大学',
            college='计算机学院',
            major='软件工程',
            teacher_name='张老师',
            teacher_phone='13800138000',
            contact_phone='13900139000',
            contact_email=f'{student.username}@example.com',
            status=reg_data['status'],
            submitted_at=datetime.now() if reg_data['status'] != 'draft' else None
        )

        db.session.add(registration)
        db.session.flush()
        created_count += 1

        # 添加队员
        for i in range(2):
            member = RegistrationMember(
                registration_id=registration.id,
                name=f'队员{i+1}',
                student_no=f'2026{1000+i}',
                college='计算机学院',
                major='软件工程',
                role_in_team='member'
            )
            db.session.add(member)

        # 更新竞赛报名数
        if reg_data['status'] != 'draft':
            comp.registration_count = (comp.registration_count or 0) + 1

    db.session.commit()
    print(f'完成！创建 {created_count} 条报名记录')


def main():
    app = create_app()

    with app.app_context():
        print('=' * 50)
        print('开始生成竞赛和报名数据')
        print('=' * 50)
        print()

        # 获取所有用户
        users = {u.username: u for u in User.query.all()}

        print('1. 生成竞赛数据...')
        competitions = seed_competitions()
        print()

        print('2. 生成报名数据...')
        seed_registrations(users, competitions)
        print()

        print('=' * 50)
        print('竞赛和报名数据生成完成！')
        print('=' * 50)


if __name__ == '__main__':
    main()
