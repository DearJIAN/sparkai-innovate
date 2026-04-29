# 创新创业比赛全流程管理系统

> Innovation Competition Management Platform

一个面向高校的创新创业比赛全流程管理软件，覆盖项目从申报、团队管理、材料上传、任务进度、评审打分、AI 辅助、管理员看板的完整流程。

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
│   │   ├── competition.py  # 比赛接口
│   │   ├── material.py     # 材料接口（预留）
│   │   └── team.py         # 团队接口（预留）
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
│       │   ├── GuideSystem.vue   # 新手引导系统
│       │   └── HelloWorld.vue
│       ├── layouts/        # 布局组件
│       │   └── MainLayout.vue
│       ├── router/         # 路由配置
│       │   └── index.js
│       ├── stores/         # Pinia 状态管理
│       │   ├── user.js
│       │   └── guide.js    # 引导状态管理
│       ├── views/          # 页面视图
│       │   ├── login/            # 登录注册
│       │   ├── dashboard/        # 数据看板（分角色）
│       │   ├── projects/         # 项目管理
│       │   ├── reviews/          # 评审管理
│       │   ├── ai-assistant/     # AI 助手
│       │   ├── competitions/     # 比赛管理
│       │   ├── admin/            # 管理员页面
│       │   ├── tasks/            # 任务页面（预留）
│       │   ├── materials/        # 材料页面（预留）
│       │   ├── teams/            # 团队页面（预留）
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

使用 MySQL 客户端（如 MySQL Workbench、Navicat 或命令行）执行以下 SQL：

```sql
CREATE DATABASE IF NOT EXISTS innovation_competition
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

命令行方式：
```bash
mysql -u root -p
-- 输入密码后执行
CREATE DATABASE innovation_competition CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### 2.2 配置环境变量

```bash
cd backend

# 复制环境变量示例文件
cp .env.example .env

# 编辑 .env 文件，修改数据库连接信息
```

`.env` 文件示例：
```env
# Flask 配置
SECRET_KEY=your-secret-key-here

# MySQL 数据库配置
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4

# JWT 配置
JWT_SECRET_KEY=your-jwt-secret-key-here

# 环境
FLASK_ENV=development
FLASK_DEBUG=1
```

**注意**：请将 `root:123456` 替换为你本地 MySQL 的实际用户名和密码。

### 3. 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

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

**启动成功输出示例**：
```
✅ 数据库连接成功
✅ 数据库表创建完成
 * Running on http://0.0.0.0:5000
```

**数据库连接失败时**：
```
❌ 数据库连接失败: (pymysql.err.OperationalError) (2003, "Can't connect to MySQL server on 'localhost' ([WinError 10061] ...)")
请检查:
  1. MySQL 服务是否已启动
  2. 数据库 innovation_competition 是否已创建
  3. 用户名和密码是否正确
  4. .env 文件中的 DATABASE_URL 配置
```

### 4. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务默认运行在 http://localhost:5173

### 5. 访问系统

打开浏览器访问 http://localhost:5173

### 6. 初始化测试数据（可选）

```bash
cd backend
python seed.py
```

这将创建测试用户、比赛、项目、成员、任务和评审记录。

## 演示账号

| 用户名 | 密码 | 角色 | 说明 |
|--------|------|------|------|
| admin | admin123 | 管理员 | 系统管理员 |
| student1 | student123 | 学生 | 项目负责人 |
| student2 | student123 | 学生 | 项目负责人 |
| student3 | student123 | 学生 | 项目负责人 |
| teacher1 | teacher123 | 指导老师 | 项目指导 |
| teacher2 | teacher123 | 指导老师 | 项目指导 |
| judge1 | judge123 | 评委 | 项目评审 |
| judge2 | judge123 | 评委 | 项目评审 |

## 健康检查

后端提供健康检查接口，用于验证服务状态：

```bash
curl http://localhost:5000/api/health
```

**正常响应**：
```json
{
  "status": "ok",
  "message": "服务运行正常",
  "database": "connected"
}
```

**数据库异常响应**：
```json
{
  "status": "degraded",
  "message": "服务运行正常",
  "database": "disconnected",
  "database_error": "..."
}
```

## 用户角色

1. **student** - 学生/项目负责人
2. **teacher** - 指导老师
3. **judge** - 评委
4. **admin** - 管理员

## 数据库模型

| 模型 | 说明 | 主要字段 |
|------|------|----------|
| User | 用户信息 | username, password_hash, role, real_name, email |
| Competition | 比赛批次 | name, description, start_time, end_time, status |
| Project | 项目信息 | name, description, status, stage, track, category, leader_id, teacher_id, competition_id |
| ProjectMember | 项目成员 | project_id, user_id, member_name, role_in_project, responsibility |
| ProjectFile | 项目文件 | project_id, filename, original_name, file_type, material_type, file_size, storage_path, uploader_id |
| ProjectTask | 项目任务 | project_id, title, description, assignee_id, status, priority, deadline, completed_at |
| Review | 评审记录 | project_id, judge_id, innovation_score, feasibility_score, market_score, team_score, business_score, technology_score, presentation_score, total_score, comment |
| AiRecord | AI 使用记录 | user_id, project_id, type, prompt, result |

## MVP 核心功能

- [x] 登录注册
- [x] 角色权限控制（基础框架）
- [x] 学生创建和管理创新创业项目（后端 API 完成）
- [x] 项目团队成员管理（后端 API + 前端页面完成）
- [x] 项目材料上传和下载（图片、Word、PPT、PDF、视频等）
- [x] 项目任务与阶段进度管理
- [x] 项目提交评审（后端 API 完成）
- [x] 评委查看项目并评分
- [x] 学生查看评审结果
- [x] 管理员查看项目数据看板
- [x] AI 辅助生成项目简介、商业计划书建议、风险分析
- [x] 比赛批次管理
- [x] 新手引导系统（支持多角色、动态高亮、透明度调节、拖拽）

## API 接口文档

### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户信息（需 JWT） |
| `/api/auth/logout` | POST | 登出（需 JWT） |

### 用户接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/users` | GET | 获取用户列表 | admin |
| `/api/users/<id>` | GET | 获取用户详情 | admin |
| `/api/users/<id>` | PUT | 更新用户信息 | admin/本人 |
| `/api/users/<id>` | DELETE | 删除用户 | admin |

### 项目接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/projects` | GET | 获取项目列表 | 所有登录用户 |
| `/api/projects` | POST | 创建项目 | 学生/管理员 |
| `/api/projects/<id>` | GET | 查看项目详情 | 项目相关人 |
| `/api/projects/<id>` | PUT | 编辑项目 | 负责人/管理员 |
| `/api/projects/<id>` | DELETE | 删除项目 | 负责人/管理员（仅 draft） |
| `/api/projects/<id>/submit` | POST | 提交项目评审 | 负责人/管理员 |

### 成员接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/projects/<id>/members` | GET | 获取项目成员列表 | 项目相关人 |
| `/api/projects/<id>/members` | POST | 添加项目成员 | 负责人/管理员 |
| `/api/members/<id>` | PUT | 编辑成员信息 | 负责人/管理员 |
| `/api/members/<id>` | DELETE | 删除成员 | 负责人/管理员 |

### 文件接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/projects/<id>/files` | GET | 获取项目文件列表 | 项目相关人/teacher/judge/admin |
| `/api/projects/<id>/files` | POST | 上传项目文件 | 负责人/成员/admin |
| `/api/files/<file_id>/download` | GET | 下载文件 | 项目相关人/teacher/judge/admin |
| `/api/files/<file_id>` | DELETE | 删除文件 | 上传者/负责人/admin |

**支持的材料类型**：项目申报书、商业计划书、路演PPT、项目图片、演示视频、调研报告、其他附件

**材料类型说明**：

| 材料类型 | 英文标识 | 说明 |
|----------|----------|------|
| 项目申报书 | declaration | 项目申报相关文档 |
| 商业计划书 | business_plan | 商业计划书文档 |
| 路演 PPT | roadshow_ppt | 路演演示文稿 |
| 项目图片 | project_image | 项目相关图片 |
| 演示视频 | demo_video | 项目演示视频 |
| 调研报告 | research_report | 调研分析报告 |
| 其他附件 | other | 其他类型附件 |

**支持的文件类型**：
- 图片：jpg, jpeg, png, gif, webp
- 文档：doc, docx, pdf, txt
- PPT：ppt, pptx
- 表格：xls, xlsx
- 视频：mp4, mov, avi
- 压缩包：zip, rar

**文件存储路径**：`backend/uploads/project_<project_id>/<uuid>.<ext>`

**单文件大小限制**：4GB

### 任务接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/projects/<id>/tasks` | GET | 获取项目任务列表 | 项目相关人 |
| `/api/projects/<id>/tasks` | POST | 创建任务 | 负责人/管理员 |
| `/api/tasks/<task_id>` | PUT | 更新任务 | 负责人/管理员 |
| `/api/tasks/<task_id>` | DELETE | 删除任务 | 负责人/管理员 |

**任务状态**：todo（待开始）、doing（进行中）、done（已完成）、delayed（已延期）、cancelled（已取消）

**任务优先级**：low（低）、medium（中）、high（高）

### 评审接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/reviews/projects` | GET | 获取待评审项目列表 | judge/admin |
| `/api/reviews/projects/<id>` | GET | 获取项目评审详情 | judge/admin |
| `/api/reviews/projects/<id>` | POST | 提交/更新评审 | judge/admin |
| `/api/projects/<id>/reviews` | GET | 查看项目评审结果 | 项目相关人 |
| `/api/reviews/my` | GET | 我的评审记录 | judge/admin |

**评分维度**：创新性、可行性、市场前景、团队能力、商业模式、技术实现、路演表现（各0-100分）

**总分计算**：七项平均分

### AI 接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/ai/project-summary` | POST | 生成项目简介 | 所有登录用户 |
| `/api/ai/business-plan-advice` | POST | 生成商业计划书建议 | 所有登录用户 |
| `/api/ai/risk-analysis` | POST | 生成风险分析 | 所有登录用户 |
| `/api/ai/records` | GET | 获取 AI 使用记录 | 所有登录用户 |

**AI 功能说明**：当前版本使用 Mock 数据模拟 AI 生成，后续可替换为真实 AI API（如 OpenAI、文心一言、通义千问等）

### 比赛接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/competitions` | GET | 获取比赛列表 | 所有登录用户 |
| `/api/competitions` | POST | 创建比赛 | admin |
| `/api/competitions/<id>` | PUT | 更新比赛 | admin |
| `/api/competitions/<id>` | DELETE | 删除比赛 | admin |

**比赛状态**：draft（草稿）、active（进行中）、ended（已结束）、archived（已归档）

### 预留接口

以下接口为预留扩展接口，当前版本已实现基础框架：

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/materials` | GET | 材料列表 | 所有登录用户 |
| `/api/materials/upload` | POST | 材料上传 | 所有登录用户 |
| `/api/teams` | GET | 团队列表 | 所有登录用户 |
| `/api/teams/<id>` | GET | 团队详情 | 所有登录用户 |

### 管理员看板接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/api/dashboard/stats` | GET | 获取统计数据 | admin |
| `/api/dashboard/recent` | GET | 获取最近数据 | admin |

**统计数据包括**：用户统计、项目统计（按状态/阶段/赛道）、文件数、评审数、比赛数、AI 调用数

#### 项目列表查询参数

```
GET /api/projects?keyword=xxx&status=draft&stage=idea&track=人工智能&page=1&per_page=10
```

| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 项目名称关键字搜索 |
| status | string | 项目状态过滤 |
| stage | string | 项目阶段过滤 |
| track | string | 赛道过滤 |
| page | int | 页码，默认 1 |
| per_page | int | 每页数量，默认 10 |

#### 项目权限规则

| 角色 | 列表可见范围 |
|------|-------------|
| student | 自己负责或参与的项目 |
| teacher | 自己指导的项目 |
| judge | 已提交或评审中的项目 |
| admin | 所有项目 |

#### 项目状态流转

```
draft -> submitted -> teacher_review -> judging -> passed/rejected
  ^         ^
  |         |
need_modify  |
```

- `draft`: 草稿，可编辑删除
- `submitted`: 已提交，等待审核
- `teacher_review`: 教师审核中
- `judging`: 评审中，不可修改
- `passed`: 已通过
- `rejected`: 已驳回
- `need_modify`: 需要修改，可重新提交

## 项目阶段

| 阶段 | 英文标识 | 说明 |
|------|----------|------|
| 创意阶段 | idea | 项目创意构思阶段 |
| 验证阶段 | proof | 概念验证阶段 |
| 资源整合 | resource | 资源整合阶段 |
| 产品开发 | development | 产品开发阶段 |
| 市场推广 | market | 市场推广阶段 |
| 路演展示 | roadshow | 路演展示阶段 |
| 孵化运营 | incubation | 孵化运营阶段 |

## 项目赛道

| 赛道 | 说明 |
|------|------|
| 高教主赛道 | 本科生创意组、创业组等 |
| 青年红色筑梦之旅 | 红色主题、乡村振兴 |
| 产业命题赛道 | 企业命题、产教融合 |

## 前端页面路由

| 路由 | 页面 | 说明 |
|------|------|------|
| `/login` | 登录页 | 用户登录 |
| `/register` | 注册页 | 用户注册 |
| `/dashboard` | 数据看板 | 根据角色显示不同内容 |
| `/my-projects` | 我的项目 | 学生查看自己的项目 |
| `/guide-projects` | 指导项目 | 教师查看指导的项目 |
| `/projects/:id` | 项目详情 | 查看项目详情 |
| `/projects/:id/members` | 成员管理 | 管理项目成员 |
| `/projects/:id/files` | 材料管理 | 上传下载项目材料 |
| `/projects/:id/tasks` | 任务管理 | 管理项目任务进度 |
| `/pending-reviews` | 待评审项目 | 评委查看待评审项目 |
| `/reviews/:id` | 项目评审 | 评委进行评审打分 |
| `/review-history` | 评审记录 | 查看评审历史 |
| `/ai-assistant` | AI 助手 | AI 辅助功能 |
| `/competition-management` | 比赛管理 | 管理员管理比赛批次 |
| `/project-management` | 项目管理 | 管理员管理所有项目 |
| `/user-management` | 用户管理 | 管理员管理用户 |
| `/review-management` | 评审管理 | 管理员查看所有评审 |
| `/project-review` | 项目审核 | 教师审核学生项目 |
| `/create-project` | 创建项目 | 学生创建新项目 |
| `/projects/:id/edit` | 编辑项目 | 编辑项目信息 |

## 新手引导系统

系统内置了完善的新手引导功能，帮助不同角色的用户快速上手。

### 引导功能特性

| 特性 | 说明 |
|------|------|
| **多角色引导** | 学生、教师、评委、管理员各有专属引导流程 |
| **动态高亮** | 引导过程中动态高亮页面元素，引起注意 |
| **步骤导航** | 显示当前步骤序号，支持点击跳转 |
| **上一步/下一步** | 支持前后导航，方便回顾 |
| **透明度调节** | 底部滑块实时调节遮罩层透明度（10%-100%） |
| **拖拽功能** | 引导弹窗支持全屏拖拽，通过顶部手柄拖动 |
| **暂不需要按钮** | 可随时关闭引导，左侧出现重新打开按钮 |
| **首次登录询问** | 登录后自动弹出欢迎弹窗询问是否需要引导 |

### 引导流程

**学生引导（9步）**：
1. 欢迎使用 → 2. 数据看板 → 3. 我的项目 → 4. 项目详情 → 5. 团队成员管理 → 6. 项目材料上传 → 7. 任务进度管理 → 8. AI 项目助手 → 9. 开始创业之旅

**教师引导（7步）**：
1. 欢迎使用 → 2. 数据看板 → 3. 指导项目 → 4. 项目详情与审核 → 5. 评审结果查看 → 6. AI 助手辅助 → 7. 开始指导学生

**评委引导（7步）**：
1. 欢迎使用 → 2. 数据看板 → 3. 待评审项目 → 4. 项目评审 → 5. 评分维度 → 6. 评审记录 → 7. 开始评审

**管理员引导（8步）**：
1. 欢迎使用 → 2. 管理员看板 → 3. 用户管理 → 4. 项目管理 → 5. 比赛批次管理 → 6. 评审管理 → 7. 系统管理 → 8. 开始管理系统

### 使用方式

- **首次登录**：自动弹出欢迎弹窗，可选择"开始引导"或"暂不需要"
- **重新打开**：点击页面左侧"使用引导"按钮重新打开引导
- **透明度调节**：拖动引导弹窗底部的滑块调节遮罩透明度
- **拖拽移动**：按住引导弹窗顶部的拖拽手柄可移动弹窗位置

## 开发规范

- 遵循 RESTful API 设计规范
- 前端使用 Composition API 风格
- 代码注释使用中文
- 提交信息清晰描述改动内容

## 常见问题

### 1. 数据库连接失败

**现象**：启动后端时提示数据库连接失败

**解决**：
1. 检查 MySQL 服务是否已启动
2. 确认数据库 `innovation_competition` 已创建
3. 检查 `.env` 文件中的 `DATABASE_URL` 配置
4. 确认用户名和密码正确

### 2. 前端跨域问题

**现象**：前端请求后端 API 时报跨域错误

**解决**：
- 后端已配置 Flask-CORS，默认允许所有来源
- 检查后端服务是否正常运行
- 确认前端请求的 API 地址正确

### 3. 文件上传失败

**现象**：上传文件时提示失败

**解决**：
1. 检查文件类型是否在支持列表中
2. 确认文件大小不超过 4GB
3. 检查 `backend/uploads` 目录是否有写入权限
4. 确认项目目录 `project_<id>` 已创建

### 4. JWT 认证失败

**现象**：API 返回 401 未授权

**解决**：
1. 检查请求头是否包含 `Authorization: Bearer <token>`
2. 确认 token 未过期
3. 重新登录获取新 token

### 5. 引导系统不显示

**现象**：登录后没有弹出引导

**解决**：
1. 清除浏览器 localStorage 中的 `guide_completed` 和 `guide_skipped`
2. 刷新页面重新登录
3. 检查浏览器控制台是否有错误

## 扩展开发

### 接入真实 AI API

当前 AI 功能使用 Mock 数据，如需接入真实 AI：

1. 在 `backend/services/ai_service.py` 中替换生成逻辑
2. 添加 API Key 配置到 `.env` 文件
3. 调用 OpenAI / 文心一言 / 通义千问 等 API

示例：
```python
import openai

def generate_project_summary(project_info):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"生成项目简介: {project_info}"}]
    )
    return response.choices[0].message.content
```

### 添加新角色

1. 在 `backend/models/user.py` 的 `VALID_ROLES` 中添加新角色
2. 在 `frontend/src/stores/user.js` 中添加角色判断方法
3. 在 `frontend/src/router/index.js` 中添加角色路由配置
4. 在 `frontend/src/stores/guide.js` 中添加角色引导步骤

## 许可证

MIT License
