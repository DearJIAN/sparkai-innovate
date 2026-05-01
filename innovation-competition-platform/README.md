# 高校创新创业竞赛服务平台

> University Innovation and Entrepreneurship Competition Service Platform

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题等多元化功能。

平台集成了 **Live2D 虚拟形象「火花」**、**语音交互**、**AI 智能对话**等特色功能，为用户提供沉浸式智能辅助体验。

---

## 技术栈

### 前端

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | ^3.5.32 | 渐进式 JavaScript 框架（Composition API + `<script setup>`） |
| Vite | ^8.0.10 | 下一代前端构建工具 |
| @vitejs/plugin-vue | ^6.0.6 | Vite Vue 插件 |
| Element Plus | ^2.13.7 | 基于 Vue 3 的组件库 |
| @element-plus/icons-vue | ^2.3.2 | Element Plus 图标库 |
| Pinia | ^3.0.4 | Vue 状态管理方案 |
| Vue Router | ^5.0.6 | 前端路由管理（createWebHistory） |
| Axios | ^1.15.2 | HTTP 客户端（baseURL: `/api`，30s 超时） |
| ECharts | ^6.0.0 | 数据可视化图表库 |
| marked | ^18.0.2 | Markdown 渲染库（AI 输出格式化） |
| Live2D Widget | - | Live2D 看板娘组件（CDN + 本地 SDK） |

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| Flask | 3.0.3 | 轻量级 Web 框架（应用工厂模式） |
| Flask-SQLAlchemy | 3.1.1 | ORM 数据库工具 |
| Flask-Migrate | 4.0.7 | 数据库迁移工具（Alembic） |
| Flask-JWT-Extended | 4.6.0 | JWT 认证（Access 24h / Refresh 7d） |
| Flask-CORS | 4.0.1 | 跨域支持（仅允许 localhost:5173） |
| PyMySQL | 1.1.1 | MySQL 驱动 |
| cryptography | 42.0.8 | 加密库 |
| python-dotenv | 1.0.1 | 环境变量管理 |
| Werkzeug | 3.0.3 | WSGI 工具库（密码哈希 / 安全文件名） |
| volcengine-python-sdk[ark] | - | 火山方舟 AI SDK |
| opencc-python-reimplemented | - | 简繁转换（ASR 结果处理） |
| langchain / langchain-core | - | AI 编排框架 |
| websockets | - | WebSocket 客户端（实时语音对话 / ASR） |
| requests | - | HTTP 请求库（TTS 合成） |
| Pillow | - | 图像处理（seed.py 海报自动生成） |
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
- 流式输出重试机制（最大重试 2 次，递增间隔 1s/2s）+ 3 分钟超时控制

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
- 高亮指引 + 拖拽弹窗 + 路由自动跳转（`routePath` 配置）
- 引导状态持久化（Pinia `guide.js`）
- 四角色独立引导步骤（学生 14 步 / 教师 / 评委 / 管理员）

### 双模式布局

- 平台页面（首页 / 竞赛广场 / 训练营等）：无侧边栏，顶部导航
- 工作台页面（项目 / 评审 / 管理等）：左侧边栏 + 顶部导航
- 侧边栏可折叠，响应式适配

### 数字雨背景动画

- 全局 Canvas 数字雨效果（《黑客帝国》风格）
- 十六进制字符 + 编程符号，头部高亮 + 拖尾残影
- 水平扫描线增强科幻感
- 全屏铺满，动态高度检测
- IntersectionObserver 懒加载触发

---

## 项目结构

```
innovation-competition-platform/
├── start.bat                         # 一键启动脚本（自动检测依赖 + 启动前后端）
├── README.md                         # 项目文档
│
├── backend/                          # Flask 后端
│   ├── app.py                        # 应用入口（应用工厂模式 + 蓝图注册 + 错误处理）
│   ├── config.py                     # 配置文件（Development/Production/Testing 三环境）
│   ├── extensions.py                 # 扩展初始化（db/migrate/jwt/cors）
│   ├── seed.py                       # 测试数据初始化脚本（含 Pillow 海报生成）
│   ├── seed_competitions.py          # 竞赛数据种子脚本
│   ├── .env                          # 环境变量（本地开发，含 AI/ASR/TTS 配置）
│   ├── .env.example                  # 环境变量模板（基础配置）
│   ├── requirements.txt              # Python 依赖
│   ├── test_all_api.py               # API 测试脚本
│   ├── test_file_api.py              # 文件接口测试
│   ├── test_task_api.py              # 任务接口测试
│   │
│   ├── models/                       # 数据模型（12 个）
│   │   ├── __init__.py               # 模型统一导出
│   │   ├── user.py                   # 用户信息（users 表）
│   │   ├── competition.py            # 竞赛信息（competitions 表）
│   │   ├── competition_track.py      # 竞赛赛道（competition_tracks 表）
│   │   ├── competition_registration.py # 竞赛报名（competition_registrations 表）
│   │   ├── registration_member.py    # 报名队员（registration_members 表）
│   │   ├── registration_material.py  # 报名材料（registration_materials 表）
│   │   ├── project.py                # 项目信息（projects 表）
│   │   ├── project_member.py         # 项目成员（project_members 表）
│   │   ├── project_file.py           # 项目文件（project_files 表）
│   │   ├── project_task.py           # 项目任务（project_tasks 表）
│   │   ├── review.py                 # 评审记录（reviews 表）
│   │   └── ai_record.py             # AI 使用记录（ai_records 表）
│   │
│   ├── routes/                       # API 路由（13 个蓝图）
│   │   ├── __init__.py               # 蓝图包初始化
│   │   ├── auth.py                   # /api/auth    认证接口（注册/登录/当前用户/登出）
│   │   ├── user.py                   # /api/users   用户接口（列表/详情）
│   │   ├── project.py                # /api/projects 项目接口（CRUD/提交）
│   │   ├── member.py                 # /api         成员接口
│   │   ├── file.py                   # /api         文件接口
│   │   ├── material.py               # /api/materials 材料接口
│   │   ├── team.py                   # /api/teams   团队接口
│   │   ├── task.py                   # /api         任务接口
│   │   ├── review.py                 # /api         评审接口
│   │   ├── dashboard.py              # /api/dashboard 看板接口（统计/最近数据）
│   │   ├── ai.py                     # /api/ai      AI 接口（聊天/语音/ASR/TTS/分析/表情/健康）
│   │   ├── competition.py            # /api         竞赛接口（公开+管理+赛道）
│   │   └── registration.py           # /api         报名接口（学生+管理员）
│   │
│   ├── services/                     # 业务逻辑
│   │   ├── __init__.py
│   │   ├── ai_service.py             # AI 核心（火山方舟 SDK + 会话管理 + 流式输出 + 回答清洗）
│   │   ├── tts_service.py            # TTS 语音合成（火山 TTS HTTP API + 文件缓存 + 缓存统计/清理）
│   │   ├── volc_realtime_bridge.py   # 火山实时语音对话桥（WebSocket + 流式回复 + 回答清洗）
│   │   └── volc_realtime_protocol.py # 火山实时语音二进制协议（编解码 + Gzip）
│   │
│   ├── utils/                        # 工具函数
│   │   ├── __init__.py
│   │   ├── response.py               # 统一响应格式（success/error → {code, message, data}）
│   │   └── decorators.py             # 装饰器（require_roles / require_min_role / jwt_required_custom）
│   │
│   ├── uploads/                      # 文件上传目录
│   │   ├── competition_posters/      # 竞赛海报（seed.py 自动生成）
│   │   └── .gitkeep
│   └── migrations/                   # 数据库迁移（Alembic）
│       ├── versions/
│       │   └── 448f0412e5bb_initial_migration_with_all_models.py
│       ├── alembic.ini
│       ├── env.py
│       └── script.py.mako
│
├── frontend/                         # Vue 3 前端
│   ├── package.json                  # 依赖配置
│   ├── vite.config.js                # Vite 配置（代理 /api + /uploads → localhost:5000，CSP header）
│   ├── index.html                    # HTML 入口（标题：创新创业竞赛服务平台）
│   ├── README.md                     # 前端说明
│   │
│   ├── public/
│   │   ├── favicon.svg               # 网站图标
│   │   ├── icons.svg                 # 图标集
│   │   ├── live2d/                   # Live2D 模型资源
│   │   │   ├── huahuo/              # 「火花」模型
│   │   │   │   ├── 火花.model3.json  # 模型配置
│   │   │   │   ├── 火花.moc3         # 模型数据
│   │   │   │   ├── 火花.physics3.json # 物理引擎
│   │   │   │   ├── 火花.cdi3.json    # 参数定义
│   │   │   │   ├── model_list.json   # 模型列表
│   │   │   │   ├── icon.png          # 模型图标
│   │   │   │   ├── 按键设置说明.png    # 按键说明图
│   │   │   │   ├── Expressions/      # 12 个表情文件
│   │   │   │   ├── Motions/          # 2 个动作文件（循环/睡觉）
│   │   │   │   └── 火花.4096/        # 高清纹理（texture_00/01.png）
│   │   │   ├── huahuo-clean/         # 清理版模型（备用）
│   │   │   │   └── README.md
│   │   │   └── huahuo-packages.json  # 模型包配置
│   │   └── live2d-widget-dist/       # Live2D Widget SDK
│   │       ├── chunk/                # SDK 分块（index.js/index2.js + source maps）
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
│       │   ├── request.js            # Axios 基础配置（baseURL:/api，30s超时，Token拦截器，401自动跳转）
│       │   ├── auth.js               # 认证 API（login/register/getCurrentUser）
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
│       │   ├── GuideSystem.vue       # 全局引导系统（首次登录引导/高亮/拖拽弹窗/路由跳转）
│       │   ├── HuahuoAssistant.vue   # Live2D 虚拟形象「火花」（全屏拖拽/AI对话/语音/表情联动/3分钟超时/完整清理）
│       │   ├── VoiceChat.vue         # 语音交互面板（流式对话/语音识别/TTS/可拖拽/深色毛玻璃）
│       │   ├── Live2dWidget.vue      # Live2D 看板娘组件（旧版，已被 HuahuoAssistant 替代）
│       │   ├── TestButton.vue        # 测试按钮组件
│       │   ├── TestButtonDemo.vue    # 测试按钮演示
│       │   └── HelloWorld.vue        # 示例组件
│       │
│       ├── composables/              # 组合函数
│       │   └── useLive2d.js          # Live2D 表情/情绪联动工具（detectEmotionByText/getExpressionByEmotion/notifyLive2dHook）
│       │
│       ├── layouts/
│       │   └── MainLayout.vue        # 主布局（双模式：平台页无侧边栏/工作台有侧边栏 + Live2D 集成 + 导航/侧边栏/活跃状态）
│       │
│       ├── router/
│       │   └── index.js              # 路由配置（公共/学生/教师/评委/管理员/平台/通用路由 + beforeEach 守卫 + 角色权限检查）
│       │
│       ├── stores/                   # Pinia 状态管理
│       │   ├── user.js               # 用户状态（token/userInfo/角色权限计算属性/初始化/登录登出）
│       │   └── guide.js              # 引导系统状态（步骤配置/当前步骤/完成状态持久化）
│       │
│       ├── styles/
│       │   ├── design-system.css     # 设计系统变量（Cyan 主色调/暗色侧边栏/暗黑模式预留/间距/圆角/过渡/布局变量）
│       │   └── global.css            # 全局样式（Element Plus 覆盖/滚动条/过渡动画/布局类）
│       │
│       ├── assets/                   # 静态资源
│       │   ├── hero.png              # 首页主图
│       │   ├── vite.svg              # Vite 图标
│       │   ├── vue.svg               # Vue 图标
│       │   └── images/               # 图片资源
│       │       ├── competitions/     # 竞赛海报图（10 张，与比赛名称一对一匹配）
│       │       ├── certificates/     # 证书与获奖图片（5 张证书 + 2 张获奖）
│       │       ├── training-camps/   # 训练营图片（4 张）
│       │       └── courses/          # 在线课程图片（5 张）
│       │
│       └── views/                    # 页面视图（42 个 Vue 文件）
│           ├── ai-assistant/         # AI 助手（双标签页：分析工具 + 对话）
│           │   └── index.vue
│           ├── admin/                # 管理员页面（5 个）
│           │   ├── users.vue         # 用户管理（搜索/角色筛选/状态筛选/CRUD弹窗）
│           │   ├── projects.vue      # 项目管理（6维统计/搜索/阶段筛选/评分颜色分级）
│           │   ├── competitions.vue  # 竞赛管理（比赛批次/统计卡片/创建编辑启用停用）
│           │   ├── RegistrationManagement.vue # 报名管理（审核/驳回/统计）
│           │   └── reviews.vue       # 评审管理
│           ├── competitions/         # 竞赛管理
│           │   └── index.vue
│           ├── dashboard/            # 工作台（5 个角色看板）
│           │   ├── index.vue         # 看板主页（根据角色动态加载）
│           │   ├── student.vue       # 学生看板
│           │   ├── teacher.vue       # 教师看板（指导项目数/待审核/学生数）
│           │   ├── judge.vue         # 评委看板（待评审/已评审/评分分布图）
│           │   └── admin.vue         # 管理员看板
│           ├── error/
│           │   └── 404.vue           # 404 页面
│           ├── login/                # 登录注册
│           │   ├── index.vue         # 登录页（含快速登录提示）
│           │   └── register.vue      # 注册页
│           ├── materials/
│           │   └── index.vue         # 材料管理
│           ├── portal/               # 平台页面（12 个，无侧边栏）
│           │   ├── PortalHome.vue    # 平台首页（全局数字雨背景 + 功能入口 + 推荐竞赛 + 动态统计）
│           │   ├── CompetitionSquare.vue # 竞赛广场（深蓝渐变 Banner + 双光球呼吸动画 + 海报封面卡片）
│           │   ├── CompetitionDetail.vue # 竞赛详情（海报占满宽度 + 完整时间/奖项/材料 + 智能内容生成）
│           │   ├── CompetitionRegister.vue # 竞赛报名（快速填充 + 团队信息 + 队员管理）
│           │   ├── MyRegistrations.vue # 我的赛事（海报封面卡片 + 状态跟踪）
│           │   ├── TrainingCamps.vue # 训练营（紫罗兰渐变 Banner + 光球漂浮动画 + 海报封面）
│           │   ├── TrainingCampDetail.vue # 训练营详情（海报占满宽度 + 课程大纲 + 讲师团队）
│           │   ├── Courses.vue       # 在线课程（翠绿渐变 Banner + 光球浮动动画 + 海报封面）
│           │   ├── CourseDetail.vue   # 课程详情（海报占满宽度 + 章节目录 + 学习计划）
│           │   ├── IndustryTopics.vue # 产业命题（承接命题跳转填写页）
│           │   ├── AcceptTopic.vue   # 承接命题（填写承接信息 + 快速填充 + 跳转创建项目）
│           │   └── Certificates.vue  # 证书成果（查看详情弹窗 + 证书图片）
│           ├── projects/             # 项目页面（9 个）
│           │   ├── my-projects.vue   # 我的项目（onActivated 自动刷新）
│           │   ├── create.vue        # 创建项目（快速填充 + 数据预处理 + 详细错误处理）
│           │   ├── detail.vue        # 项目详情
│           │   ├── edit.vue          # 编辑项目
│           │   ├── members.vue       # 团队成员
│           │   ├── files.vue         # 项目材料
│           │   ├── tasks.vue         # 任务进度
│           │   ├── guide-projects.vue # 指导项目（审核弹窗 + 反馈弹窗）
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
└── image/                            # 项目截图
    └── README/
```

---

## 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 后端运行环境（推荐使用 `newyolo` conda 环境） |
| Node.js | 18+ | 前端构建环境 |
| MySQL | 8.0+ | 关系型数据库 |
| ffmpeg | - | 音频格式转换（ASR 功能需要，需加入系统 PATH） |
| conda | - | Python 环境管理（推荐 `newyolo` 环境） |

> **重要**：本项目指定使用 `newyolo` conda 环境，Python 解释器路径为 `D:\TOOLS\anaconda\envs\newyolo\python.exe`。`start.bat` 已配置使用此环境。

---

## 快速开始

### 方式一：一键启动（推荐）

双击项目根目录的 `start.bat`，脚本会自动：
1. 停止占用 5000/5173 端口的旧进程
2. 检测并安装前端依赖（首次运行时 `npm install`）
3. 使用 `newyolo` conda 环境启动后端服务（端口 5000）
4. 启动前端开发服务器（端口 5173）

启动完成后访问：
- 前端：http://localhost:5173
- 后端：http://localhost:5000

### 方式二：手动启动

#### 1. 克隆项目

```bash
git clone <repository-url>
cd innovation-competition-platform
```

#### 2. MySQL 数据库初始化

```sql
CREATE DATABASE IF NOT EXISTS innovation_competition
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
```

#### 3. 配置环境变量

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

> **注意**：`.env.example` 仅包含基础配置（Flask/MySQL/JWT），AI/ASR/TTS 相关配置需手动添加。

#### 4. 后端启动

```bash
cd backend

# 激活 conda 环境（推荐 newyolo）
conda activate newyolo

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

> **启动流程**：`app.py` → `create_app()` → 加载配置 → 初始化扩展 → 注册蓝图 → 注册错误处理 → `init_database()` 检查数据库连接并创建表 → `app.run(host='0.0.0.0', port=5000, debug=True)`

#### 5. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务默认运行在 http://localhost:5173

> **Vite 代理配置**：`/api` 和 `/uploads` 请求代理到 `http://localhost:5000`，CSP header 允许 `unsafe-eval`（Live2D SDK 需要）。

#### 6. 初始化测试数据

```bash
cd backend
python seed.py
```

seed.py 会自动创建：
- 8 个测试用户（4 种角色）
- 10 个竞赛（含赛道、Pillow 海报自动生成）
- 2 个项目
- 8 条报名记录（含队员信息，多种状态：draft/submitted/approved/rejected）

---

## 后端配置详情

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Flask 密钥（生产环境必须修改） |
| `SQLALCHEMY_DATABASE_URI` | `mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4` | 数据库连接字符串 |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | False | 关闭修改追踪 |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_size` | 10 | 数据库连接池大小 |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_recycle` | 3600 | 连接回收时间（秒） |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_pre_ping` | True | 连接前检测可用性 |
| `JWT_SECRET_KEY` | `dev-jwt-secret-key-change-in-production` | JWT 签名密钥（生产环境必须修改） |
| `JWT_ACCESS_TOKEN_EXPIRES` | 24 小时 | Access Token 有效期 |
| `JWT_REFRESH_TOKEN_EXPIRES` | 7 天 | Refresh Token 有效期 |
| `MAX_CONTENT_LENGTH` | 4 GB | 文件上传大小限制 |
| `DEFAULT_PAGE_SIZE` | 10 | 默认分页大小 |
| `MAX_PAGE_SIZE` | 100 | 最大分页大小 |
| `UPLOAD_FOLDER` | backend/uploads | 文件上传目录 |
| `ALLOWED_EXTENSIONS` | png/jpg/jpeg/gif/bmp/doc/docx/ppt/pptx/pdf/mp4/avi/mov/wmv/mkv/zip/rar/7z | 允许上传的文件类型 |

### CORS 配置

后端 CORS 仅允许以下来源访问 API：
- `http://localhost:5173`
- `http://127.0.0.1:5173`

允许的方法：GET / POST / PUT / DELETE / OPTIONS
允许的请求头：Content-Type / Authorization

### 环境配置类

| 配置类 | 说明 | 数据库 |
|--------|------|--------|
| `DevelopmentConfig` | 开发环境（DEBUG=True） | MySQL |
| `ProductionConfig` | 生产环境（DEBUG=False） | MySQL |
| `TestingConfig` | 测试环境（TESTING=True） | SQLite 内存数据库 |

---

## 演示账号

| 用户名 | 密码 | 角色 | 真实姓名 | 邮箱 |
|--------|------|------|----------|------|
| admin | admin123 | 管理员 | 管理员 | admin@example.com |
| student1 | student123 | 学生 | 张三 | student1@example.com |
| student2 | student123 | 学生 | 李四 | student2@example.com |
| student3 | student123 | 学生 | 王五 | student3@example.com |
| teacher1 | teacher123 | 指导老师 | 赵老师 | teacher1@example.com |
| teacher2 | teacher123 | 指导老师 | 钱老师 | teacher2@example.com |
| judge1 | judge123 | 评委 | 孙评委 | judge1@example.com |
| judge2 | judge123 | 评委 | 周评委 | judge2@example.com |

---

## API 接口文档

### 统一响应格式

所有 API 返回统一的 JSON 格式：

```json
// 成功响应
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}

// 错误响应
{
  "code": 400/401/403/404/409/500,
  "message": "错误描述",
  "data": null
}
```

### 认证接口 `/api/auth`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/auth/register` | POST | 无 | 用户注册（username/password 必填，email/role/real_name/phone/college/major 可选） |
| `/api/auth/login` | POST | 无 | 用户登录（返回 `{token, user}`，JWT Token 存 localStorage） |
| `/api/auth/me` | GET | JWT | 获取当前登录用户信息 |
| `/api/auth/logout` | POST | JWT | 登出（前端清除 Token） |

**注册请求示例**：
```json
{
  "username": "student1",
  "password": "123456",
  "email": "student@example.com",
  "role": "student",
  "real_name": "张三",
  "phone": "13800000000",
  "college": "计算机学院",
  "major": "软件工程"
}
```

**登录响应示例**：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": 1,
      "username": "admin",
      "role": "admin",
      "real_name": "管理员",
      ...
    }
  }
}
```

**注册校验规则**：
- 用户名至少 3 个字符，不可重复
- 密码至少 6 个字符
- 邮箱不可重复（可选）
- 角色只能是：student / teacher / judge / admin（默认 student）
- 账号被禁用时无法登录（返回 403）

### 用户接口 `/api/users`

| 接口 | 方法 | 认证 | 权限 | 说明 |
|------|------|------|------|------|
| `/api/users/` | GET | JWT | admin | 获取所有用户列表 |
| `/api/users/<id>` | GET | JWT | 本人或admin | 获取用户详情 |

### 竞赛接口

#### 公开接口（无需登录）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/public/competitions` | GET | 获取可报名竞赛列表（支持 keyword/category/level/status/page/per_page 参数） |
| `/api/public/competitions/:id` | GET | 获取竞赛详情（含赛道信息，自动增加浏览量） |
| `/api/public/competitions/:id/tracks` | GET | 获取竞赛赛道列表 |
| `/api/public/competition-categories` | GET | 获取竞赛分类列表（10 个分类） |

#### 管理员接口

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/competitions` | GET | JWT | 获取竞赛列表（支持 status 筛选） |
| `/api/competitions` | POST | admin | 创建竞赛 |
| `/api/competitions/:id` | PUT | admin | 更新竞赛 |
| `/api/competitions/:id` | DELETE | admin | 删除竞赛 |
| `/api/competitions/:id/tracks` | POST | admin | 创建赛道 |

### 报名接口

#### 学生接口

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/registrations` | POST | student | 创建报名草稿（competition_id/track_id 必填） |
| `/api/registrations/:id` | GET | student | 查看报名详情（仅自己的） |
| `/api/registrations/:id` | PUT | student | 更新报名信息（已提交不可修改） |
| `/api/registrations/:id/members` | POST | student | 添加队员 |
| `/api/registration-members/:id` | PUT | student | 编辑队员 |
| `/api/registration-members/:id` | DELETE | student | 删除队员 |
| `/api/registrations/:id/materials` | POST | student | 上传报名材料（multipart/form-data） |
| `/api/registration-materials/:id` | DELETE | student | 删除报名材料 |
| `/api/registrations/:id/submit` | POST | student | 提交报名（team_name 必填） |
| `/api/my-registrations` | GET | student | 查看我的报名列表（含竞赛名/赛道名/海报） |

#### 管理员接口

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/admin/registrations` | GET | admin | 获取所有报名记录（支持 competition_id/status/keyword/page/per_page） |
| `/api/admin/registrations/:id` | GET | admin | 查看报名详情 |
| `/api/admin/registrations/:id/approve` | POST | admin | 审核通过报名 |
| `/api/admin/registrations/:id/reject` | POST | admin | 驳回报名（可附 remark） |
| `/api/admin/registrations/statistics` | GET | admin | 报名统计数据 |

### 项目接口 `/api/projects`

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/projects` | GET | JWT | 获取项目列表（按角色过滤：学生看自己参与/负责的，教师看指导的，评委看已提交的，admin 看全部） |
| `/api/projects` | POST | student/admin | 创建项目（name 必填，stage 默认 idea，status 默认 draft） |
| `/api/projects/:id` | GET | JWT | 获取项目详情（含成员/文件数/任务数，需权限检查） |
| `/api/projects/:id` | PUT | JWT | 更新项目（仅负责人或 admin，评审阶段不可修改） |
| `/api/projects/:id` | DELETE | JWT | 删除项目（仅 draft 状态，仅负责人或 admin） |
| `/api/projects/:id/submit` | POST | JWT | 提交项目进入评审（draft/need_modify → submitted） |

**项目查询参数**：keyword / status / stage / track / page / per_page

### AI 分析工具 `/api/ai`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/ai/project-summary` | POST | JWT | 生成项目简介（AI 驱动，失败回退模板） |
| `/api/ai/business-plan-advice` | POST | JWT | 商业计划书建议（AI 驱动，失败回退模板） |
| `/api/ai/risk-analysis` | POST | JWT | 风险分析（AI 驱动，失败回退模板） |
| `/api/ai/records` | GET | JWT | AI 使用记录（按时间倒序） |

### AI 对话 `/api/ai`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/ai/chat` | POST | JWT | 文本聊天（非流式，返回 reply/sessionId/model/mode） |
| `/api/ai/chat/stream` | POST | JWT | 文本聊天（SSE 流式，text/event-stream） |
| `/api/ai/voice/chat/stream` | POST | JWT | 语音聊天（SSE 流式，优先火山实时语音，回退文本模型） |

**请求参数**：`message`（必填）/ `question` / `scene`（默认"创新创业平台"）/ `sessionId`

**SSE 流式响应协议**：

```
sessionId:<session-id>     # 首行返回会话 ID
delta:<text-chunk>         # 增量文本
error:<error-message>      # 错误信息（不中断流）
done:1                     # 流结束标记
```

### 语音交互 `/api/ai`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/ai/asr` | POST | JWT | 语音识别（multipart/form-data，豆包 ASR / faster-whisper 回退，返回 text/provider/model） |
| `/api/ai/tts/synthesize` | POST | JWT | TTS 语音合成（火山 TTS，返回 audio_url） |
| `/api/ai/tts/audio/<filename>` | GET | 无 | 获取合成音频文件（MP3） |
| `/api/ai/voice/config` | GET | JWT | 语音配置信息（realtime_configured/speaker/bot_name/input_mod） |

### Live2D / 健康 `/api/ai`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/ai/expressions` | GET | 无 | 获取表情列表（base 10 个 + overlay 2 个含概率） |
| `/api/ai/model-info` | GET | 无 | 获取 Live2D 模型信息（name: huahuo, path: /live2d/huahuo/火花.model3.json） |
| `/api/ai/health` | GET | 无 | AI 服务健康检查（chat_configured / voice_realtime_configured / model） |

### 看板接口 `/api/dashboard`

| 接口 | 方法 | 权限 | 说明 |
|------|------|------|------|
| `/api/dashboard/stats` | GET | admin | 管理员统计数据（用户/项目/文件/评审/竞赛/AI 使用，含角色分布/阶段分布/赛道分布） |
| `/api/dashboard/recent` | GET | admin | 最近数据（最近 5 个项目/文件/评审） |

### 系统接口

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/health` | GET | 无 | 系统健康检查（数据库连接状态，503 表示降级） |
| `/uploads/<path:filename>` | GET | 无 | 静态文件访问（上传文件，含海报/报名材料等） |

### 其他接口

| 接口前缀 | 说明 |
|----------|------|
| `/api/` | 成员（member.py）/ 文件（file.py）/ 任务（task.py）/ 评审（review.py） |
| `/api/teams` | 团队管理 |
| `/api/materials` | 材料管理 |

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
| `/accept-topic/:id` | portal/AcceptTopic.vue | 承接命题（填写承接信息） |

### 通用路由（所有角色）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/dashboard` | dashboard/index.vue | 工作台（按角色加载不同看板） |
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

### 路由守卫逻辑

1. **页面标题**：自动设置为 `{title} - 创新创业平台`
2. **公共页面**：已登录用户访问 /login 或 /register 时重定向到 /portal
3. **登录检查**：未登录用户重定向到 /login
4. **用户信息加载**：首次访问时调用 `userStore.init()` 加载用户信息
5. **角色权限检查**：路由 `meta.roles` 指定允许访问的角色，无权限时重定向到 /dashboard
6. **404 匹配**：未匹配路由显示 404 页面

---

## 数据库模型

### 表结构总览

| 模型 | 表名 | 说明 |
|------|------|------|
| User | users | 用户信息 |
| Competition | competitions | 竞赛信息 |
| CompetitionTrack | competition_tracks | 竞赛赛道 |
| CompetitionRegistration | competition_registrations | 竞赛报名 |
| RegistrationMember | registration_members | 报名队员 |
| RegistrationMaterial | registration_materials | 报名材料 |
| Project | projects | 项目信息 |
| ProjectMember | project_members | 项目成员 |
| ProjectFile | project_files | 项目文件 |
| ProjectTask | project_tasks | 项目任务 |
| Review | reviews | 评审记录 |
| AiRecord | ai_records | AI 使用记录 |

### 模型详细字段

#### User（用户信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 用户 ID |
| username | String(80) | 用户名（唯一，索引） |
| password_hash | String(255) | 密码哈希（Werkzeug generate_password_hash） |
| real_name | String(50) | 真实姓名 |
| email | String(120) | 邮箱（唯一） |
| phone | String(20) | 手机号 |
| role | String(20) | 角色（student/teacher/judge/admin，默认 student） |
| college | String(100) | 学院 |
| major | String(100) | 专业 |
| avatar | String(255) | 头像 URL |
| is_active | Boolean | 是否启用（默认 True） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

**关系**：projects（负责的项目）/ teacher_projects（指导的项目）/ reviews（评审记录）/ tasks（分配的任务）/ ai_records（AI 使用记录）

**方法**：`set_password(password)` / `check_password(password)` / `is_admin()` / `is_teacher()` / `is_judge()` / `is_student()`

#### Competition（竞赛信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 竞赛 ID |
| name | String(200) | 竞赛名称 |
| description | Text | 竞赛描述 |
| organizer | String(200) | 主办方 |
| category | String(50) | 分类（创新创业/人工智能/数字经济/乡村振兴/电子商务/软件开发/智能制造/职业规划/公益实践/产业命题） |
| level | String(20) | 级别（校级/省级/国家级/企业命题） |
| registration_start | DateTime | 报名开始时间 |
| registration_end | DateTime | 报名截止时间 |
| competition_start | DateTime | 比赛开始时间 |
| competition_end | DateTime | 比赛结束时间 |
| status | String(20) | 状态（draft/active/ended/archived/upcoming） |
| poster_url | String(500) | 海报 URL |
| tags | String(500) | 标签（逗号分隔，to_dict 时转为数组） |
| target_audience | String(500) | 目标受众 |
| requirements | Text | 参赛要求 |
| awards | Text | 奖项设置 |
| schedule | Text | 赛程安排 |
| view_count | Integer | 浏览量（默认 0） |
| registration_count | Integer | 报名数（默认 0） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

**关系**：projects / tracks（级联删除）/ registrations（级联删除）

#### CompetitionTrack（竞赛赛道）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 赛道 ID |
| competition_id | Integer (FK) | 所属竞赛 |
| name | String | 赛道名称 |
| description | Text | 赛道描述 |
| category | String | 赛道分类 |
| team_min | Integer | 最小团队人数（默认 1） |
| team_max | Integer | 最大团队人数（默认 5） |
| material_requirements | Text | 材料要求 |
| status | String | 赛道状态（默认 open） |

#### CompetitionRegistration（竞赛报名）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 报名 ID |
| competition_id | Integer (FK) | 竞赛 ID |
| track_id | Integer (FK) | 赛道 ID |
| project_id | Integer | 关联项目 ID |
| leader_id | Integer (FK) | 队长用户 ID |
| team_name | String | 队伍名称 |
| school | String | 学校 |
| college | String | 学院 |
| major | String | 专业 |
| teacher_name | String | 指导老师姓名 |
| teacher_phone | String | 指导老师电话 |
| contact_phone | String | 联系电话 |
| contact_email | String | 联系邮箱 |
| status | String | 状态（draft/submitted/approved/rejected/withdrawn） |
| remark | Text | 备注（驳回原因等） |
| submitted_at | DateTime | 提交时间 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

**关系**：members / materials

#### RegistrationMember（报名队员）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 队员 ID |
| registration_id | Integer (FK) | 报名记录 ID |
| name | String | 姓名 |
| student_no | String | 学号 |
| college | String | 学院 |
| major | String | 专业 |
| phone | String | 手机号 |
| email | String | 邮箱 |
| role_in_team | String | 队内角色（leader/member，默认 member） |

#### RegistrationMaterial（报名材料）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 材料 ID |
| registration_id | Integer (FK) | 报名记录 ID |
| uploader_id | Integer (FK) | 上传者 ID |
| material_type | String | 材料类型 |
| file_name | String | 文件名（UUID 重命名） |
| original_name | String | 原始文件名 |
| file_path | String | 文件存储路径 |
| file_type | String | 文件扩展名 |
| file_size | Integer | 文件大小（字节） |

#### Project（项目信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 项目 ID |
| name | String(100) | 项目名称 |
| description | Text | 项目描述 |
| category | String(50) | 项目类别 |
| track | String(50) | 所属赛道 |
| stage | String(30) | 当前阶段（idea/prototype/proof/development/production，默认 idea） |
| status | String(30) | 项目状态（draft/submitted/teacher_review/need_modify/judging/passed/rejected，默认 draft） |
| leader_id | Integer (FK → users) | 负责人 ID |
| teacher_id | Integer (FK → users) | 指导老师 ID |
| competition_id | Integer (FK → competitions) | 关联竞赛 ID |
| start_date | Date | 开始日期 |
| end_date | Date | 结束日期 |
| progress | Integer | 进度百分比（默认 0） |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

**关系**：members（级联删除）/ files（级联删除）/ tasks（级联删除）/ reviews（级联删除）/ ai_records

#### ProjectMember（项目成员）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 成员 ID |
| project_id | Integer (FK) | 项目 ID |
| user_id | Integer (FK) | 用户 ID |
| member_name | String | 成员姓名 |
| role_in_project | String | 项目角色 |
| responsibility | String | 职责 |

#### ProjectFile（项目文件）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 文件 ID |
| project_id | Integer (FK) | 项目 ID |
| filename | String | 文件名 |
| original_name | String | 原始文件名 |
| file_type | String | 文件类型 |
| material_type | String | 材料类型 |
| file_size | Integer | 文件大小 |
| storage_path | String | 存储路径 |
| uploader_id | Integer (FK) | 上传者 ID |

#### ProjectTask（项目任务）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 任务 ID |
| project_id | Integer (FK) | 项目 ID |
| title | String | 任务标题 |
| description | Text | 任务描述 |
| assignee_id | Integer (FK → users) | 负责人 ID |
| status | String | 任务状态 |
| priority | String | 优先级 |
| deadline | DateTime | 截止日期 |
| completed_at | DateTime | 完成时间 |

#### Review（评审记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 评审 ID |
| project_id | Integer (FK) | 项目 ID |
| judge_id | Integer (FK → users) | 评委 ID |
| innovation_score | Integer | 创新性评分 |
| feasibility_score | Integer | 可行性评分 |
| market_score | Integer | 市场评分 |
| team_score | Integer | 团队评分 |
| business_score | Integer | 商业评分 |
| technology_score | Integer | 技术评分 |
| presentation_score | Integer | 展示评分 |
| total_score | Float | 总分 |
| comment | Text | 评审意见 |

#### AiRecord（AI 使用记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 记录 ID |
| user_id | Integer (FK → users) | 用户 ID |
| project_id | Integer (FK → projects) | 项目 ID |
| type | String | 类型（summary/business_advice/risk_analysis） |
| prompt | Text | 输入提示 |
| result | Text | AI 输出结果 |
| created_at | DateTime | 创建时间 |

---

## 用户角色与权限

### 角色定义

| 角色 | 标识 | 层级 | 说明 |
|------|------|------|------|
| 学生 | `student` | 1 | 项目负责人 / 团队成员 |
| 指导老师 | `teacher` | 2 | 项目指导 |
| 评委 | `judge` | 3 | 项目评审 |
| 管理员 | `admin` | 4 | 系统管理 |

### 权限控制

后端使用 `require_roles` 装饰器进行角色权限控制：

```python
from utils.decorators import require_roles

@competition_bp.route('/competitions', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_competition():
    ...
```

还提供 `require_min_role` 装饰器用于层级权限控制（如：`require_min_role('teacher')` 允许 teacher/judge/admin 访问）。

### 侧边栏菜单

| 角色 | 侧边栏菜单 |
|------|------------|
| 学生 | 工作台、我的赛事、我的项目、创建项目、训练营、在线课程、产业命题、证书成果、AI 助手 |
| 指导老师 | 工作台、指导项目、项目审核、训练营、在线课程、产业命题、AI 助手 |
| 评委 | 工作台、待评审项目、评审记录、AI 助手 |
| 管理员 | 工作台、比赛批次管理、报名管理、项目管理、评审管理、用户管理、数据看板、AI 助手 |

---

## 设计系统

### CSS 变量体系

项目使用 `design-system.css` 定义统一的设计变量：

| 类别 | 变量前缀 | 说明 |
|------|----------|------|
| 主色调 | `--primary-50` ~ `--primary-900` | Cyan 专业色系（#06b6d4） |
| 中性色 | `--gray-50` ~ `--gray-900` | 灰色系（Tailwind 风格） |
| 语义色 | `--success/warning/danger/info` | 成功/警告/危险/信息色 |
| 背景 | `--bg-primary/secondary/tertiary/sidebar` | 页面/侧边栏背景色 |
| 文字 | `--text-primary/secondary/tertiary/inverse/sidebar` | 多层级文字色 |
| 阴影 | `--shadow-sm/md/lg/xl` | 4 级阴影 |
| 字体 | `--font-heading/body` | Poppins + Open Sans + 中文回退 |
| 间距 | `--space-1` ~ `--space-12` | 0.25rem ~ 3rem |
| 圆角 | `--radius-sm/md/lg/xl` | 0.375rem ~ 1rem |
| 过渡 | `--transition-fast/normal/slow` | 150ms/200ms/300ms |
| 布局 | `--sidebar-width/collapsed-width/header-height` | 240px/64px/64px |

### 暗黑模式预留

通过 `data-theme="dark"` 属性切换暗黑模式变量（尚未启用）。

---

## 开发规范

- 遵循 RESTful API 设计规范
- 前端使用 Composition API 风格（`<script setup>`）
- 代码注释使用中文
- 提交信息清晰描述改动内容
- 共享逻辑抽取为 composable（`src/composables/`）
- 统一响应格式：`{ code, data, message }`（`utils/response.py`）
- AI 回答清洗逻辑前后端一致（`sanitize_answer_text`）
- Live2D 表情 / 情绪联动通过 `window.__voiceLive2dHooks` 和 `window.__syncExpressionState` 全局桥接
- 密码使用 Werkzeug `generate_password_hash` / `check_password_hash` 加密
- 文件名使用 `werkzeug.utils.secure_filename` 安全处理 + UUID 重命名
- 权限控制使用 `require_roles` 装饰器，支持角色层级（`ROLE_HIERARCHY`）

---

## 常见问题

### 1. 数据库连接失败

1. 检查 MySQL 服务是否已启动
2. 确认数据库 `innovation_competition` 已创建（`utf8mb4` 字符集）
3. 检查 `.env` 文件中的 `DATABASE_URL` 配置
4. 确认用户名和密码正确
5. 检查 MySQL 连接池配置（pool_size: 10, pool_recycle: 3600）

### 2. AI 对话失败

1. 检查 `.env` 中的 `ARK_API_KEY` 是否正确
2. 确认火山方舟 API 可访问
3. 检查网络连接
4. 访问 `/api/ai/health` 查看配置状态（chat_configured / voice_realtime_configured / model）
5. AI 对话超时已设为 3 分钟（CHUNK_TIMEOUT = 180000ms），含重试机制（最多 2 次）

### 3. Live2D 模型加载失败

1. 确认 `frontend/public/live2d/huahuo/` 目录存在
2. 检查模型文件完整性（火花.model3.json / 火花.moc3 / 火花.physics3.json / 火花.cdi3.json）
3. 清除浏览器缓存重试
4. 检查浏览器控制台是否有 CORS 或 MIME 类型错误
5. 确认 Vite 代理配置正确（`/api` 和 `/uploads` 代理到后端）
6. 确认 CSP header 允许 `unsafe-eval`（Vite 配置中已设置）
7. 检查 `frontend/public/live2d-widget-dist/` 目录完整性

### 4. 语音识别不可用

1. Chrome / Edge 浏览器原生支持 Web Speech API
2. Firefox 需要后端 ASR 服务，检查 `.env` 中的 ASR 配置
3. 确保使用 HTTPS 或 localhost（麦克风权限要求）
4. 检查 ffmpeg 是否已安装并加入系统 PATH（音频格式转换需要）
5. ASR 回退机制：豆包 ASR → faster-whisper（需安装 faster-whisper 库）

### 5. 前端构建失败

1. 确认 Node.js 版本 >= 18
2. 删除 `node_modules` 后重新 `npm install`
3. 检查是否有语法错误（如括号表达式中的尾随逗号）
4. 确认 `useLive2d.js` 中使用数组而非括号表达式（`META_LINE_PREFIXES` / `META_LINE_KEYWORDS` / `ANSWER_MARKERS`）

### 6. TTS 语音合成失败

1. 检查 `.env` 中的 `VOICE_REALTIME_TOKEN` 和 `VOICE_REALTIME_APP_ID` 是否正确
2. 确认火山 TTS API 可访问
3. 检查 `backend/services/tts_cache/` 目录是否有写入权限
4. TTS 缓存：MD5 键 + 7 天 TTL，可通过 `get_tts_cache_stats` / `clear_tts_cache` 管理

### 7. 项目创建 500 错误

1. 检查 `teacher_id` 和 `competition_id` 是否为有效整数（空字符串需传 `null`）
2. 日期格式需为 `YYYY-MM-DD` 字符串
3. 使用「快速填充」按钮生成合规数据测试
4. 查看浏览器控制台 `[CreateProject]` 日志确认请求数据格式

### 8. 数字雨动画不显示

1. 确认 `globalRainCanvas` ref 已定义
2. 检查 `.global-rain-canvas` 的 `z-index: 0` 低于内容区域的 `z-index: 1`
3. 确认 Canvas 的 `pointer-events: none` 不影响交互
4. 检查浏览器是否支持 Canvas API
5. 确认 IntersectionObserver 懒加载触发正常

### 9. Live2D 拖拽按钮不跟随形象

1. 确认 `applyModelPosition` 函数中同步更新了 `live2d-drag-handle` 位置
2. 检查 `localStorage` 中 `huahuoModelPos` 是否有残留的 `bottom` 定位数据（需清除）
3. 确认 `#waifu` 使用 `top` 定位而非 `bottom`

### 10. CORS 跨域问题

1. 确认前端运行在 `http://localhost:5173` 或 `http://127.0.0.1:5173`
2. 后端 CORS 仅允许这两个来源
3. 生产环境需修改 `app.py` 中的 CORS 配置

### 11. JWT Token 过期

1. Access Token 有效期 24 小时，过期后需重新登录
2. 前端 Axios 拦截器自动检测 401 响应，清除 Token 并跳转登录页
3. 登录接口返回的 Token 存储在 `localStorage`

---

## 当前开发状态

### 已完成功能模块

| 模块 | 状态 | 说明 |
|------|------|------|
| 用户认证 | ✅ 完成 | 注册/登录/JWT Token/角色权限/账号禁用 |
| 竞赛广场 | ✅ 完成 | 公开竞赛列表/详情/海报/时间安排/奖项设置/分类筛选/浏览量统计 |
| 竞赛管理 | ✅ 完成 | 管理员 CRUD/赛道管理/状态控制 |
| 竞赛报名 | ✅ 完成 | 学生报名/队员管理/材料上传/提交/管理员审核/驳回/统计 |
| 训练营 | ✅ 完成 | 列表/详情/海报/章节大纲/讲师信息 |
| 在线课程 | ✅ 完成 | 列表/详情/海报/章节视频/进度跟踪 |
| 产业命题 | ✅ 完成 | 命题列表/承接填写页/跳转创建项目 |
| 项目管理 | ✅ 完成 | 创建/编辑/详情/成员/文件/任务/提交评审/删除 |
| AI 智能对话 | ✅ 完成 | 流式输出/重试机制/3分钟超时/会话管理/回答清洗 |
| AI 分析工具 | ✅ 完成 | 项目简介/商业计划书/风险分析 |
| 语音交互 | ✅ 完成 | ASR/TTS/实时语音对话/可拖拽面板 |
| Live2D 虚拟形象 | ✅ 完成 | 全屏拖拽/表情联动/口型驱动/位置持久化/拖拽按钮跟随 |
| 证书成果 | ✅ 完成 | 证书列表/获奖记录/查看详情弹窗/证书图片 |
| 我的赛事 | ✅ 完成 | 报名列表/海报封面/状态跟踪 |
| 全局引导系统 | ✅ 完成 | 首次登录引导/步骤导航/路由跳转/状态持久化 |
| 数据看板 | ✅ 完成 | 4 角色看板/统计图表/动态数据/最近数据 |
| 管理后台 | ✅ 完成 | 用户/项目/竞赛/报名/评审管理 |
| 首页数字雨 | ✅ 完成 | 全局 Canvas 数字雨背景/科幻风格/扫描线/全屏铺满 |
| Banner 动画 | ✅ 完成 | 竞赛/训练营/课程各具独特渐变色+光球动画 |
| 一键启动 | ✅ 完成 | start.bat 自动检测依赖+启动前后端 |

### 正在进行的开发任务

| 任务 | 优先级 | 说明 |
|------|--------|------|
| 进度条横向滚动 | 高 | 多步骤流程场景的横向拖拽/滑动查看 |
| 产业命题后端 API | 中 | 承接命题数据持久化、命题 CRUD 接口 |
| 训练营/课程学习进度 | 中 | 视频观看进度、章节完成状态 |
| 评审打分优化 | 中 | 多维度评分、评分模板、评审意见模板 |
| 移动端适配 | 低 | 响应式布局优化、触屏交互 |

### 未来规划

- **消息通知系统**：站内信、竞赛状态变更通知、报名审核通知
- **数据导出**：报名表 Excel 导出、评审结果导出、证书 PDF 下载
- **团队协作**：项目讨论区、文件版本管理、任务看板
- **AI 能力扩展**：项目匹配推荐、竞赛策略分析、路演稿生成
- **性能优化**：前端懒加载、后端缓存、CDN 静态资源
- **暗黑模式**：设计系统已预留暗黑模式变量，待实现切换逻辑

---

## 调试指南

### 前端调试

#### 开发工具

| 工具 | 用途 | 访问方式 |
|------|------|----------|
| Vue DevTools | 组件树/状态/路由/事件/Pinia Store | 浏览器扩展 |
| Chrome DevTools | 网络/性能/内存/Console | F12 |
| Vite DevServer | HMR/代理/构建 | `npm run dev` |

#### 常用调试命令

```bash
# 前端开发服务器（HMR 热更新）
cd frontend && npm run dev

# 前端生产构建
cd frontend && npm run build

# 检查前端依赖安全
cd frontend && npm audit
```

#### 关键调试日志

| 日志前缀 | 位置 | 说明 |
|----------|------|------|
| `[AI Stream]` | HuahuoAssistant.vue | AI 流式对话重试/超时/错误 |
| `[CreateProject]` | create.vue | 项目创建请求数据/错误详情 |
| `[Live2D]` | HuahuoAssistant.vue | 模型加载/表情切换/拖拽位置 |

#### 前端断点调试技巧

1. **Vue 组件状态**：在 Vue DevTools 中查看组件 props/data/computed
2. **API 请求**：Chrome DevTools → Network → 筛选 `XHR/Fetch`
3. **路由跳转**：在 `router/index.js` 的 `beforeEach` 守卫中添加 `console.log`
4. **Pinia Store**：Vue DevTools → Pinia 面板查看状态快照
5. **Live2D 问题**：检查 `window.__voiceLive2dHooks` 和 `window.__syncExpressionState` 全局对象
6. **Token 问题**：检查 `localStorage.getItem('token')` 是否存在
7. **CSP 问题**：检查浏览器控制台 Content-Security-Policy 违规报告

### 后端调试

#### 常用调试命令

```bash
# 后端开发服务器（debug 模式自动重载）
cd backend && python app.py

# 使用 conda 环境
conda activate newyolo
cd backend && python app.py

# 初始化/重置数据库
cd backend && flask db upgrade

# 运行 API 测试
cd backend && python test_all_api.py

# 检查 AI 服务健康状态
curl http://localhost:5000/api/ai/health

# 检查系统健康状态
curl http://localhost:5000/api/health
```

#### 后端日志说明

| 日志内容 | 说明 |
|----------|------|
| `SQLAlchemy` 查询日志 | 设置 `SQLALCHEMY_ECHO=True` 开启 |
| AI 会话管理日志 | 会话创建/清理/过期检查 |
| TTS 缓存统计 | 缓存命中率/文件数量/总大小 |
| 流式对话日志 | SSE 连接/断开/错误 |
| 数据库连接日志 | `init_database()` 输出连接状态 |

#### 数据库调试

```bash
# 进入 MySQL 命令行
mysql -u root -p innovation_competition

# 查看所有表
SHOW TABLES;

# 查看用户列表
SELECT id, username, role, real_name, is_active FROM users;

# 查看竞赛列表
SELECT id, name, level, status, view_count, registration_count FROM competitions;

# 查看报名统计
SELECT status, COUNT(*) as count FROM competition_registrations GROUP BY status;

# 重置数据库（危险操作）
DROP DATABASE innovation_competition;
CREATE DATABASE innovation_competition DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
cd backend && flask db upgrade && python seed.py
```

### 快速填充功能

多个页面提供「快速填充」按钮用于调试，点击后自动填入合规的测试数据：

| 页面 | 填充内容 |
|------|----------|
| 创建项目 | 项目名称/类别/赛道/简介/指导老师/日期（5 个预设名称随机选择） |
| 竞赛报名 | 团队名称/学校/学院/专业/队员信息（3 名测试队员） |
| 承接命题 | 负责人/电话/团队人数/方案/优势 |

### 环境变量检查清单

| 变量 | 必需 | 说明 |
|------|------|------|
| `DATABASE_URL` | ✅ | MySQL 连接字符串 |
| `SECRET_KEY` | ✅ | Flask 密钥 |
| `JWT_SECRET_KEY` | ✅ | JWT 签名密钥 |
| `ARK_API_KEY` | ❌ | AI 对话（不配置则 AI 功能不可用） |
| `ARK_BASE_URL` | ❌ | 火山方舟 API 地址 |
| `ARK_MODEL` | ❌ | AI 模型名称 |
| `VOICE_REALTIME_*` | ❌ | 实时语音对话（不配置则回退文本模式） |
| `DOUBAO_ASR_*` | ❌ | 语音识别（不配置则仅 Chrome 原生 ASR） |

---

## 版本变更记录

### v3.0.0 - 2026-05-01（当前版本）

> AI流式输出优化、项目创建修复、引导内容更新、产业命题承接、动态数据、头部卡片动画

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

#### AI 对话流式输出稳定性优化

- **问题根因**：原流式输出代码在遇到网络抖动、API 返回空数组或响应中断时直接报错，无重试机制
- **修复方案**：
  - **重试机制**：最大重试 2 次，每次重试间隔递增（1s、2s）
  - **超时控制**：单 chunk 接收超时 3 分钟（180000ms），超时自动触发重试
  - **缓冲区处理**：完善 decoder 缓冲区管理，确保最后一行数据不丢失
  - **错误隔离**：服务端返回的 `error:` 行不再中断流，继续读取后续内容
  - **完整保存**：使用 `fullResponse` 变量累计完整回复，避免 `streamingText` 重置导致内容丢失
  - **空响应保护**：检查 `response.body` 是否存在，不存在时抛出明确错误

#### 项目创建失败问题修复（500 错误）

- **问题根因**：快速填充生成的 `teacher_id` 和 `competition_id` 为字符串，后端期望整数或 null；空字符串传给后端导致 500 错误
- **修复方案**：
  - **数据预处理**：提交前将 `teacher_id` / `competition_id` 从字符串转为整数，空字符串转为 `null`
  - **格式校验**：日期对象转为 `YYYY-MM-DD` 字符串格式
  - **详细错误提示**：区分 500/400/401/403/网络错误，给出针对性提示
  - **调试日志**：提交前 `console.log` 完整请求数据，便于排查

#### 引导窗口内容适配更新

- **问题根因**：引导步骤仍引用 v2.0 旧功能（工作台数据看板、成员管理、材料上传等），与当前平台功能不匹配
- **修复方案**：
  - 更新为 v3.0 功能路径：首页 → 竞赛广场 → 我的赛事 → 训练营 → 课程 → 产业命题 → 项目管理 → 证书成果 → AI 助手
  - 删除已移除的功能（工作台数据看板、成员管理、材料上传等）
  - 补充新增功能：我的赛事、产业命题、证书成果
  - 每步引导文案与当前页面功能一致

#### 产业命题承接流程完善

- **新增页面**：`AcceptTopic.vue` 承接命题填写页面
  - 表单字段：负责人姓名、联系电话（手机号校验）、团队人数、预计完成时间、项目方案概述、团队优势、备注
  - 顶部展示命题信息（企业、标题、周期、奖金）
  - 一键快速填充按钮（调试辅助）
  - 确认承接后跳转创建项目页面，URL 传递命题信息
- **路由配置**：新增 `/accept-topic/:id` 路由
- **IndustryTopics.vue**：点击「承接命题」跳转至填写页面（而非直接确认弹窗）

#### 项目列表动态更新

- **问题根因**：从创建项目页面返回「我的项目」时，列表不自动刷新
- **修复方案**：`my-projects.vue` 添加 `onActivated` 钩子，页面从 keep-alive 恢复时自动调用 `fetchProjects()`

#### 系统数值动态化

- **问题根因**：首页 Banner 统计（50+ 竞赛、1000+ 团队、10+ 赛道）为硬编码
- **修复方案**：
  - 调用 `getDashboardStats()` API 获取实时数据
  - 添加 `homeStats` 响应式数据对象
  - API 失败时回退到默认值
  - 模板使用 `{{ homeStats.competitions }}+` 动态绑定

#### 页面头部卡片渐变色 + 动画优化

- **竞赛广场**：深蓝渐变 `#1e3a5f → #0c4a6e → #0ea5e9` + 双光球呼吸动画 `bannerPulse`
- **训练营**：紫罗兰渐变 `#312e81 → #4338ca → #7c3aed` + 光球漂浮动画 `campGlow`（带位移）
- **在线课程**：翠绿渐变 `#064e3b → #059669 → #10b981` + 光球上下浮动动画 `courseFloat`
- **动画实现**：纯 CSS `@keyframes` + `::before/::after` 伪元素，无需额外库

#### 修改文件清单

| 文件 | 修改内容 |
|------|----------|
| `CompetitionDetail.vue` | 移除 padding-top:64px；海报 aspect-ratio:16/9 占满宽度；去掉 poster-fallback 中央文字 |
| `TrainingCampDetail.vue` | 移除 padding-top:64px；海报 object-fit:contain + aspect-ratio:16/9 |
| `CourseDetail.vue` | 移除 padding-top:64px；海报 object-fit:contain + aspect-ratio:16/9 |
| `HuahuoAssistant.vue` | 拖拽按钮 v-if 改为常驻；panel-open 类控制透明度隐藏；流式输出重试+超时机制（3分钟） |
| `MainLayout.vue` | isMenuActive 修复：/create-project 独立匹配，/my-projects 不再匹配 /create-project |
| `create.vue` | 添加 quickFillProject 函数；快速填充栏 UI；handleSubmit 数据预处理+详细错误处理 |
| `IndustryTopics.vue` | 底部对齐样式修复；handleAccept 跳转至填写页面 |
| `AcceptTopic.vue` | 新增：产业命题承接填写页面，含表单、校验、快速填充 |
| `PortalHome.vue` | 推荐竞赛卡片改用海报封面；全局数字雨；动态加载首页统计数据 |
| `my-projects.vue` | 添加 onActivated 钩子实现返回时自动刷新 |
| `guide.js` | 引导步骤更新为 v3.0 功能路径 |
| `CompetitionSquare.vue` | Banner 渐变色+双光球呼吸动画 |
| `TrainingCamps.vue` | Banner 紫罗兰渐变色+光球漂浮动画 |
| `Courses.vue` | Banner 翠绿渐变色+光球浮动动画 |
| `router/index.js` | 新增 /accept-topic/:id 路由 |

---

### v2.10.0 - 2026-05-01

> Live2D拖拽按钮常驻、侧边栏选中状态修复、创建项目快速填充、产业命题承接功能

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
