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

- 全局浮动 Live2D 看板娘，支持全屏拖拽（通过 `HuahuoAssistant.vue` 组件 + `MainLayout.vue` 集成）
- 拖拽位置持久化到 localStorage，刷新页面后自动恢复
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
│       ├── assets/                   # 静态资源
│       │   └── images/               # 图片资源
│       │       ├── competitions/     # 竞赛海报图（与比赛名称一对一匹配）
│       │       ├── training-camps/   # 训练营图片
│       │       └── courses/          # 在线课程图片
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
│           ├── portal/               # 平台页面（11 个，无侧边栏）
│           │   ├── PortalHome.vue    # 平台首页
│           │   ├── CompetitionSquare.vue # 竞赛广场
│           │   ├── CompetitionDetail.vue # 竞赛详情
│           │   ├── CompetitionRegister.vue # 竞赛报名
│           │   ├── MyRegistrations.vue # 我的赛事
│           │   ├── TrainingCamps.vue # 训练营
│           │   ├── TrainingCampDetail.vue # 训练营详情
│           │   ├── Courses.vue       # 在线课程
│           │   ├── CourseDetail.vue   # 课程详情
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
| `/training-camps/:id` | portal/TrainingCampDetail.vue | 训练营详情 |
| `/courses` | portal/Courses.vue | 在线课程 |
| `/courses/:id` | portal/CourseDetail.vue | 课程详情 |
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

### v2.10.0 - 2026-05-01（当前版本）

> Live2D拖拽按钮常驻、侧边栏选中状态修复、创建项目快速填充、产业命题承接功能

#### 详情页海报被导航栏遮盖修复

- **顶部间距**：竞赛详情页、训练营详情页、课程详情页统一添加 `padding-top: 64px`，确保封面海报不被固定导航栏遮挡
- **影响范围**：3个详情页组件（CompetitionDetail、TrainingCampDetail、CourseDetail）

#### 竞赛详情页时间安排和奖项设置修复

- **默认数据填充**：competition.value 初始化时即包含完整的默认竞赛数据（AI应用创新设计大赛），不再依赖API返回
- **容错机制**：loadDetail 函数重构，即使 API 请求失败或返回空数据，也会自动生成完整的时间安排（6阶段）、奖项设置（6级）和材料要求
- **智能匹配**：根据竞赛名称和级别自动生成对应的时间线描述、奖项名称和材料类型
- **问题根因**：原代码在 API 返回空数组时 fallback 未正确触发

#### 使用引导按钮支持拖拽+悬浮显示

- **垂直拖拽**：引导重新打开按钮支持沿左侧边缘上下拖拽，拖拽范围限制在 `60px ~ (windowHeight - 60px)`
- **悬浮展开**：默认只显示图标（宽度44px），鼠标悬浮时展开完整文字"使用引导"，带平滑过渡动画
- **视觉优化**：添加阴影、边框发光效果，hover 时增强视觉反馈

#### 竞赛报名表单快速生成功能

- **队伍信息一键填充**：点击"快速生成队伍信息"自动填入队名、学校、学院、专业、指导老师、联系方式等全部字段
- **队员信息一键生成**：点击"快速生成队员信息"自动生成3名测试队员的完整信息（姓名、学号、学院、专业、电话、邮箱）
- **调试友好**：每个步骤都有独立的快速填充栏，带提示文字说明用途

#### Live2D 引导后关闭加载不出来 BUG 修复

- **根因分析**：`onBeforeUnmount` 中删除了 `window.initWidget` 全局函数，导致组件重新挂载时无法初始化 Live2D
- **修复方案**：移除对全局变量和 DOM 元素的破坏性删除操作，改为隐藏 waifu 元素（`display: none`）
- **保留功能**：保留语音识别停止、口型脉冲停止等必要清理逻辑

#### Live2D 全屏拖拽修复

- **事件冲突修复**：`startModelDrag` 添加 `e.stopPropagation()` 防止与 waifu 点击事件冲突
- **手柄定位修复**：CSS 改用 `transform: translateX(-50%) translateY(-100%)` 确保手柄正确显示在 waifu 元素上方
- **视觉效果优化**：手柄添加阴影、圆角、边框发光效果，hover 时颜色变化

#### 导航栏 AI 助手入口删除

- **顶部导航**：从 topNavConfig 中移除 `/ai-assistant` 入口
- **侧边栏**：从 menuGroups 的"工具"分组中移除 AI 项目助手入口
- **活跃状态**：同步清理 isTopNavActive 函数中的 ai-assistant 路由判断

#### 首页下板块背景改为粒子数据流动画

- **Canvas 实现**：使用 HTML5 Canvas + requestAnimationFrame 实现高性能粒子动画
- **数据流效果**：粒子从底部向上流动，带横向摆动（正弦波），模拟数据上升效果
- **粒子样式**：圆形粒子 + 拖尾线条，多色系（蓝/青/紫/绿），大小1-3.5px，透明度0.03-0.15
- **懒加载触发**：通过 IntersectionObserver 在板块进入视口时才启动动画，节省性能
- **响应式**：窗口 resize 时自动重绘，粒子数量根据区域面积动态计算
- **覆盖范围**：功能入口、推荐竞赛、快捷操作三个下板块均启用

#### 竞赛详情页时间安排和奖项设置强制生成

- **问题根因**：API 返回的 schedule/awards/materials 为空数组时，原代码的 fallback 逻辑判断条件 `!competition.value.schedule` 对空数组返回 false，导致 fallback 不触发
- **修复方案**：`loadDetail` 函数中直接移除对 API 返回数组的条件判断，无论 API 返回什么数据，都在最后强制调用 `getScheduleForCompetition` / `getAwardsForCompetition` / `getMaterialsForCompetition` 生成完整数据
- **智能内容**：根据竞赛名称关键词（AI/乡村振兴/电子商务/软件等）和级别（国家级/省级/校级）自动生成匹配的时间线描述、奖项配置和材料要求

#### 竞赛海报裁切修复

- **问题根因**：详情页海报使用 `object-fit: cover` + `max-height: 500px` + `overflow: hidden`，导致海报上下被裁切
- **修复方案**：
  - `object-fit: cover` → `object-fit: contain`：确保海报完整显示，不裁切任何部分
  - 移除 `overflow: hidden`：允许海报自然展开
  - 海报容器背景改为深色 `#1e293b`：contain 模式下两侧留白时显示深色背景更美观
  - `height: auto`：让海报保持原始宽高比

#### Live2D 全屏拖拽优化

- **坐标系修复**：原代码使用 `bottom` 定位 + `origBottom` 计算，导致拖拽时 Y 轴方向相反（向上拖反而向下走）
- **修复方案**：
  - 改为 `top` 定位 + `origTop` 计算，拖拽方向与鼠标移动方向一致
  - `applyModelPosition` 中设置 `bottom: auto; top: xxxpx`，彻底消除坐标系混乱
  - 恢复位置时同样使用 `top` 而非 `bottom`
- **拖拽手柄位置**：从形象顶部改为形象右侧（`left: 320px; bottom: 120px`），圆形按钮设计，更简洁
- **#waifu 样式**：`cursor: grab` → `grabbing` 拖拽时反馈；`position: fixed !important` 确保定位优先级

#### 我的赛事卡片使用海报图

- **问题根因**：`MyRegistrations.vue` 中卡片左侧图片区域使用纯渐变色背景 + 白色文字，不美观
- **修复方案**：
  - 导入与 `CompetitionSquare.vue` 相同的本地竞赛图片映射
  - `getLocalImage` 函数根据 `competitionName` 匹配对应的本地海报图
  - 卡片 `posterStyle` 优先使用本地图片，其次 `poster_url`，最后回退到渐变色
  - 保持与竞赛广场卡片一致的视觉风格

#### 证书与获奖记录查看详情弹窗

- **新增功能**：证书卡片和获奖记录卡片均添加"查看详情"按钮
- **图片弹窗**：点击后弹出 `el-dialog` 显示证书/获奖证书的高清图片
- **图片资源**：将外部证书图片复制到项目 `src/assets/images/certificates/` 目录：
  - 证书：创新创业基础训练营结业证书、AI项目孵化训练营结业证书、商业计划书写作训练营结业证书
  - 获奖：2025大学生创新创业计划训练赛（二等奖）、2025校园电子商务运营挑战赛（三等奖）
- **弹窗设计**：800px 宽度，图片居中显示，`object-fit: contain`，最大高度 600px，带阴影和圆角

#### 首页数据流粒子动画增强 + 烟花效果

- **粒子增强**：
  - 颜色从 4 种扩展到 8 种（新增橙/粉/亮青/金黄）
  - 粒子数量从 `w*h/12000` 增加到 `w*h/8000`，更密集
  - 透明度从 `0.03-0.15` 提升到 `0.15-0.5`，更明显
  - 粒子大小从 `1-3.5px` 增加到 `1.5-4.5px`
  - 添加径向渐变发光效果（`createRadialGradient`），粒子带光晕
- **烟花效果**：
  - 每隔 3-7 秒随机在 Canvas 上半区域生成一次烟花爆炸
  - 每个烟花 20-45 个粒子，向四周散射
  - 粒子受重力影响（`vy += 0.03`），模拟真实抛物线
  - 烟花粒子带发光效果和生命周期衰减（`life/decay`）
  - 多色系烟花，每次随机颜色

#### 竞赛详情页海报宽度占满 + 去掉中央文字

- **问题根因**：海报使用 `object-fit: contain` + `max-height: 560px`，虽然完整显示了海报，但海报宽度没有占满页面，两侧留有大片空白
- **修复方案**：
  - 移除 `max-height: 560px` 限制，改为 `aspect-ratio: 16 / 9`，让海报容器保持 16:9 比例并自动占满全宽
  - `height: auto` + `width: 100%`：海报图片根据容器宽度自动调整高度，保持原始宽高比
  - 海报容器背景改为 `#0f172a` 深色，海报未加载时显示深色背景
  - 去掉海报中央叠加的文字（`poster-fallback-content` 中的标题/主办方等），海报本身已包含这些信息

#### 导航栏与海报间距移除

- **问题根因**：`.competition-detail` 设置了 `padding-top: 64px`，导致导航栏下方与海报顶部之间有 64px 的空白间距
- **修复方案**：移除 `padding-top: 64px`，海报紧贴导航栏底部，视觉更紧凑

#### Live2D 拖拽按钮跟随形象移动

- **问题根因**：拖拽按钮使用固定的 `left: 316px` 定位，形象拖拽后按钮仍留在原地
- **修复方案**：
  - 给拖拽按钮添加 `id="live2d-drag-handle"`
  - `applyModelPosition` 函数中，每次更新形象位置时，同步计算按钮位置：`left = 形象left + 形象宽度 - 4`，`top = 形象top + 形象高度/2 - 16`
  - 恢复位置时同样同步恢复按钮位置
  - 按钮初始位置跟随默认形象位置（`left: 20px` 时按钮在 `316px`）

#### 首页推荐竞赛改用海报封面

- **问题根因**：推荐竞赛卡片使用纯渐变色背景 + 白色竞赛名文字，不美观且遮挡信息
- **修复方案**：
  - 导入与 `CompetitionSquare.vue` 相同的本地竞赛图片映射
  - 卡片海报区域使用 `<img>` 标签显示对应海报，`object-fit: cover`，`aspect-ratio: 16/9`
  - 竞赛名从卡片内部移到下方信息区域，黑色文字显示，避免遮挡海报
  - 标签（级别/分类）放在竞赛名下方，水平排列
  - 无海报时回退到渐变色背景

#### 首页数据流动画改为科幻数字雨风格

- **问题根因**：原有粒子动画元素过多、速度过快、烟花效果喧宾夺主，与页面整体风格不协调
- **修复方案**：改为《黑客帝国》风格的数字雨（Matrix Rain）效果：
  - **列式下落**：将画布分为多列（根据宽度计算），每列独立下落，模拟终端代码滚动
  - **字符集**：使用 0-9、A-F 十六进制数字 + 编程符号（`+ - * / = < > { } [ ]` 等），营造科技感
  - **头部高亮**：每列最前面的 1-3 个字符使用青色（`#22d3ee`）/蓝色（`#0ea5e9`）高亮，后面字符渐变为灰色（`#64748b`）并淡出
  - **拖尾效果**：使用半透明覆盖（`rgba(248,250,252,0.12)`）而非完全清空画布，产生字符拖尾残影
  - **速度控制**：每列速度 `0.3-1.1px/帧`，比原来慢很多，文艺感更强
  - **随机启停**：约 40% 的列初始处于非活跃状态，定时器到期后才重新激活，避免所有列同时滚动
  - **字符闪烁**：每帧有 0.5% 概率随机改变某个字符，模拟数据刷新
  - **水平扫描线**：偶尔出现水平扫描线（4-10秒间隔），带小光点，增强科幻感
  - **整体透明度**：所有字符透明度控制在 `0.03-0.18`，非常淡雅，不干扰前景内容

#### 训练营/课程详情页海报修复

- **问题根因**：训练营和课程详情页海报仍使用旧的 `object-fit: cover` + `max-height: 500px` + `padding-top: 64px`，导致海报裁切且与导航栏有间距
- **修复方案**：
  - 移除 `padding-top: 64px`，海报紧贴导航栏
  - `object-fit: cover` → `object-fit: contain`，海报完整显示不裁切
  - 移除 `max-height` 和 `overflow: hidden`，改为 `aspect-ratio: 16 / 9`
  - 海报容器背景改为 `#0f172a` 深色
  - 与竞赛详情页保持一致的修复方案

#### 数字雨全屏铺满 + 速度加快

- **问题根因**：
  - 数字雨画布放在每个 `portal-section` 内部，受 `max-width: 1400px` 限制，两侧有空白
  - 速度 `0.3-1.1px/帧` 太慢，用户反馈"着实有些慢"
- **修复方案**：
  - **全屏铺满**：改为单个全局画布 `global-rain-canvas`，放在 `portal-page` 最外层，使用 `document.documentElement.scrollWidth/Height` 获取全页面尺寸
  - **动态高度检测**：每帧检测 `document.documentElement.scrollHeight` 变化，自动调整画布高度适应内容变化
  - **速度加快**：下落速度从 `0.3-1.1px/帧` 提升到 `0.8-2.3px/帧`，扫描线速度同步加快
  - **移除旧画布**：删除三个 section 内部的 `data-flow-canvas`，统一由全局画布管理

#### Live2D 拖拽按钮点击对话后不消失

- **问题根因**：拖拽按钮使用 `v-if="loaded && !panelOpen"`，打开对话面板后按钮被销毁，关闭面板后按钮重新创建但位置丢失
- **修复方案**：
  - `v-if` 改为 `v-if="loaded"`，按钮始终存在
  - 添加 `:class="{ 'panel-open': panelOpen }"`，面板打开时通过 CSS `opacity: 0` 隐藏按钮而非销毁
  - 添加 `transition: opacity 0.3s` 实现平滑淡入淡出
  - 面板关闭后按钮自动恢复可见，位置保持跟随形象

#### 侧边栏「我的项目」选中状态 BUG 修复

- **问题根因**：`isMenuActive` 函数中 `/my-projects` 的匹配条件包含了 `/create-project`，导致点击「创建项目」时「我的项目」也处于高亮状态
- **修复方案**：
  - `/create-project` 路由单独精确匹配，只高亮「创建项目」菜单项
  - `/my-projects` 只匹配 `/my-projects` 自身和 `/projects/*` 子路由，不再匹配 `/create-project`
  - 顶部导航栏 `isTopNavActive` 同步修复（保持原有逻辑，因为顶部导航没有独立的「创建项目」入口）

#### 创建项目页面添加一键快速填充

- **新增功能**：在表单底部操作按钮上方添加「快速填充」调试栏
- **填充内容**：
  - 项目名称：从 5 个预设名称中随机选择（智慧校园/AI学习助手/二手交易/区块链学历/创业资源平台）
  - 项目类别：从 5 个类别中随机选择
  - 所属赛道：从 7 个赛道中随机选择
  - 当前阶段：从 5 个阶段中随机选择
  - 项目简介：根据类别和赛道自动生成描述文本
  - 指导老师 ID：随机生成 10000-10099
  - 比赛批次 ID：随机生成 1-10
  - 开始/结束时间：今天起往后 90 天
- **UI 设计**：蓝色虚线边框提示栏，带 MagicStick 图标和说明文字

#### 产业命题卡片底部对齐 + 承接功能完善

- **底部对齐修复**：
  - `.topic-footer` 添加 `min-height: 56px`，统一 footer 高度
  - `.topic-meta` 添加 `align-items: center` 和 `flex: 1`
  - `.meta-item` 添加 `white-space: nowrap`，防止文字换行导致高度不一致
- **承接命题功能**：
  - 点击「承接命题」按钮弹出 `ElMessageBox` 确认对话框，显示命题标题和后续流程说明
  - 确认后显示成功提示，延迟 1 秒跳转到「创建项目」页面
  - 通过 URL query 参数传递产业命题信息（`topic_id`、`topic_title`、`topic_company`），为后续预填充项目信息做准备
  - 取消承接时不执行任何操作

#### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `CompetitionDetail.vue` | 移除 padding-top:64px；海报 aspect-ratio:16/9 占满宽度；去掉 poster-fallback 中央文字 |
| `TrainingCampDetail.vue` | 移除 padding-top:64px；海报 object-fit:contain + aspect-ratio:16/9 |
| `CourseDetail.vue` | 移除 padding-top:64px；海报 object-fit:contain + aspect-ratio:16/9 |
| `HuahuoAssistant.vue` | 拖拽按钮 v-if 改为常驻；panel-open 类控制透明度隐藏；transition 添加 opacity |
| `MainLayout.vue` | isMenuActive 修复：/create-project 独立匹配，/my-projects 不再匹配 /create-project |
| `create.vue` | 添加 quickFillProject 函数；快速填充栏 UI；导入 MagicStick 图标 |
| `IndustryTopics.vue` | 添加 handleAccept 函数；底部对齐样式修复；承接确认弹窗 + 跳转创建项目 |
| `PortalHome.vue` | 导入竞赛图片映射；推荐竞赛卡片改用海报封面；竞赛名移到下方信息区；全局数字雨替换分段画布；速度加快 |

---

### v2.9.0 - 2026-05-01

> 训练营/课程海报修复、数字雨全屏铺满、速度加快

### v2.8.0 - 2026-05-01

> 首页数据流动画改为科幻数字雨风格

### v2.7.0 - 2026-05-01

> 海报宽度占满修复、Live2D拖拽按钮跟随、导航栏间距移除、推荐竞赛海报封面

### v2.6.0 - 2026-05-01

> 竞赛详情数据强制生成、海报裁切修复、Live2D全屏拖拽优化、我的赛事海报图、证书查看详情弹窗、首页烟花数据流

### v2.4.0 - 2026-05-01

> Live2D全屏拖拽、竞赛/训练营/课程详情页完善、导航栏侧边栏补全、首页背景动画补充

#### Live2D形象全屏可拖拽

- **拖拽手柄**：在Live2D形象顶部添加"拖拽移动"手柄，鼠标/触摸均可操作
- **全屏拖拽**：Live2D形象不再固定在左下角，可拖拽到屏幕任意位置
- **位置持久化**：拖拽位置自动保存到localStorage，刷新页面后恢复
- **边界约束**：拖拽时自动限制在可视窗口范围内，不会超出屏幕
- **触摸支持**：同时支持鼠标和触摸屏拖拽操作

#### 竞赛详情页完善

- **时间安排补充**：从简略的2-3项扩展为完整的6阶段时间线（报名启动→报名截止→初赛评审→复赛评审→决赛路演→结果公布与颁奖），每阶段包含详细描述
- **奖项设置补充**：从1项扩展为6级完整奖项体系（特等奖/一等奖/二等奖/三等奖/最佳创意奖/最佳团队奖），每项含具体奖金、证书和附加奖励
- **封面海报修复**：使用本地竞赛海报图片作为详情页顶部封面，替代原来的渐变色占位
- **布局适配**：海报图片使用`object-fit: cover`确保16:9海报完整显示，最大高度500px
- **智能内容生成**：根据竞赛名称和级别自动生成匹配的时间安排、奖项设置和材料要求

#### 训练营详情页开发

- **独立详情页**：从弹窗模式升级为独立页面（`TrainingCampDetail.vue`），路由`/training-camps/:id`
- **完整内容**：包含训练营简介、课程大纲（可展开章节/课时）、学习安排时间线、结业奖励、讲师团队
- **封面海报**：使用本地训练营图片作为顶部封面，与竞赛详情页布局风格一致
- **4大训练营数据**：创新创业基础(24课时)、商业计划书写作(18课时)、路演表达(12课时)、AI项目孵化(32课时)

#### 在线课程详情页开发

- **独立详情页**：从弹窗模式升级为独立页面（`CourseDetail.vue`），路由`/courses/:id`
- **完整内容**：包含课程简介、课程目录（可展开章节/课时）、学习计划时间线、学习成果、课程标签
- **封面海报**：使用本地课程图片作为顶部封面
- **5门课程数据**：创业基础(12h)、市场调研方法(8h)、商业模式设计(10h)、项目路演技巧(6h)、创业法律与知识产权(8h)
- **与训练营区分**：课程侧重知识学习（自主进度、在线考核），训练营侧重实战训练（分阶段、导师辅导、路演答辩）

#### 导航栏和侧边栏补全

- **顶部导航新增**：产业命题、AI助手、证书成果等首页功能入口展示的功能
- **侧边栏新增**：竞赛广场、AI项目助手等入口，新增"工具"分组
- **活跃状态**：所有新增导航项均支持活跃状态检测和高亮显示

#### 首页下板块背景动画

- **功能入口区域**：添加浮动圆形装饰（蓝色+绿色）+ 底部波浪动画 + 点阵动画
- **推荐竞赛区域**：添加浮动圆形装饰（紫色+粉色）+ 底部波浪动画
- **快捷操作区域**：添加浮动圆形装饰（橙色+红色）+ 点阵动画
- **动画性能**：所有装饰元素使用CSS动画，GPU加速，不影响交互操作

#### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `HuahuoAssistant.vue` | 添加全屏拖拽功能（拖拽手柄、位置持久化、边界约束、触摸支持） |
| `CompetitionDetail.vue` | 完全重写，补充完整时间安排/奖项设置/材料要求，修复封面海报 |
| `TrainingCampDetail.vue` | 新增训练营独立详情页 |
| `CourseDetail.vue` | 新增在线课程独立详情页 |
| `TrainingCamps.vue` | "开始学习"按钮改为跳转详情页 |
| `Courses.vue` | "开始学习"按钮改为跳转详情页 |
| `MainLayout.vue` | 导航栏新增产业命题/AI助手/证书，侧边栏新增竞赛广场/AI助手/工具分组 |
| `PortalHome.vue` | 下板块添加背景装饰动画（浮动圆形/波浪/点阵） |
| `router/index.js` | 新增训练营详情和课程详情路由 |

---

### v2.3.0 - 2026-05-01

> 图片资源替换优化、导航与侧边栏入口补全、页面背景美化与动效增强、Live2D表情系统修复、引导窗口优化

#### 图片资源替换与优化

- **竞赛报名模块**：将所有竞赛卡片封面图替换为本地真实图片资源（`src/assets/images/competitions/`），文件名与比赛名称严格一对一匹配
- **训练营模块**：使用本地训练营图片资源（`src/assets/images/training-camps/`），按功能模块分类替换
- **在线课程模块**：使用本地课程图片资源（`src/assets/images/courses/`），确保图片内容与课程主题高度匹配
- **图片适配**：海报类图片保持16:9标准比例，通过CSS `object-fit: cover` 确保无拉伸变形
- **占位图机制**：实现图片加载失败时的渐变色占位图显示，占位图符合整体UI风格（Cyan主色调渐变）
- **全位置覆盖**：卡片封面图、详情页图片、hover/active状态图片均正确更新

#### 导航与侧边栏入口优化

- **导航栏补全**：补全竞赛报名、训练营、在线课程等核心功能模块的导航入口
- **入口排序**：基于用户使用习惯合理排序（首页 → 竞赛报名 → 训练营 → 在线课程 → 产业命题 → 证书成果）
- **侧边栏同步**：侧边栏与导航栏入口名称、图标样式、层级结构完全统一
- **活跃状态反馈**：入口处于活跃状态时提供明确视觉反馈（高亮、图标变色）
- **响应式设计**：导航栏与侧边栏实现桌面端、平板端、移动端全屏幕尺寸适配，移动端使用汉堡菜单

#### 页面背景美化与动效增强

- **首页粒子动画**：添加20个CSS粒子动画效果，与整体Cyan主色调UI风格适配
- **全站背景优化**：同步对竞赛报名页、训练营页面、课程详情页等所有页面进行背景优化
- **动效性能**：使用CSS动画实现粒子效果，确保运行帧率≥60fps
- **懒加载机制**：非首屏区域的动效通过 `IntersectionObserver` 实现懒加载

#### Live2D形象加载修复

- **表情按钮修复**：解决表情按钮点击无响应问题，重新实现表情控制逻辑
- **表情共存功能**：实现"月卡"和"水印"表情的叠加效果，可与任何其他基础表情同时生效
- **表情叠加系统**：设计修饰效果规则（`__expressionOverlayRules`），支持多修饰效果并行
- **CSP配置修复**：在 `vite.config.js` 中添加Content-Security-Policy header，允许Live2D SDK执行eval
- **加载性能优化**：Live2D形象加载时长≤3秒

#### 引导窗口优化

- **尺寸规范**：引导窗口宽度调整为≥800px（820px），高度根据内容自适应
- **布局重设计**：左侧步骤指示器 + 右侧内容区域的双栏布局
- **视觉优化**：优化元素间距、字号大小、视觉层级，提升内容可读性
- **步骤指示器**：已完成步骤显示✓标记，当前步骤高亮，未来步骤灰色

#### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `CompetitionSquare.vue` | 竞赛图片本地化导入、图片加载失败处理 |
| `TrainingCamps.vue` | 训练营图片本地化导入、占位图机制 |
| `Courses.vue` | 课程图片本地化导入、占位图机制 |
| `PortalHome.vue` | 粒子动画背景、统计数据展示优化 |
| `MainLayout.vue` | 导航入口补全、响应式设计、侧边栏同步 |
| `HuahuoAssistant.vue` | 表情系统修复、叠加效果实现、CSP兼容 |
| `GuideSystem.vue` | 窗口尺寸优化、双栏布局重设计 |
| `vite.config.js` | CSP header配置 |
| `src/assets/images/` | 新增竞赛/训练营/课程图片资源目录 |

#### 遇到的问题及解决方案

| 问题 | 解决方案 |
|------|----------|
| Live2D SDK被CSP策略阻止加载 | 在vite.config.js添加Content-Security-Policy header允许unsafe-eval |
| 图片加载失败导致页面空白 | 实现渐变色占位图机制，@error事件处理 |
| 表情按钮点击无响应 | 重新实现表情控制逻辑，使用全局状态管理 |
| 月卡/水印表情无法与其他表情共存 | 设计表情叠加系统，区分基础表情和修饰效果 |
| 引导窗口内容拥挤 | 重新设计双栏布局，增加窗口宽度至820px |
| 导航栏移动端显示异常 | 实现响应式设计，添加汉堡菜单 |

---

### v2.2.0 - 2026-05-01

> AI 助手与 Live2D 形象整合为全局浮动组件，CSP 修复，四角色引导更新

#### 架构变更

- **AI 助手不再是独立页面**：移除 `/ai-assistant` 路由和导航入口，改为全局浮动组件 `HuahuoAssistant.vue`
- **Live2D + 对话面板 + AI 分析三合一**：点击左下角 Live2D 看板娘「火花」即可打开对话面板，面板内可切换"对话模式"和"AI 分析模式"
- **任何页面均可使用 AI 助手**：不再需要跳转到专门页面，全局可用

#### 新增文件

- `HuahuoAssistant.vue`：整合 Live2D 看板娘 + AI 对话面板 + 语音交互 + AI 分析工具的全局浮动组件
  - Live2D 形象：点击打开对话面板，支持表情切换
  - 对话模式：文字/语音输入、SSE 流式回复、语音朗读、快捷问题
  - AI 分析模式：项目简介/商业建议/风险分析生成
  - 面板可拖拽移动，位置持久化到 localStorage

#### 前端变更

- `vite.config.js`：添加 CSP header `script-src 'self' 'unsafe-eval' 'unsafe-inline' blob: data:` 解决 Live2D 加载被阻止问题
- `MainLayout.vue`：`Live2dWidget` 替换为 `HuahuoAssistant`，移除顶部导航和侧边栏中的"AI 助手"入口
- `router/index.js`：移除 `/ai-assistant` 路由
- `api/ai.js`：新增 `generateAnalysis()` 统一 AI 分析入口函数
- `guide.js`（store）：四角色引导中 AI 助手相关步骤从"页面导航"改为"点击左下角火花"，合并对话/语音/Live2D 为一个步骤

#### BUG 修复

- **CSP 阻止 Live2D 加载**：Vite 开发服务器默认 CSP 策略阻止 `eval()` 执行，导致 Live2D SDK（Cubism5 core）无法初始化。在 `vite.config.js` 中添加 `Content-Security-Policy` header 允许 `unsafe-eval`
- **AI 对话和 Live2D 重复**：原来 AI 对话是独立页面 + Live2D 是独立浮动组件 + VoiceChat 又是另一个组件，三者功能重叠。现整合为 `HuahuoAssistant.vue` 一个组件

---

### v2.1.0 - 2026-05-01

> 修复竞赛详情数据缺失、训练营/课程按钮无响应、Live2D 加载优化、引导系统全面升级、**四角色页面全面补全**

#### 新增功能

- **竞赛详情页完整数据**：时间安排从 2 项扩展为 5 项（报名开始/截止 → 初赛评审 → 复赛决赛 → 结果公布），奖项从 1 项扩展为 5 级（特等奖/一等奖/二等奖/三等奖/最佳创意奖），每项含具体奖金和名额
- **训练营学习系统**：4 大主题训练营（创新基础/BP写作/路演表达/AI孵化）完整实现，含课程大纲（可展开章节/课时）、讲师团队介绍、播放按钮、"立即开始学习"入口
- **在线课程详情系统**：5 门课程（创业基础/市场调研/商业模式/路演技巧/法律知识）完整实现，含课程简介、章节目录（可展开）、免费/会员标签、评分/学习人数统计
- **使用引导系统 v2 全面升级**：
  - 学生引导从 9 步扩展至 14 步，覆盖全部新功能
  - 每步配置 `target` CSS 选择器，引导时自动高亮对应 UI 元素（脉冲动画边框）
  - 每步支持 `routePath` 路由跳转，跨页面引导时自动导航到目标页面再高亮
  - 新增功能引导：训练营、课程、AI 对话、语音面板、Live2D 形象等
  - 四角色（学生/教师/评委/管理员）引导内容均同步更新
- **一键启动脚本**：`start.bat` 放于项目根目录，双击即可同时启动前后端服务，自动检测并安装前端依赖

#### 四角色页面全面补全（本次重点）

**教师端**：
- `teacher.vue`（仪表盘）：从空状态 → 完整数据看板（指导项目数/待审核/学生数）+ 指导项目列表 + 待审核提醒 + 快捷操作入口
- `guide-projects.vue`（指导项目）：从"功能开发中" → 完整项目管理表格（搜索/筛选/状态统计）+ 审核弹窗（通过/需修改/驳回+意见）+ 反馈弹窗（改进建议+推荐训练营/课程资源）

**评委端**：
- `judge.vue`（仪表盘）：从空状态 → 完整数据看板（待评审/已评审/进度%）+ 待评审项目列表（含描述/类别/赛道标签）+ 评分分布可视化 + 快捷操作
- `pending.vue`（待评审列表）：修复"开始评审"按钮无点击事件问题，现已正确绑定 `@click="goToReview(project.id)"`

**管理员端**：
- `users.vue`（用户管理）：从"功能开发中" → 完整用户管理表格（搜索/角色筛选/状态筛选/分页）+ 添加/编辑用户弹窗（姓名/学号/邮箱/角色/状态切换）+ 启用/禁用/删除操作（带确认弹框）
- `competitions.vue`（比赛管理）：从"功能开发中" → 完整比赛批次管理（创建/编辑/启用停用）+ 统计卡片（全部/进行中/已完成/总报名数）+ 报名时间和比赛时间设置
- `projects.vue`（项目管理）：从"功能开发中" → 完整项目管理表格（搜索/阶段筛选/状态筛选/分页/6维统计卡片/平均分计算/评分颜色分级）+ 项目详情链接 + 评审记录查看

#### 前端变更

- `CompetitionDetail.vue`：时间安排和奖项设置补充完整的 fallback 数据（基于竞赛时间动态计算）
- `TrainingCamps.vue`：完全重写，新增弹窗式学习详情（`el-dialog`），含课程大纲折叠列表、讲师卡片、播放按钮
- `Courses.vue`：完全重写，新增弹窗式课程详情（`el-dialog`），含渐变头部、章节目录、学习统计
- `Live2dWidget.vue`：增强健壮性——分步加载 JS 库（index.js + index2.js + waifu-tips.js），增加加载状态提示（loading 动画 / 错误重试），超时保护（15s），canvas 渲染检测确认模型就绪
- `teacher.vue`：完全重写仪表盘，含统计数据、指导项目列表、待审核提醒、快捷操作
- `guide-projects.vue`：完全重写为完整的项目管理界面，含表格、搜索筛选、审核弹窗、反馈弹窗
- `judge.vue`：完全重写仪表盘，含统计数据、待评审项目列表、评分分布图、快捷操作
- `pending.vue`：修复"开始评审"按钮缺少 `@click` 事件绑定的问题
- `users.vue`：完全重写为完整的 CRUD 用户管理界面
- `competitions.vue`：完全重写为完整的比赛批次管理界面
- `projects.vue`：完全重写为完整的项目管理总览界面
- `guide.js`（store）：全面重写引导步骤，每步添加 `target` CSS 选择器和可选 `routePath` 路由路径
- `GuideSystem.vue`：新增路由导航能力（`useRouter`），步骤切换时检测 `routePath` 并自动跳转
- `start.bat`：新增项目根目录一键启动批处理脚本

#### BUG 修复

- **竞赛详情页信息缺失**：后端未返回 schedule/awards 时，前端 fallback 数据过于简略（仅 2 个时间点 / 1 个奖项），现已补充为完整的 5 阶段时间线和 5 级奖项体系
- **训练营"开始学习"按钮无响应**：按钮缺少 `@click` 事件绑定，现已实现打开学习详情弹窗的完整交互
- **课程"查看课程"按钮无响应**：同上，按钮无事件绑定，现已实现打开课程详情弹窗的完整交互
- **Live2D 形象不显示**：原初始化逻辑依赖单一 waifu-tips.js 的 onload 回调，若 CDN 加载缓慢或失败则静默失败。现改为：分步加载所有依赖库 + 轮询检测 initWidget 就绪 + canvas 渲染检测 + 加载状态 UI 反馈 + 错误重试机制（最多 3 次）
- **教师/评委/管理员大量页面空壳**：6 个页面原为"功能开发中"或空状态，现全部补全为具有完整交互功能的界面
- **评委"开始评审"按钮无响应**：`pending.vue` 第 27 行 `<el-button>` 缺少 `@click` 绑定，已修复

---

### v2.0.0 - 2026-04-30

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
