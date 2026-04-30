# 高校创新创业竞赛服务平台

> University Innovation and Entrepreneurship Competition Service Platform

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题等多元化功能。

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Element Plus** - 基于 Vue 3 的组件库
- **Pinia** - Vue 状态管理方案
- **Vue Router** - 前端路由管理
- **Axios** - HTTP 客户端
- **ECharts** - 数据可视化图表库

### 后端
- **Python Flask** - 轻量级 Web 框架
- **Flask-SQLAlchemy** - ORM 数据库工具
- **Flask-Migrate** - 数据库迁移工具
- **Flask-JWT-Extended** - JWT 认证
- **Flask-CORS** - 跨域支持
- **MySQL** - 关系型数据库
- **PyMySQL** - MySQL 驱动
- **python-dotenv** - 环境变量管理

## 项目结构

```
innovation-competition-platform/
├── backend/                 # Flask 后端
│   ├── app.py              # 应用入口
│   ├── config.py           # 配置文件
│   ├── .env                # 环境变量（本地开发）
│   ├── .env.example        # 环境变量示例
│   ├── requirements.txt    # Python 依赖
│   ├── extensions.py       # 扩展初始化
│   ├── seed.py             # 测试数据初始化脚本
│   ├── models/             # 数据模型
│   │   ├── user.py
│   │   ├── competition.py
│   │   ├── competition_track.py
│   │   ├── competition_registration.py
│   │   ├── registration_member.py
│   │   ├── registration_material.py
│   │   ├── project.py
│   │   ├── project_member.py
│   │   ├── project_file.py
│   │   ├── project_task.py
│   │   ├── review.py
│   │   └── ai_record.py
│   ├── routes/             # API 路由
│   │   ├── auth.py         # 认证接口
│   │   ├── user.py         # 用户接口
│   │   ├── project.py      # 项目接口
│   │   ├── member.py       # 成员接口
│   │   ├── file.py         # 文件接口
│   │   ├── task.py         # 任务接口
│   │   ├── review.py       # 评审接口
│   │   ├── dashboard.py    # 看板接口
│   │   ├── ai.py           # AI 接口
│   │   ├── competition.py  # 竞赛接口
│   │   └── registration.py # 报名接口
│   ├── services/           # 业务逻辑
│   │   └── ai_service.py   # AI 服务（Mock）
│   ├── utils/              # 工具函数
│   │   ├── response.py     # 统一响应格式
│   │   └── decorators.py   # 装饰器
│   ├── uploads/            # 文件上传目录
│   │   └── project_<id>/   # 按项目分目录存储
│   └── migrations/         # 数据库迁移
│
├── frontend/               # Vue 3 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── api/            # API 接口封装
│       │   ├── auth.js
│       │   ├── user.js
│       │   ├── project.js
│       │   ├── member.js
│       │   ├── file.js
│       │   ├── task.js
│       │   ├── review.js
│       │   ├── dashboard.js
│       │   ├── ai.js
│       │   └── competition.js
│       ├── assets/         # 静态资源
│       ├── components/     # 公共组件
│       │   └── GuideSystem.vue
│       ├── layouts/        # 布局组件
│       │   └── MainLayout.vue
│       ├── router/         # 路由配置
│       │   └── index.js
│       ├── stores/         # Pinia 状态管理
│       │   ├── user.js
│       │   └── guide.js
│       ├── styles/         # 全局样式
│       │   ├── variables.css
│       │   ├── design-system.css
│       │   └── global.css
│       ├── views/          # 页面视图
│       │   ├── login/            # 登录注册
│       │   ├── dashboard/        # 数据看板（分角色）
│       │   ├── portal/           # 平台首页、竞赛广场等
│       │   ├── projects/         # 项目管理
│       │   ├── reviews/          # 评审管理
│       │   ├── ai-assistant/     # AI 助手
│       │   ├── competitions/     # 比赛管理
│       │   ├── admin/            # 管理员页面
│       │   └── error/            # 错误页面
│       ├── utils/          # 工具函数
│       ├── App.vue
│       └── main.js
│
└── README.md
```

## 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd innovation-competition-platform
```

### 2. MySQL 数据库初始化

#### 2.1 创建数据库

```sql
CREATE DATABASE IF NOT EXISTS innovation_competition
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

#### 2.2 配置环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，修改数据库连接信息
```

`.env` 文件示例：
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
```

### 3. 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库迁移
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 启动服务
python app.py
```

后端服务默认运行在 http://localhost:5000

### 4. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务默认运行在 http://localhost:5173

### 5. 初始化测试数据

```bash
cd backend
python seed.py
```

## 演示账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | admin123 | 管理员 | 系统管理员 |
| student1 | student123 | 学生 | 张三 |
| student2 | student123 | 学生 | 李四 |
| student3 | student123 | 学生 | 王五 |
| teacher1 | teacher123 | 指导老师 | 赵老师 |
| teacher2 | teacher123 | 指导老师 | 钱老师 |
| judge1 | judge123 | 评委 | 孙评委 |
| judge2 | judge123 | 评委 | 周评委 |

## 平台功能模块

### 侧边栏功能入口（按角色）

| 角色 | 侧边栏菜单 |
|------|-----------|
| 学生 | 工作台、我的赛事、我的项目、创建项目、训练营、在线课程、产业命题、证书成果、AI 项目助手 |
| 老师 | 工作台、指导项目、项目审核、训练营、在线课程、产业命题、AI 项目助手 |
| 评委 | 工作台、待评审项目、评审记录、AI 项目助手 |
| 管理员 | 工作台、比赛批次管理、报名管理、项目管理、评审管理、用户管理、数据看板、AI 项目助手 |

### 平台首页 (/portal)
- 双创竞赛服务平台总入口
- 角色化功能卡片（学生/老师/评委/管理员）
- 推荐竞赛展示
- 快捷操作入口

### 竞赛广场 (/competitions)
- 浏览所有可报名竞赛
- 按分类、级别、状态筛选
- 搜索竞赛
- 竞赛卡片展示（海报、信息、报名数）

### 竞赛详情 (/competitions/:id)
- 竞赛头图与基本信息
- 赛道设置
- 时间安排（时间线）
- 奖项设置
- 材料要求
- 报名按钮

### 竞赛报名 (/competitions/:id/register)
- 五步报名流程：选择赛道 → 队伍信息 → 队员信息 → 上传材料 → 确认报名
- 支持关联已有项目
- 队员信息录入
- 材料上传

### 我的赛事 (/my-registrations)
- 查看所有报名记录
- 报名状态统计
- 继续完善草稿
- 查看报名详情

### 训练营 (/training-camps)
- 创新创业基础训练营
- 商业计划书写作训练营
- 路演表达训练营
- AI 项目孵化训练营

### 在线课程 (/courses)
- 创业基础、市场调研、商业模式设计
- 项目路演技巧
- 创业法律与知识产权

### 产业命题 (/industry-topics)
- 企业真实命题展示
- 命题背景与需求说明
- 交付物要求
- 承接命题

### 项目工作室 (/my-projects)
- 项目统计卡片
- 搜索与筛选
- 项目进度展示
- 创建新项目

### AI 助手 (/ai-assistant)
- 生成项目简介
- 商业计划书建议
- 风险分析

### 管理员功能
- 用户管理
- 项目管理
- 比赛批次管理
- 报名管理（审核/驳回）
- 评审管理

## 数据库模型

| 模型 | 说明 | 主要字段 |
|------|------|----------|
| User | 用户信息 | username, password_hash, role, real_name, email |
| Competition | 竞赛信息 | name, description, organizer, category, level, status |
| CompetitionTrack | 竞赛赛道 | competition_id, name, description, team_min, team_max |
| CompetitionRegistration | 竞赛报名 | competition_id, track_id, leader_id, team_name, status |
| RegistrationMember | 报名队员 | registration_id, name, student_no, role_in_team |
| RegistrationMaterial | 报名材料 | registration_id, material_type, file_name, file_path |
| Project | 项目信息 | name, description, status, stage, track, category, leader_id, teacher_id, competition_id |
| ProjectMember | 项目成员 | project_id, user_id, member_name, role_in_project, responsibility |
| ProjectFile | 项目文件 | project_id, filename, original_name, file_type, material_type, file_size, storage_path, uploader_id |
| ProjectTask | 项目任务 | project_id, title, description, assignee_id, status, priority, deadline, completed_at |
| Review | 评审记录 | project_id, judge_id, innovation_score, feasibility_score, market_score, team_score, business_score, technology_score, presentation_score, total_score, comment |
| AiRecord | AI 使用记录 | user_id, project_id, type, prompt, result |

## API 接口文档

### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户信息 |
| `/api/auth/logout` | POST | 登出 |

### 竞赛广场接口（公开）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/public/competitions` | GET | 获取竞赛列表 |
| `/api/public/competitions/<id>` | GET | 获取竞赛详情 |
| `/api/public/competitions/<id>/tracks` | GET | 获取竞赛赛道 |
| `/api/public/competition-categories` | GET | 获取竞赛分类 |

### 报名接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/registrations` | POST | 创建报名草稿 | student |
| `/api/registrations/<id>` | GET | 查看报名详情 | student |
| `/api/registrations/<id>` | PUT | 更新报名信息 | student |
| `/api/registrations/<id>/members` | POST | 添加队员 | student |
| `/api/registrations/<id>/materials` | POST | 上传材料 | student |
| `/api/registrations/<id>/submit` | POST | 提交报名 | student |
| `/api/my-registrations` | GET | 我的报名列表 | student |
| `/api/admin/registrations` | GET | 所有报名（管理员） | admin |
| `/api/admin/registrations/<id>/approve` | POST | 审核通过 | admin |
| `/api/admin/registrations/<id>/reject` | POST | 驳回报名 | admin |

### 项目接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/projects` | GET | 获取项目列表 | 所有登录用户 |
| `/api/projects` | POST | 创建项目 | 学生/管理员 |
| `/api/projects/<id>` | GET | 查看项目详情 | 项目相关人 |
| `/api/projects/<id>` | PUT | 编辑项目 | 负责人/管理员 |
| `/api/projects/<id>` | DELETE | 删除项目 | 负责人/管理员 |
| `/api/projects/<id>/submit` | POST | 提交项目评审 | 负责人/管理员 |

### 其他接口

详见项目代码中的路由文件。

## 项目状态流转

```
draft -> submitted -> teacher_review -> judging -> passed/rejected
  ^         ^
  |         |
need_modify  |
```

## 用户角色

1. **student** - 学生/项目负责人
2. **teacher** - 指导老师
3. **judge** - 评委
4. **admin** - 管理员

## 开发规范

- 遵循 RESTful API 设计规范
- 前端使用 Composition API 风格
- 代码注释使用中文
- 提交信息清晰描述改动内容

## 常见问题

### 1. 数据库连接失败

**解决**：
1. 检查 MySQL 服务是否已启动
2. 确认数据库 `innovation_competition` 已创建
3. 检查 `.env` 文件中的 `DATABASE_URL` 配置
4. 确认用户名和密码正确

### 2. 前端跨域问题

**解决**：
- 后端已配置 Flask-CORS，默认允许所有来源
- 检查后端服务是否正常运行

### 3. 文件上传失败

**解决**：
1. 检查文件类型是否在支持列表中
2. 确认文件大小不超过 4GB
3. 检查 `backend/uploads` 目录是否有写入权限

### 4. JWT 认证失败

**解决**：
1. 检查请求头是否包含 `Authorization: Bearer <token>`
2. 确认 token 未过期
3. 重新登录获取新 token

## 扩展开发

### 接入真实 AI API

当前 AI 功能使用 Mock 数据，如需接入真实 AI：

1. 在 `backend/services/ai_service.py` 中替换生成逻辑
2. 添加 API Key 配置到 `.env` 文件
3. 调用 OpenAI / 文心一言 / 通义千问 等 API

## 许可证

MIT License
