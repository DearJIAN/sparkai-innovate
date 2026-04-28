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
│   ├── models/             # 数据模型
│   ├── routes/             # API 路由
│   ├── services/           # 业务逻辑
│   ├── utils/              # 工具函数
│   ├── uploads/            # 文件上传目录
│   └── migrations/         # 数据库迁移
│
├── frontend/               # Vue 3 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── api/            # API 接口
│       ├── assets/         # 静态资源
│       ├── components/     # 公共组件
│       ├── layouts/        # 布局组件
│       ├── router/         # 路由配置
│       ├── stores/         # Pinia 状态管理
│       ├── views/          # 页面视图
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

## MVP 核心功能

- [x] 登录注册
- [x] 角色权限控制（基础框架）
- [x] 学生创建和管理创新创业项目（后端 API 完成）
- [x] 项目团队成员管理（后端 API + 前端页面完成）
- [ ] 项目材料上传和下载（图片、Word、PPT、PDF、视频等）
- [ ] 项目任务与阶段进度管理
- [x] 项目提交评审（后端 API 完成）
- [ ] 评委查看项目并评分
- [ ] 学生查看评审结果
- [ ] 管理员查看项目数据看板
- [ ] AI 辅助生成项目简介、商业计划书建议、风险分析

## API 接口文档

### 认证接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户信息（需 JWT） |
| `/api/auth/logout` | POST | 登出（需 JWT） |

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

## 开发规范

- 遵循 RESTful API 设计规范
- 前端使用 Composition API 风格
- 代码注释使用中文
- 提交信息清晰描述改动内容

## 许可证

MIT License
