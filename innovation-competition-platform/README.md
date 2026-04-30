# 高校创新创业竞赛服务平台

> University Innovation and Entrepreneurship Competition Service Platform

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题等多元化功能。

平台集成了 **Live2D 虚拟形象「火花」**、**语音交互**、**AI 智能对话**等特色功能，为用户提供沉浸式智能辅助体验。

---

## 技术栈

### 前端

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | ^3.5.32 | 渐进式 JavaScript 框架（Composition API） |
| Vite | ^8.0.10 | 下一代前端构建工具 |
| Element Plus | ^2.13.7 | 基于 Vue 3 的组件库 |
| @element-plus/icons-vue | ^2.3.2 | Element Plus 图标库 |
| Pinia | ^3.0.4 | Vue 状态管理方案 |
| Vue Router | ^5.0.6 | 前端路由管理 |
| Axios | ^1.15.2 | HTTP 客户端 |
| ECharts | ^6.0.0 | 数据可视化图表库 |
| marked | ^18.0.2 | Markdown 渲染库（AI 输出格式化） |
| Live2D Widget | - | Live2D 看板娘组件（CDN + 本地 SDK） |

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| Flask | 3.0.3 | 轻量级 Web 框架 |
| Flask-SQLAlchemy | 3.1.1 | ORM 数据库工具 |
| Flask-Migrate | 4.0.7 | 数据库迁移工具 |
| Flask-JWT-Extended | 4.6.0 | JWT 认证（Access 24h / Refresh 7d） |
| Flask-CORS | 4.0.1 | 跨域支持 |
| PyMySQL | 1.1.1 | MySQL 驱动 |
| cryptography | 42.0.8 | 加密库 |
| python-dotenv | 1.0.1 | 环境变量管理 |
| Werkzeug | 3.0.3 | WSGI 工具库 |
| volcengine-python-sdk[ark] | - | 火山方舟 AI SDK |
| opencc-python-reimplemented | - | 简繁转换（ASR 结果处理） |
| langchain / langchain-core | - | AI 编排框架 |
| websockets | - | WebSocket 客户端（实时语音对话 / ASR） |
| requests | - | HTTP 请求库（TTS 合成） |
| MySQL | 8.0+ | 关系型数据库 |

---

## 特色功能

### Live2D 虚拟形象「火花」

- 全局浮动 Live2D 看板娘，固定在页面右下角（通过 `Live2dWidget.vue` 组件 + `MainLayout.vue` 集成）
- 10 种基础表情（黑脸 / 脸红爱心 / 生气 / 晕 / ＞＜ / 0.0 / 星星眼 / 流泪 / 捧心 / 要饭）+ 2 种叠加效果（月卡 / 水印）
- AI 对话时自动切换表情（基于关键词的情绪检测：开心 / 害羞 / 生气 / 难过 / 晕 / 惊讶）
- 语音朗读时口型驱动动画（正弦波模拟 + 文本长度驱动）
- 可拖拽、可隐藏、可切换表情
- 表情 / 情绪联动逻辑抽取为共享 composable（`useLive2d.js`）
- 组件卸载时完整清理（CSS link / DOM 元素 / 全局变量），避免内存泄漏

### AI 智能对话

- 基于火山方舟大模型（doubao-seed-1-6-251015）的真实 AI 对话
- 支持 SSE 流式输出，打字机效果（`/api/ai/chat/stream`）
- 会话管理（6 轮上下文记忆，6 小时 TTL，自动清理过期会话）
- 智能回答清洗（过滤思考过程、去重、提取最终答案标记后的内容、半文重复检测）
- 快捷问题按钮（分析项目创新性 / 商业计划书 / 竞赛评审 / 团队组建）
- AI 助手页面双标签页设计：**AI 分析工具** + **AI 对话**

### 语音交互

- Chrome / Edge：Web Speech API 浏览器原生语音识别（`webkitSpeechRecognition`）
- Firefox：录音上传后端 ASR（豆包 ASR 优先 / faster-whisper 回退）
- TTS 语音合成（火山 TTS HTTP API + 浏览器 SpeechSynthesis 双通道）
- 语音识别结果自动繁转简（OpenCC）
- 可拖拽语音对话面板（`VoiceChat.vue`，位置持久化到 localStorage）
- 深色毛玻璃主题，可折叠 / 展开

### AI 分析工具

- 项目简介生成（AI 驱动，Markdown 格式输出，AI 失败时回退到模板）
- 商业计划书建议（AI 驱动）
- 风险分析（AI 驱动）
- AI 输出结果 Markdown 渲染（marked 库）+ 一键复制 + 朗读

### 火山实时语音对话

- 通过 WebSocket 连接火山实时语音对话服务（`volc_realtime_bridge.py`）
- 自定义二进制协议编解码（`volc_realtime_protocol.py`）
- 支持 Gzip 压缩的 JSON 序列化
- 文本输入模式，流式回复输出
- 可配置发音人、bot 名称、系统角色、说话风格

### 全局引导系统

- 首次登录引导（`GuideSystem.vue`）
- 高亮指引 + 拖拽弹窗
- 引导状态持久化（Pinia `guide.js`）

### 双模式布局

- 平台页面（首页 / 竞赛广场 / 训练营等）：无侧边栏，顶部导航
- 工作台页面（项目 / 评审 / 管理等）：左侧边栏 + 顶部导航
- 侧边栏可折叠，响应式适配

---

## 项目结构

```
innovation-competition-platform/
├── backend/                          # Flask 后端
│   ├── app.py                        # 应用入口（应用工厂模式）
│   ├── config.py                     # 配置文件（Development/Production/Testing）
│   ├── extensions.py                 # 扩展初始化（db/migrate/jwt/cors）
│   ├── seed.py                       # 测试数据初始化脚本（含海报生成）
│   ├── seed_competitions.py          # 竞赛数据种子脚本
│   ├── .env                          # 环境变量（本地开发，含 AI/ASR/TTS 配置）
│   ├── .env.example                  # 环境变量模板
│   ├── requirements.txt              # Python 依赖
│   ├── test_all_api.py               # API 测试脚本
│   ├── test_file_api.py              # 文件接口测试
│   ├── test_task_api.py              # 任务接口测试
│   │
│   ├── models/                       # 数据模型（12 个）
│   │   ├── user.py                   # 用户信息
│   │   ├── competition.py            # 竞赛信息
│   │   ├── competition_track.py      # 竞赛赛道
│   │   ├── competition_registration.py # 竞赛报名
│   │   ├── registration_member.py    # 报名队员
│   │   ├── registration_material.py  # 报名材料
│   │   ├── project.py                # 项目信息
│   │   ├── project_member.py         # 项目成员
│   │   ├── project_file.py           # 项目文件
│   │   ├── project_task.py           # 项目任务
│   │   ├── review.py                 # 评审记录
│   │   └── ai_record.py             # AI 使用记录
│   │
│   ├── routes/                       # API 路由（13 个蓝图）
│   │   ├── auth.py                   # /api/auth    认证接口
│   │   ├── user.py                   # /api/users   用户接口
│   │   ├── project.py                # /api/projects 项目接口
│   │   ├── member.py                 # /api         成员接口
│   │   ├── file.py                   # /api         文件接口
│   │   ├── material.py               # /api/materials 材料接口
│   │   ├── team.py                   # /api/teams   团队接口
│   │   ├── task.py                   # /api         任务接口
│   │   ├── review.py                 # /api         评审接口
│   │   ├── dashboard.py              # /api/dashboard 看板接口
│   │   ├── ai.py                     # /api/ai      AI 接口（聊天/语音/ASR/TTS/分析/表情/健康）
│   │   ├── competition.py            # /api         竞赛接口
│   │   └── registration.py           # /api         报名接口
│   │
│   ├── services/                     # 业务逻辑
│   │   ├── ai_service.py             # AI 核心（火山方舟 SDK + 会话管理 + 流式输出 + 回答清洗）
│   │   ├── tts_service.py            # TTS 语音合成（火山 TTS HTTP API + 文件缓存 + 缓存统计/清理）
│   │   ├── volc_realtime_bridge.py   # 火山实时语音对话桥（WebSocket + 流式回复 + 回答清洗）
│   │   └── volc_realtime_protocol.py # 火山实时语音二进制协议（编解码 + Gzip）
│   │
│   ├── utils/                        # 工具函数
│   │   ├── response.py               # 统一响应格式（success/error）
│   │   └── decorators.py             # 装饰器
│   │
│   ├── uploads/                      # 文件上传目录
│   │   └── competition_posters/      # 竞赛海报（seed.py 自动生成）
│   └── migrations/                   # 数据库迁移
│
├── frontend/                         # Vue 3 前端
│   ├── package.json                  # 依赖配置
│   ├── vite.config.js                # Vite 配置（代理 /api + /uploads -> localhost:5000）
│   ├── index.html                    # HTML 入口（标题：创新创业竞赛服务平台）
│   │
│   ├── public/
│   │   ├── live2d/                   # Live2D 模型资源
│   │   │   ├── huahuo/              # 「火花」模型
│   │   │   │   ├── 火花.model3.json  # 模型配置
│   │   │   │   ├── 火花.moc3         # 模型数据
│   │   │   │   ├── 火花.physics3.json # 物理引擎
│   │   │   │   ├── 火花.cdi3.json    # 参数定义
│   │   │   │   ├── icon.png          # 模型图标
│   │   │   │   ├── 按键设置说明.png    # 按键说明图
│   │   │   │   ├── Expressions/      # 12 个表情文件
│   │   │   │   ├── Motions/          # 2 个动作文件（循环/睡觉）
│   │   │   │   └── 火花.4096/        # 高清纹理
│   │   │   ├── huahuo-clean/         # 清理版模型（备用）
│   │   │   └── huahuo-packages.json  # 模型包配置
│   │   └── live2d-widget-dist/       # Live2D Widget SDK
│   │       ├── chunk/                # SDK 分块
│   │       ├── autoload.js           # 自动加载脚本
│   │       ├── waifu-huahuo.json     # 看板娘配置
│   │       ├── waifu-huahuo.clean.json # 清理版配置
│   │       ├── waifu-tips.js         # 看板娘逻辑
│   │       ├── waifu-tips.json       # 看板娘提示语
│   │       └── waifu.css             # 看板娘样式
│   │
│   └── src/
│       ├── main.js                   # 应用入口（Element Plus 全量注册）
│       ├── App.vue                   # 根组件（路由视图 + GuideSystem）
│       ├── style.css                 # 全局基础样式
│       │
│       ├── api/                      # API 接口封装（11 个模块）
│       │   ├── request.js            # Axios 基础配置（拦截器/Token/错误处理）
│       │   ├── auth.js               # 认证 API
│       │   ├── project.js            # 项目 API
│       │   ├── member.js             # 成员 API
│       │   ├── file.js               # 文件 API
│       │   ├── task.js               # 任务 API
│       │   ├── review.js             # 评审 API
│       │   ├── dashboard.js          # 看板 API
│       │   ├── competition.js        # 竞赛 API
│       │   ├── registration.js       # 报名 API
│       │   └── ai.js                 # AI API（聊天/语音/ASR/TTS/流式/分析）
│       │
│       ├── components/               # 公共组件
│       │   ├── GuideSystem.vue       # 全局引导系统（首次登录引导/高亮/拖拽弹窗）
│       │   ├── Live2dWidget.vue      # Live2D 看板娘组件（表情/口型/情绪联动/完整清理）
│       │   ├── VoiceChat.vue         # 语音交互面板（流式对话/语音识别/TTS/可拖拽/深色毛玻璃）
│       │   └── HelloWorld.vue        # 示例组件
│       │
│       ├── composables/              # 组合函数
│       │   └── useLive2d.js          # Live2D 表情/情绪联动工具（detectEmotionByText/getExpressionByEmotion/notifyLive2dHook）
│       │
│       ├── layouts/
│       │   └── MainLayout.vue        # 主布局（双模式：平台页无侧边栏/工作台有侧边栏 + Live2D 集成）
│       │
│       ├── router/
│       │   └── index.js              # 路由配置（公共/学生/教师/评委/管理员/平台/通用路由 + 守卫）
│       │
│       ├── stores/                   # Pinia 状态管理
│       │   ├── user.js               # 用户状态（token/userInfo/角色权限/初始化）
│       │   └── guide.js              # 引导系统状态
│       │
│       ├── styles/
│       │   ├── design-system.css     # 设计系统变量（Cyan 主色调/暗色侧边栏/暗黑模式预留）
│       │   └── global.css            # 全局样式（Element Plus 覆盖/滚动条/过渡动画/布局类）
│       │
│       └── views/                    # 页面视图（42 个 Vue 文件）
│           ├── ai-assistant/         # AI 助手（双标签页：分析工具 + 对话）
│           │   └── index.vue
│           ├── admin/                # 管理员页面（5 个）
│           │   ├── users.vue         # 用户管理
│           │   ├── projects.vue      # 项目管理
│           │   ├── competitions.vue  # 竞赛管理（比赛批次）
│           │   ├── RegistrationManagement.vue # 报名管理
│           │   └── reviews.vue       # 评审管理
│           ├── competitions/         # 竞赛管理
│           │   └── index.vue
│           ├── dashboard/            # 工作台（5 个角色看板）
│           │   ├── index.vue         # 看板主页（根据角色动态加载）
│           │   ├── student.vue       # 学生看板
│           │   ├── teacher.vue       # 教师看板
│           │   ├── judge.vue         # 评委看板
│           │   └── admin.vue         # 管理员看板
│           ├── error/
│           │   └── 404.vue           # 404 页面
│           ├── login/                # 登录注册
│           │   ├── index.vue         # 登录页（含快速登录提示）
│           │   └── register.vue      # 注册页
│           ├── materials/
│           │   └── index.vue         # 材料管理
│           ├── portal/               # 平台页面（9 个，无侧边栏）
│           │   ├── PortalHome.vue    # 平台首页
│           │   ├── CompetitionSquare.vue # 竞赛广场
│           │   ├── CompetitionDetail.vue # 竞赛详情
│           │   ├── CompetitionRegister.vue # 竞赛报名
│           │   ├── MyRegistrations.vue # 我的赛事
│           │   ├── TrainingCamps.vue # 训练营
│           │   ├── Courses.vue       # 在线课程
│           │   ├── IndustryTopics.vue # 产业命题
│           │   └── Certificates.vue  # 证书成果
│           ├── projects/             # 项目页面（9 个）
│           │   ├── my-projects.vue   # 我的项目
│           │   ├── create.vue        # 创建项目
│           │   ├── detail.vue        # 项目详情
│           │   ├── edit.vue          # 编辑项目
│           │   ├── members.vue       # 团队成员
│           │   ├── files.vue         # 项目材料
│           │   ├── tasks.vue         # 任务进度
│           │   ├── guide-projects.vue # 指导项目
│           │   └── index.vue         # 项目列表
│           ├── reviews/              # 评审页面（5 个）
│           │   ├── pending.vue       # 待评审项目
│           │   ├── history.vue       # 评审记录
│           │   ├── detail.vue        # 评审详情
│           │   ├── index.vue         # 评审列表
│           │   └── teacher-review.vue # 项目审核
│           ├── tasks/
│           │   └── index.vue         # 任务列表
│           └── teams/
│               └── index.vue         # 团队列表
│
├── image/                            # 项目截图
│   └── README/
└── README.md
```

---

## 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建环境 |
| MySQL | 8.0+ | 关系型数据库 |
| ffmpeg | - | 音频格式转换（ASR 功能需要，需加入系统 PATH） |

---

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd innovation-competition-platform
```

### 2. MySQL 数据库初始化

```sql
CREATE DATABASE IF NOT EXISTS innovation_competition
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，修改数据库连接信息和 AI API 配置
```

`.env` 文件完整配置项：

```env
# Flask 配置
SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=1

# MySQL 数据库配置
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4

# JWT 配置
# Access Token 有效期：24 小时 / Refresh Token 有效期：7 天
JWT_SECRET_KEY=your-jwt-secret-key

# AI 对话 - 火山方舟
ARK_API_KEY=your-ark-api-key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
ARK_MODEL=doubao-seed-1-6-251015
VOICE_TEMPERATURE=0.4

# 实时语音对话 - volc.speech.dialog
VOICE_REALTIME_APP_ID=your-app-id
VOICE_REALTIME_APP_KEY=your-app-key
VOICE_REALTIME_TOKEN=your-token
VOICE_REALTIME_RESOURCE_ID=volc.speech.dialog
VOICE_REALTIME_UID=huahuo-web
VOICE_REALTIME_DIALOG_ADDRESS=wss://openspeech.bytedance.com
VOICE_REALTIME_DIALOG_URI=/api/v3/realtime/dialogue
VOICE_REALTIME_SPEAKER=zh_male_yunzhou_jupiter_bigtts
VOICE_REALTIME_BOT_NAME=火花
VOICE_REALTIME_INPUT_MOD=text

# 语音识别 ASR
ASR_PROVIDER=doubao
DOUBAO_ASR_WS_URL=wss://openspeech.bytedance.com/api/v3/sauc/bigmodel
DOUBAO_ASR_APP_ID=your-asr-app-id
DOUBAO_ASR_ACCESS_TOKEN=your-asr-access-token
DOUBAO_ASR_SECRET_KEY=your-asr-secret-key
DOUBAO_ASR_RESOURCE_ID=volc.bigasr.sauc.duration
DOUBAO_ASR_MODEL_NAME=bigmodel
DOUBAO_ASR_FORMAT=wav
DOUBAO_ASR_RATE=16000
DOUBAO_ASR_BITS=16
DOUBAO_ASR_CHANNEL=1
DOUBAO_ASR_LANGUAGE=zh-CN
```

### 4. 后端启动

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

### 5. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务默认运行在 http://localhost:5173

### 6. 初始化测试数据

```bash
cd backend
python seed.py
```

seed.py 会自动创建：
- 8 个测试用户（4 种角色）
- 10 个竞赛（含赛道、海报自动生成）
- 2 个项目
- 8 条报名记录（含队员信息）

---

## 后端配置详情

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SQLALCHEMY_ENGINE_OPTIONS.pool_size` | 10 | 数据库连接池大小 |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_recycle` | 3600 | 连接回收时间（秒） |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_pre_ping` | True | 连接前检测可用性 |
| `JWT_ACCESS_TOKEN_EXPIRES` | 24 小时 | Access Token 有效期 |
| `JWT_REFRESH_TOKEN_EXPIRES` | 7 天 | Refresh Token 有效期 |
| `MAX_CONTENT_LENGTH` | 4 GB | 文件上传大小限制 |
| `DEFAULT_PAGE_SIZE` | 10 | 默认分页大小 |
| `MAX_PAGE_SIZE` | 100 | 最大分页大小 |
| `UPLOAD_FOLDER` | backend/uploads | 文件上传目录 |
| `ALLOWED_EXTENSIONS` | png/jpg/doc/pdf/mp4/zip 等 | 允许上传的文件类型 |

---

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

---

## API 接口文档

### 认证接口 `/api/auth`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/auth/login` | POST | 用户登录（返回 JWT Token） |
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/refresh` | POST | 刷新 Token |

### 用户接口 `/api/users`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/users/profile` | GET | 获取当前用户信息 |
| `/api/users/profile` | PUT | 更新用户信息 |

### 竞赛接口 `/api/competitions`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/competitions` | GET | 获取竞赛列表 |
| `/api/competitions/:id` | GET | 获取竞赛详情 |
| `/api/competitions` | POST | 创建竞赛（管理员） |

### 项目接口 `/api/projects`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/projects` | GET | 获取项目列表（按角色过滤） |
| `/api/projects/:id` | GET | 获取项目详情 |
| `/api/projects` | POST | 创建项目 |
| `/api/projects/:id` | PUT | 更新项目 |

### AI 分析工具 `/api/ai`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/project-summary` | POST | 生成项目简介（AI 驱动，失败回退模板） |
| `/api/ai/business-plan-advice` | POST | 商业计划书建议（AI 驱动，失败回退模板） |
| `/api/ai/risk-analysis` | POST | 风险分析（AI 驱动，失败回退模板） |
| `/api/ai/records` | GET | AI 使用记录 |

### AI 对话 `/api/ai`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/chat` | POST | 文本聊天（非流式） |
| `/api/ai/chat/stream` | POST | 文本聊天（SSE 流式，text/event-stream） |
| `/api/ai/voice/chat/stream` | POST | 语音聊天（SSE 流式，优先火山实时语音，回退文本模型） |

**SSE 流式响应协议**：

```
sessionId:<session-id>     # 首行返回会话 ID
delta:<text-chunk>         # 增量文本
error:<error-message>      # 错误信息
done:1                     # 流结束标记
```

### 语音交互 `/api/ai`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/asr` | POST | 语音识别（multipart/form-data，豆包 ASR / faster-whisper 回退） |
| `/api/ai/tts/synthesize` | POST | TTS 语音合成（火山 TTS，返回音频 URL） |
| `/api/ai/tts/audio/<filename>` | GET | 获取合成音频文件（MP3） |
| `/api/ai/voice/config` | GET | 语音配置信息（发音人/bot 名称/输入模式） |

### Live2D / 健康 `/api/ai`

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/ai/expressions` | GET | 获取表情列表（base 10 个 + overlay 2 个） |
| `/api/ai/model-info` | GET | 获取 Live2D 模型信息（名称/路径） |
| `/api/ai/health` | GET | AI 服务健康检查（chat_configured / voice_realtime_configured / model） |

### 其他接口

| 接口前缀 | 说明 |
|----------|------|
| `/api/dashboard` | 数据看板（统计信息） |
| `/api/teams` | 团队管理 |
| `/api/materials` | 材料管理 |
| `/api/` | 成员 / 文件 / 任务 / 评审 / 报名等 |

### 系统接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/health` | GET | 系统健康检查（数据库连接状态） |
| `/uploads/<path:filename>` | GET | 静态文件访问（上传文件） |

---

## 路由配置

### 公共路由（无需登录）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | login/index.vue | 登录页 |
| `/register` | login/register.vue | 注册页 |

### 平台页面（所有角色，无侧边栏）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/portal` | portal/PortalHome.vue | 平台首页 |
| `/competitions` | portal/CompetitionSquare.vue | 竞赛广场 |
| `/competitions/:id` | portal/CompetitionDetail.vue | 竞赛详情 |
| `/training-camps` | portal/TrainingCamps.vue | 训练营 |
| `/courses` | portal/Courses.vue | 在线课程 |
| `/industry-topics` | portal/IndustryTopics.vue | 产业命题 |

### 通用路由（所有角色）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/dashboard` | dashboard/index.vue | 工作台（按角色加载不同看板） |
| `/ai-assistant` | ai-assistant/index.vue | AI 项目助手（分析工具 + 对话） |
| `/projects/:id` | projects/detail.vue | 项目详情 |
| `/projects/:id/edit` | projects/edit.vue | 编辑项目 |
| `/projects/:id/members` | projects/members.vue | 团队成员 |
| `/projects/:id/files` | projects/files.vue | 项目材料 |
| `/projects/:id/tasks` | projects/tasks.vue | 任务进度 |
| `/reviews/:id` | reviews/detail.vue | 评审详情 |

### 学生专属路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/my-projects` | projects/my-projects.vue | 我的项目 |
| `/create-project` | projects/create.vue | 创建项目 |
| `/competitions/:id/register` | portal/CompetitionRegister.vue | 竞赛报名 |
| `/my-registrations` | portal/MyRegistrations.vue | 我的赛事 |
| `/certificates` | portal/Certificates.vue | 证书成果 |

### 教师专属路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/guide-projects` | projects/guide-projects.vue | 指导项目 |
| `/project-review` | reviews/teacher-review.vue | 项目审核 |

### 评委专属路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/pending-reviews` | reviews/pending.vue | 待评审项目 |
| `/review-history` | reviews/history.vue | 评审记录 |

### 管理员专属路由

| 路径 | 组件 | 说明 |
|------|------|------|
| `/user-management` | admin/users.vue | 用户管理 |
| `/project-management` | admin/projects.vue | 项目管理 |
| `/competition-management` | competitions/index.vue | 比赛批次管理 |
| `/registration-management` | admin/RegistrationManagement.vue | 报名管理 |
| `/review-management` | admin/reviews.vue | 评审管理 |

---

## 数据库模型

| 模型 | 说明 | 主要字段 |
|------|------|----------|
| User | 用户信息 | username, password_hash, role, real_name, email, is_active |
| Competition | 竞赛信息 | name, description, organizer, category, level, status, start_date, end_date, registration_start, registration_end, competition_start, competition_end, tags, target_audience, requirements, awards, schedule, poster_url, registration_count |
| CompetitionTrack | 竞赛赛道 | competition_id, name, description, team_min, team_max, material_requirements |
| CompetitionRegistration | 竞赛报名 | competition_id, track_id, leader_id, team_name, school, college, major, teacher_name, teacher_phone, contact_phone, contact_email, status, remark, submitted_at |
| RegistrationMember | 报名队员 | registration_id, name, student_no, college, major, role_in_team |
| RegistrationMaterial | 报名材料 | registration_id, material_type, file_name, file_path |
| Project | 项目信息 | name, description, status, stage, track, category, leader_id, teacher_id, competition_id, progress |
| ProjectMember | 项目成员 | project_id, user_id, member_name, role_in_project, responsibility |
| ProjectFile | 项目文件 | project_id, filename, original_name, file_type, material_type, file_size, storage_path, uploader_id |
| ProjectTask | 项目任务 | project_id, title, description, assignee_id, status, priority, deadline, completed_at |
| Review | 评审记录 | project_id, judge_id, innovation_score, feasibility_score, market_score, team_score, business_score, technology_score, presentation_score, total_score, comment |
| AiRecord | AI 使用记录 | user_id, project_id, type, prompt, result |

---

## 用户角色

| 角色 | 标识 | 说明 | 侧边栏菜单 |
|------|------|------|------------|
| 学生 | `student` | 项目负责人 / 团队成员 | 工作台、我的赛事、我的项目、创建项目、训练营、在线课程、产业命题、证书成果、AI 助手 |
| 指导老师 | `teacher` | 项目指导 | 工作台、指导项目、项目审核、训练营、在线课程、产业命题、AI 助手 |
| 评委 | `judge` | 项目评审 | 工作台、待评审项目、评审记录、AI 助手 |
| 管理员 | `admin` | 系统管理 | 工作台、比赛批次管理、报名管理、项目管理、评审管理、用户管理、数据看板、AI 助手 |

---

## 开发规范

- 遵循 RESTful API 设计规范
- 前端使用 Composition API 风格（`<script setup>`）
- 代码注释使用中文
- 提交信息清晰描述改动内容
- 共享逻辑抽取为 composable（`src/composables/`）
- 统一响应格式：`{ code, data, message }`
- AI 回答清洗逻辑前后端一致（`sanitize_answer_text`）
- Live2D 表情 / 情绪联动通过 `window.__voiceLive2dHooks` 和 `window.__syncExpressionState` 全局桥接

---

## 常见问题

### 1. 数据库连接失败

1. 检查 MySQL 服务是否已启动
2. 确认数据库 `innovation_competition` 已创建
3. 检查 `.env` 文件中的 `DATABASE_URL` 配置
4. 确认用户名和密码正确

### 2. AI 对话失败

1. 检查 `.env` 中的 `ARK_API_KEY` 是否正确
2. 确认火山方舟 API 可访问
3. 检查网络连接
4. 访问 `/api/ai/health` 查看配置状态

### 3. Live2D 模型加载失败

1. 确认 `frontend/public/live2d/huahuo/` 目录存在
2. 检查模型文件完整性（火花.model3.json / 火花.moc3 / 火花.physics3.json）
3. 清除浏览器缓存重试
4. 检查浏览器控制台是否有 CORS 或 MIME 类型错误
5. 确认 Vite 代理配置正确（`/api` 和 `/uploads` 代理到后端）

### 4. 语音识别不可用

1. Chrome / Edge 浏览器原生支持 Web Speech API
2. Firefox 需要后端 ASR 服务，检查 `.env` 中的 ASR 配置
3. 确保使用 HTTPS 或 localhost（麦克风权限要求）
4. 检查 ffmpeg 是否已安装并加入系统 PATH（音频格式转换需要）

### 5. 前端构建失败

1. 确认 Node.js 版本 >= 18
2. 删除 `node_modules` 后重新 `npm install`
3. 检查是否有语法错误（如括号表达式中的尾随逗号）
4. 确认 `useLive2d.js` 中使用数组而非括号表达式

### 6. TTS 语音合成失败

1. 检查 `.env` 中的 `VOICE_REALTIME_TOKEN` 和 `VOICE_REALTIME_APP_ID` 是否正确
2. 确认火山 TTS API 可访问
3. 检查 `backend/services/tts_cache/` 目录是否有写入权限

---

## 版本变更记录

### v2.0.0 - 2026-04-30（当前版本）

> 从 my_huahuo 项目集成 Live2D 形象、语音交互、AI 大模型等核心功能

#### 新增功能

- **Live2D 虚拟形象「火花」**：全局浮动看板娘组件（`Live2dWidget.vue`），10 种基础表情 + 2 种叠加效果，AI 对话时自动表情切换，语音朗读口型驱动
- **AI 智能对话**：基于火山方舟大模型（doubao-seed-1-6-251015）的真实 AI 对话，SSE 流式输出，会话管理（6 轮上下文记忆），智能回答清洗
- **语音交互面板**：`VoiceChat.vue` 可拖拽浮动面板，Chrome / Edge 原生语音识别 + Firefox 录音上传 ASR，TTS 语音合成
- **AI 分析工具升级**：项目简介 / 商业计划书 / 风险分析从 Mock 模板升级为 AI 驱动生成，AI 失败时自动回退到模板
- **Markdown 渲染**：AI 输出结果使用 marked 库渲染 Markdown，支持表格 / 列表 / 代码块等
- **火山实时语音对话**：`volc_realtime_bridge.py` + `volc_realtime_protocol.py`，WebSocket 连接火山实时语音服务
- **TTS 语音合成服务**：`tts_service.py`，火山 TTS HTTP API + 文件缓存 + 缓存统计 / 清理
- **AI 健康检查**：`/api/ai/health` 端点，查看聊天 / 语音配置状态
- **共享 composable**：`useLive2d.js` 提取表情 / 情绪联动逻辑，消除组件间重复代码
- **竞赛海报自动生成**：`seed.py` 中集成 Pillow 海报生成，按竞赛类别自动配色
- **报名管理增强**：报名记录包含学校 / 学院 / 专业 / 指导老师 / 联系方式等完整信息

#### 后端变更

- `ai_service.py`：完全重写，从 Mock 模板替换为火山方舟 SDK 真实 AI 调用，新增会话管理 / 流式输出 / 回答清洗（过滤思考过程 / 去重 / 半文重复检测 / 最终答案提取）
- `ai.py` 路由：新增 9 个 API 端点（chat / chat/stream / voice/chat/stream / asr / tts/synthesize / tts/audio / voice/config / expressions / model-info / health）
- `tts_service.py`：新增火山 TTS 语音合成服务（HTTP API + MD5 缓存键 + 7 天缓存 TTL + 缓存统计 / 清理）
- `volc_realtime_bridge.py`：新增火山实时语音对话桥（WebSocket + 会话管理 + 流式回复 + 回答清洗）
- `volc_realtime_protocol.py`：新增火山实时语音二进制协议编解码（Gzip 压缩）
- `requirements.txt`：新增 volcengine-python-sdk[ark]、opencc-python-reimplemented、langchain、langchain-core、websockets、requests、cryptography
- `.env`：新增 30+ 个 AI / ASR / TTS 相关配置项
- `config.py`：JWT Token 有效期配置（Access 24h / Refresh 7d）、连接池配置、文件上传限制 4GB
- `seed.py`：增强测试数据生成（10 个竞赛含赛道和海报、8 条报名含队员信息）

#### 前端变更

- `Live2dWidget.vue`：新增 Live2D 看板娘组件（表情控制 / 口型驱动 / 情绪联动 / 完整清理）
- `VoiceChat.vue`：新增语音交互面板组件（流式对话 / 语音识别 / TTS / 可拖拽 / 深色毛玻璃 / 位置持久化）
- `ai-assistant/index.vue`：完全改造为双标签页（AI 分析工具 + AI 对话），集成 Live2D 联动、语音输入、Markdown 渲染
- `MainLayout.vue`：集成 Live2D 看板娘（全局浮动）、双模式布局（平台页 / 工作台）
- `ai.js` API：新增 chatStream / voiceChatStream / uploadAsrAudio / synthesizeTts / getVoiceConfig / getAiHealth / getExpressions / getModelInfo
- `useLive2d.js`：新增共享 composable（detectEmotionByText / getExpressionByEmotion / updateExpressionByText / notifyLive2dHook）
- `index.html`：页面标题从 "frontend" 改为 "创新创业竞赛服务平台"
- `package.json`：新增 marked 依赖、@element-plus/icons-vue
- `vite.config.js`：新增 `/uploads` 代理配置
- `public/live2d/`：新增 Live2D 模型资源（huahuo + huahuo-clean + packages.json）
- `public/live2d-widget-dist/`：新增 Live2D Widget SDK（含 chunk 分块、clean 配置）

#### BUG 修复

- 修复 AI 助手路由角色限制过严：从仅限 `['student']` 改为所有角色 `['student', 'teacher', 'judge', 'admin']`
- 修复 Live2D 组件 `onBeforeUnmount` 清理不完整：增加清理 CSS link、DOM 元素、全局变量（`__expressionControlsState` / `__voiceLive2dHooks` / `__syncExpressionState` / `__live2dModel` / `__applySpeechStateToCore` / `__applyOverlayStateToCore` / `initWidget` / `loadlive2d`）
- 修复 `useLive2d.js` 括号表达式尾随逗号导致 Vite 构建失败：将 `META_LINE_PREFIXES` / `META_LINE_KEYWORDS` / `ANSWER_MARKERS` 从括号表达式改为数组
- 修复 Live2D Widget `initWidget` 参数格式错误：`apiPath` 改为 `cdnPath`

#### 调试验证

- 后端健康检查 `/api/health`：通过（数据库连接正常）
- AI 健康检查 `/api/ai/health`：通过（chat_configured: true, voice_realtime_configured: true）
- 登录功能（admin / admin123）：通过（JWT Token 正确生成）
- Dashboard 数据：通过（8 用户 / 6 项目 / 10 竞赛 / 4 评审）
- AI 流式对话：通过（SSE 流式响应正常）
- Live2D 资源访问：通过（waifu-tips.js / waifu.css / 模型文件均可访问）
- 前端构建：通过（0 错误，2315 模块编译成功）

---

### v1.0.0 - 初始版本

> 基础创新创业竞赛服务平台，AI 功能为 Mock 实现

- 竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分
- 四种角色（学生 / 指导老师 / 评委 / 管理员）
- 竞赛广场、项目工作室、训练营、在线课程、产业命题
- AI 分析工具（Mock 模板实现）
- 全局引导系统
- 双模式布局（平台页无侧边栏 / 工作台有侧边栏）

---

## 许可证

MIT License
