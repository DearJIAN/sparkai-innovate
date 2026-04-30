# 高校创新创业竞赛服务平台

> University Innovation and Entrepreneurship Competition Service Platform

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题等多元化功能。

平台集成了 **Live2D 虚拟形象「火花」**、**语音交互**、**AI 智能对话**等特色功能，为用户提供沉浸式智能辅助体验。

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Element Plus** - 基于 Vue 3 的组件库
- **Pinia** - Vue 状态管理方案
- **Vue Router** - 前端路由管理
- **Axios** - HTTP 客户端
- **ECharts** - 数据可视化图表库
- **marked** - Markdown 渲染库
- **Live2D Widget** - Live2D 看板娘组件

### 后端
- **Python Flask** - 轻量级 Web 框架
- **Flask-SQLAlchemy** - ORM 数据库工具
- **Flask-Migrate** - 数据库迁移工具
- **Flask-JWT-Extended** - JWT 认证
- **Flask-CORS** - 跨域支持
- **MySQL** - 关系型数据库
- **PyMySQL** - MySQL 驱动
- **python-dotenv** - 环境变量管理
- **volcengine-python-sdk[ark]** - 火山方舟 AI SDK
- **opencc-python-reimplemented** - 简繁转换
- **langchain / langchain-core** - AI 编排框架
- **websockets** - WebSocket 客户端（实时语音对话）

## 特色功能

### Live2D 虚拟形象「火花」
- 全局浮动 Live2D 看板娘，固定在页面右下角
- 10 种基础表情 + 2 种叠加效果（月卡/水印）
- AI 对话时自动切换表情（开心/害羞/生气/难过/晕/惊讶）
- 语音朗读时口型驱动动画
- 可拖拽、可隐藏、可切换表情

### AI 智能对话
- 基于火山方舟大模型（doubao-seed）的真实 AI 对话
- 支持 SSE 流式输出，打字机效果
- 会话管理（6 轮上下文记忆，6 小时 TTL）
- 智能回答清洗（过滤思考过程、去重、提取最终答案）
- 快捷问题按钮

### 语音交互
- Chrome/Edge：Web Speech API 浏览器原生语音识别
- Firefox：录音上传后端 ASR（豆包 ASR / faster-whisper 回退）
- TTS 语音合成（火山 TTS API + 浏览器 SpeechSynthesis）
- 语音识别结果自动繁转简（OpenCC）
- 可拖拽语音对话面板

### AI 分析工具
- 项目简介生成（AI 驱动，Markdown 格式输出）
- 商业计划书建议（AI 驱动）
- 风险分析（AI 驱动）
- AI 输出结果 Markdown 渲染 + 一键复制 + 朗读

## 项目结构

```
innovation-competition-platform/
├── backend/                 # Flask 后端
│   ├── app.py              # 应用入口
│   ├── config.py           # 配置文件
│   ├── .env                # 环境变量（本地开发）
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
│   │   ├── ai.py           # AI 接口（聊天/语音/ASR/TTS/分析）
│   │   ├── competition.py  # 竞赛接口
│   │   └── registration.py # 报名接口
│   ├── services/           # 业务逻辑
│   │   ├── ai_service.py           # AI 服务（火山方舟 + 会话管理 + 流式输出）
│   │   ├── tts_service.py          # TTS 语音合成服务（火山 TTS）
│   │   ├── volc_realtime_bridge.py # 火山实时语音对话桥
│   │   └── volc_realtime_protocol.py # 火山实时语音二进制协议
│   ├── utils/              # 工具函数
│   │   ├── response.py     # 统一响应格式
│   │   └── decorators.py   # 装饰器
│   ├── uploads/            # 文件上传目录
│   └── migrations/         # 数据库迁移
│
├── frontend/               # Vue 3 前端
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── public/
│   │   ├── live2d/                  # Live2D 模型资源
│   │   │   └── huahuo/             # 「火花」模型
│   │   │       ├── 火花.model3.json
│   │   │       ├── 火花.moc3
│   │   │       ├── 火花.physics3.json
│   │   │       ├── 火花.cdi3.json
│   │   │       ├── Expressions/    # 表情文件（12个）
│   │   │       ├── Motions/        # 动作文件
│   │   │       └── 火花.4096/      # 高清纹理
│   │   └── live2d-widget-dist/     # Live2D Widget SDK
│   │       ├── waifu.css
│   │       ├── waifu-tips.js
│   │       ├── autoload.js
│   │       └── waifu-huahuo.json
│   └── src/
│       ├── api/            # API 接口封装
│       │   ├── auth.js
│       │   ├── user.js
│       │   ├── project.js
│       │   ├── ai.js       # AI API（聊天/语音/ASR/TTS/流式）
│       │   └── ...
│       ├── components/     # 公共组件
│       │   ├── GuideSystem.vue
│       │   ├── Live2dWidget.vue   # Live2D 看板娘组件
│       │   └── VoiceChat.vue      # 语音交互面板组件
│       ├── layouts/        # 布局组件
│       │   └── MainLayout.vue     # 主布局（集成 Live2D）
│       ├── router/         # 路由配置
│       ├── stores/         # Pinia 状态管理
│       ├── styles/         # 全局样式
│       ├── views/          # 页面视图
│       │   ├── ai-assistant/     # AI 助手（双标签页：分析工具 + 对话）
│       │   └── ...
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
# 编辑 .env 文件，修改数据库连接信息和 AI API 配置
```

`.env` 文件关键配置：
```env
# 数据库
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4

# AI 对话 - 火山方舟
ARK_API_KEY=your-ark-api-key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=doubao-seed-1-6-251015

# 实时语音对话
VOICE_REALTIME_APP_ID=your-app-id
VOICE_REALTIME_APP_KEY=your-app-key
VOICE_REALTIME_TOKEN=your-token

# 语音识别 ASR
ASR_PROVIDER=doubao
DOUBAO_ASR_APP_ID=your-asr-app-id
DOUBAO_ASR_ACCESS_TOKEN=your-asr-access-token
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

## AI 接口文档

### AI 分析工具

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/project-summary` | POST | 生成项目简介 |
| `/api/ai/business-plan-advice` | POST | 商业计划书建议 |
| `/api/ai/risk-analysis` | POST | 风险分析 |
| `/api/ai/records` | GET | AI 使用记录 |

### AI 对话

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/chat` | POST | 文本聊天（非流式） |
| `/api/ai/chat/stream` | POST | 文本聊天（SSE 流式） |
| `/api/ai/voice/chat/stream` | POST | 语音聊天（SSE 流式，优先火山实时语音） |

### 语音交互

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/asr` | POST | 语音识别（豆包 ASR / faster-whisper） |
| `/api/ai/tts/synthesize` | POST | TTS 语音合成 |
| `/api/ai/tts/audio/<filename>` | GET | 获取合成音频 |
| `/api/ai/voice/config` | GET | 语音配置信息 |

### Live2D

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/expressions` | GET | 获取表情列表 |
| `/api/ai/model-info` | GET | 获取模型信息 |
| `/api/ai/health` | GET | AI 服务健康检查 |

## 平台功能模块

### 侧边栏功能入口（按角色）

| 角色 | 侧边栏菜单 |
|------|-----------|
| 学生 | 工作台、我的赛事、我的项目、创建项目、训练营、在线课程、产业命题、证书成果、AI 项目助手 |
| 老师 | 工作台、指导项目、项目审核、训练营、在线课程、产业命题、AI 项目助手 |
| 评委 | 工作台、待评审项目、评审记录、AI 项目助手 |
| 管理员 | 工作台、比赛批次管理、报名管理、项目管理、评审管理、用户管理、数据看板、AI 项目助手 |

### AI 助手 (/ai-assistant)
- **AI 分析工具**：项目简介生成、商业计划书建议、风险分析
- **AI 对话**：流式聊天、语音输入、快捷问题
- **Live2D 联动**：对话时表情自动切换、语音朗读口型驱动
- **语音交互面板**：可拖拽浮动面板、语音识别、TTS 朗读

### 其他功能模块

详见项目代码中的路由文件和页面组件。

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

### 2. AI 对话失败

**解决**：
1. 检查 `.env` 中的 `ARK_API_KEY` 是否正确
2. 确认火山方舟 API 可访问
3. 检查网络连接

### 3. Live2D 模型加载失败

**解决**：
1. 确认 `frontend/public/live2d/huahuo/` 目录存在
2. 检查模型文件完整性
3. 清除浏览器缓存重试

### 4. 语音识别不可用

**解决**：
1. Chrome/Edge 浏览器原生支持 Web Speech API
2. Firefox 需要后端 ASR 服务，检查 `.env` 中的 ASR 配置
3. 确保使用 HTTPS 或 localhost（麦克风权限要求）

## 许可证

MIT License
