# 高校创新创业竞赛服务平台

> University Innovation and Entrepreneurship Competition Service Platform

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题等多元化功能。

平台集成了 **Live2D 虚拟形象「火花」**、**语音交互**、**AI 智能对话**、**AI 项目智能体**等特色功能，为用户提供沉浸式智能辅助体验。其中 AI 项目智能体提供智能引航、材料问答、商业计划书体检、路演稿生成、评审辅助、竞赛推荐、项目创意生成、模拟答辩、批量审核、智能反馈、评审草稿、评分检查 12 大 AI 能力，基于 LangChain + FAISS + BM25 混合检索技术实现。

***

## 项目环境依赖

> 本项目后端指定使用 `newyolo` conda 环境，Python 解释器路径：`D:\TOOLS\anaconda\envs\newyolo\python.exe`

### 后端核心依赖（newyolo conda 环境）

| 库名                          | 版本     | 用途                                  |
| --------------------------- | ------ | ----------------------------------- |
| Python                      | 3.10+  | 运行环境                                |
| Flask                       | 3.0.3  | Web 框架                              |
| Flask-SQLAlchemy            | 3.1.1  | ORM 数据库工具                           |
| Flask-Migrate               | 4.0.7  | 数据库迁移（Alembic）                      |
| Flask-JWT-Extended          | 4.6.0  | JWT 认证                              |
| Flask-Cors                  | 4.0.1  | 跨域支持                                |
| PyMySQL                     | 1.1.1  | MySQL 驱动                            |
| SQLAlchemy                  | 2.0.49 | ORM 核心                              |
| Alembic                     | 1.18.4 | 数据库迁移引擎                             |
| Werkzeug                    | 3.0.3  | WSGI 工具库                            |
| python-dotenv               | 1.0.1  | 环境变量管理                              |
| cryptography                | 47.0.0 | 加密库                                 |
| PyJWT                       | 2.12.1 | JWT Token 处理                        |
| volcengine-python-sdk       | 5.0.24 | 火山方舟 AI SDK（备选模型通道）                 |
| openai                      | 2.32.0 | OpenAI 兼容接口（通义千问 qwen-plus 通过此接口接入） |
| langchain                   | 1.2.15 | AI 编排框架                             |
| langchain-core              | 1.3.0  | LangChain 核心                        |
| langchain-openai            | 1.1.15 | LangChain OpenAI 兼容接口               |
| langchain-community         | 0.4.1  | LangChain 社区扩展                      |
| langchain-text-splitters    | 1.1.2  | 文本分割器                               |
| langchain-volcengine        | 0.1.2  | 火山方舟 LangChain 集成                   |
| faiss-cpu                   | 1.13.2 | Facebook 向量相似性搜索                    |
| rank-bm25                   | 0.2.2  | BM25 稀疏检索                           |
| jieba                       | 0.42.1 | 中文分词（BM25 中文支持）                     |
| python-docx                 | 1.2.0  | Word 文档解析                           |
| python-pptx                 | 1.0.2  | PowerPoint 文档解析                     |
| pypdf                       | 6.10.2 | PDF 文档解析                            |
| websockets                  | 16.0   | WebSocket 客户端                       |
| requests                    | 2.32.5 | HTTP 请求库                            |
| Pillow                      | 11.2.1 | 图像处理（海报生成）                          |
| opencc-python-reimplemented | 0.1.7  | 简繁转换                                |
| tiktoken                    | 0.12.0 | Token 计数                            |
| numpy                       | 2.2.6  | 数值计算                                |

### 前端核心依赖

| 库名           | 版本      | 用途                |
| ------------ | ------- | ----------------- |
| Node.js      | 18+     | 运行环境              |
| Vue          | ^3.5.32 | 渐进式 JavaScript 框架 |
| Vite         | ^8.0.10 | 前端构建工具            |
| Element Plus | ^2.13.7 | Vue 3 组件库         |
| Pinia        | ^3.0.4  | 状态管理              |
| Vue Router   | ^5.0.6  | 前端路由              |
| Axios        | ^1.15.2 | HTTP 客户端          |
| ECharts      | ^6.0.0  | 数据可视化             |
| marked       | ^18.0.2 | Markdown 渲染       |
| DOMPurify    | ^3.2.6  | HTML 安全净化         |

### 基础设施

| 依赖     | 版本   | 说明                        |
| ------ | ---- | ------------------------- |
| MySQL  | 8.0+ | 关系型数据库                    |
| ffmpeg | -    | 音频格式转换（ASR 需要，需加入系统 PATH） |
| conda  | -    | Python 环境管理（`newyolo` 环境） |

***

## 技术栈

> 完整依赖版本信息见顶部 [项目环境依赖](#项目环境依赖) 章节

### 前端

| 技术                 | 说明                                                    |
| ------------------ | ----------------------------------------------------- |
| Vue 3              | 渐进式 JavaScript 框架（Composition API + `<script setup>`） |
| Vite               | 下一代前端构建工具                                             |
| Element Plus       | 基于 Vue 3 的组件库                                         |
| Pinia              | Vue 状态管理方案                                            |
| Vue Router         | 前端路由管理（createWebHistory）                              |
| Axios              | HTTP 客户端（baseURL: `/api`，30s 超时）                      |
| ECharts            | 数据可视化图表库                                              |
| marked + DOMPurify | Markdown 渲染 + XSS 防护                                  |
| Live2D Widget      | Live2D 看板娘组件（CDN + 本地 SDK）                            |

### 后端

| 技术                                | 说明                                                          |
| --------------------------------- | ----------------------------------------------------------- |
| Flask                             | 轻量级 Web 框架（应用工厂模式）                                          |
| Flask-SQLAlchemy                  | ORM 数据库工具                                                   |
| Flask-JWT-Extended                | JWT 认证（Access 24h / Refresh 7d）                             |
| LangChain                         | AI 编排框架（RAG 问答 / BP 体检 / 路演稿 / 评审辅助 / 竞赛推荐 / 统一对话路由 / 智能导航） |
| FAISS + BM25                      | 混合检索方案（向量索引 + 稀疏检索 + 关键词回退）                                 |
| 通义千问 qwen-plus                    | AI 大模型（通过 LangChain ChatOpenAI 兼容接口接入，支持多轮对话 / 意图识别 / 角色感知） |
| 火山方舟 SDK                          | AI 大模型 + Embedding + ASR + TTS（备选模型通道）                      |
| python-docx / python-pptx / pypdf | 文档解析（.docx / .pptx / .pdf）                                  |
| PyMySQL                           | MySQL 驱动                                                    |

***

## 特色功能

### Live2D 虚拟形象「火花」

- 全局浮动 Live2D 看板娘，支持全屏拖拽（通过 `HuahuoAssistant.vue` 组件 + `MainLayout.vue` 集成）
- 拖拽位置持久化到 localStorage，刷新页面后自动恢复
- 10 种基础表情（黑脸 / 脸红爱心 / 生气 / 晕 / ＞＜ / 0.0 / 星星眼 / 流泪 / 捧心 / 要饭）+ 2 种叠加效果（月卡 / 水印）
- AI 对话时自动切换表情（基于关键词的情绪检测：开心 / 害羞 / 生气 / 难过 / 晕 / 惊讶）
- 每 10 秒自动随机切换表情（AI 流式输出或朗读期间跳过），点击形象时也会随机切换
- 语音朗读时口型驱动动画（正弦波模拟 + 文本长度驱动）
- 可拖拽、可隐藏、可切换表情
- 表情 / 情绪联动逻辑抽取为共享 composable（`useLive2d.js`）
- 组件卸载时完整清理（CSS link / DOM 元素 / 全局变量），避免内存泄漏

### AI 智能对话

- 基于通义千问 qwen-plus 大模型（通过 LangChain + ChatOpenAI 兼容接口接入），同时保留火山方舟大模型（doubao-seed-1-6-251015）作为备选
- **统一对话路由**（`unified_chat`）：根据用户消息自动识别意图（导航 / 通用对话 / 智能体能力），分发到对应处理逻辑
- **智能导航**：用户输入模糊指令（如"我想报名比赛""帮我看看项目"），AI 自动识别意图并返回路由跳转建议，前端自动执行页面跳转
- 支持 SSE 流式输出，打字机效果（`/api/ai/chat/stream`）
- 会话管理（6 轮上下文记忆，6 小时 TTL，自动清理过期会话）
- 智能回答清洗（过滤思考过程、去重、提取最终答案标记后的内容、半文重复检测、去除 Markdown 特殊符号）
- 快捷问题按钮（分析项目创新性 / 商业计划书 / 竞赛评审 / 团队组建）
- AI 助手页面双标签页设计：**AI 分析工具** + **AI 对话**
- 流式输出重试机制（最大重试 2 次，递增间隔 1s/2s）+ 3 分钟超时控制
- 角色感知对话：根据当前登录角色（学生/教师/评委/管理员）自动调整 AI 回复风格和可用能力

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

### AI 项目智能体

基于 LangChain + FAISS + BM25 混合检索的 AI 项目智能体系统，为竞赛全流程提供 12 大 AI 能力：

- **智能引航**：用户输入模糊指令（如"我想报名比赛""帮我看看项目"），AI 自动识别意图并返回路由跳转建议，前端自动执行页面跳转
- **AI 材料问答**：上传项目/报名材料（支持 .docx / .pptx / .pdf），自动解析文档内容并建立向量索引，用户可针对材料内容进行自然语言问答，AI 基于检索结果精准回答
- **AI 商业计划书体检**：对商业计划书进行全方位结构化审查，从执行摘要、市场分析、商业模式、团队介绍、财务规划、风险分析等维度给出改进建议，**不给出具体评分**
- **AI 路演稿生成**：根据项目信息和材料内容，自动生成结构化路演演讲稿（开场白 / 痛点分析 / 解决方案 / 市场前景 / 团队介绍 / 结尾呼吁），支持 3/5/8 分钟时长和正式/激情/精炼/故事 4 种风格
- **AI 评审辅助**（仅 teacher / judge / admin）：辅助评审人员快速了解项目全貌，生成项目亮点/风险/改进建议的摘要分析，**严格不返回具体分数，仅提供定性评价参考**
- **智能竞赛推荐**（仅 student / admin）：根据项目类别、赛道、阶段等信息，智能匹配推荐适合参加的竞赛，给出推荐理由和匹配度分析
- **项目创意生成**（仅 student / admin）：基于学生技能特长和兴趣方向，生成 3-5 个创新项目方向建议，含核心创意/痛点/技术路线/创新亮点/可行性分析
- **模拟路演答辩**（仅 student / teacher / admin）：AI 扮演 3 位不同风格评委（温和/专业/犀利），各提出 1-2 个问题并给出参考回答要点，支持通用/技术/商业/挑战 4 种提问风格
- **批量审核助手**（仅 teacher / admin）：批量分析待审核项目，给出审核概览/逐项审核建议/优先级排序，辅助老师高效审核
- **智能反馈生成**（仅 teacher / admin）：生成项目审核反馈意见，支持修改建议/建议通过/建议驳回 3 种反馈类型
- **评审意见草稿**（仅 judge / admin）：帮助评委快速生成评审意见草稿，含项目概述/各维度评审意见/综合评审意见/建议追问问题
- **评分一致性检查**（仅 judge / admin）：检查评委评分与文字评价之间是否存在不一致，给出详细分析和改进建议

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
- 四角色独立引导步骤（学生 12 步 / 教师 9 步 / 评委 8 步 / 管理员 11 步）
- 各角色引导均包含 AI 智能体能力介绍（AgentPanel 入口 + 各角色可用能力说明）

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

***

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
│   ├── models/                       # 数据模型（14 个）
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
│   │   ├── ai_record.py             # AI 使用记录（ai_records 表）
│   │   ├── agent_task.py            # AI 智能体任务（agent_tasks 表）
│   │   └── agent_material_index.py  # AI 智能体材料索引（agent_material_indices 表）
│   │
│   ├── routes/                       # API 路由（14 个蓝图）
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
│   │   ├── registration.py           # /api         报名接口（学生+管理员）
│   │   └── agent.py                  # /api/agent   AI 智能体接口（材料索引/问答/体检/路演/评审辅助/推荐/任务）
│   │
│   ├── services/                     # 业务逻辑
│   │   ├── __init__.py
│   │   ├── ai_service.py             # AI 核心（通义千问 qwen-plus + LangChain + 统一对话路由 + 智能导航 + 意图识别 + 会话管理 + 流式输出 + 回答清洗）
│   │   ├── langchain_service.py      # LangChain 编排服务（RAG 问答 / BP 体检 / 路演稿 / 评审辅助 / 竞赛推荐 / 智能导航 / 意图检测）
│   │   ├── document_parser.py        # 文档解析服务（.docx / .pptx / .pdf 文本提取 + 分块）
│   │   ├── vector_store.py           # 向量存储服务（FAISS 索引 + BM25 混合检索 + Embedding）
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
│   ├── vector_stores/                # FAISS 向量索引存储目录
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
│       ├── api/                      # API 接口封装（12 个模块）
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
│       │   ├── ai.js                 # AI API（聊天/语音/ASR/TTS/流式/分析）
│       │   └── agent.js              # AI 智能体 API（材料索引/问答/体检/路演/评审辅助/推荐/任务）
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
│       └── views/                    # 页面视图（43 个 Vue 文件）
│           ├── ai-assistant/         # AI 助手（双标签页：分析工具 + 对话）
│           │   ├── index.vue
│           │   └── AgentPanel.vue    # AI 智能体面板（材料索引/问答/体检/路演/评审辅助/推荐）
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

***

## 环境要求

> 具体库版本信息见顶部 [项目环境依赖](#项目环境依赖) 章节

| 依赖      | 版本要求  | 说明                              |
| ------- | ----- | ------------------------------- |
| Python  | 3.10+ | 后端运行环境（指定使用 `newyolo` conda 环境） |
| Node.js | 18+   | 前端构建环境                          |
| MySQL   | 8.0+  | 关系型数据库                          |
| ffmpeg  | -     | 音频格式转换（ASR 功能需要，需加入系统 PATH）     |
| conda   | -     | Python 环境管理（`newyolo` 环境）       |

> **重要**：本项目指定使用 `newyolo` conda 环境，Python 解释器路径为 `D:\TOOLS\anaconda\envs\newyolo\python.exe`。`start.bat` 已配置使用此环境。

***

## 快速开始

> **仓库内容说明**：`.gitignore` 已配置忽略以下内容，clone 后这些目录会自动从源码运行，无需手动处理：
>
> - `frontend/dist/` — Vite `npm run build` 产生的打包产物，`npm run dev` 开发模式直接使用 `src/` 源码
> - `backend/vector_stores/` — FAISS/BM25 运行时生成的向量索引，启动服务后自动重建
> - `node_modules/`、`__pycache__/`、`venv/` — 依赖缓存
> - `backend/.env` — 含密钥的本地配置文件（`.gitignore` 不忽略，由协作者自行复制 `.env.example` 配置）

### 方式一：一键启动（推荐）

双击项目根目录的 `start.bat`，脚本会自动：

1. 停止占用 5000/5173 端口的旧进程
2. 检测并安装前端依赖（首次运行时 `npm install`）
3. 使用 `newyolo` conda 环境启动后端服务（端口 5000）
4. 启动前端开发服务器（端口 5173）

启动完成后访问：

- 前端：<http://localhost:5173>
- 后端：<http://localhost:5000>

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

# AI 智能体 - 通义千问 qwen-plus
GLM_API_KEY=your-glm-api-key
GLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
GLM_MODEL=qwen-plus

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

> **注意**：`.env.example` 包含完整配置模板（Flask/MyySQL/JWT/火山方舟 AI/实时语音/ASR），协作者按注释填入自己的凭证即可。

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

后端服务默认运行在 <http://localhost:5000>

> **启动流程**：`app.py` → `create_app()` → 加载配置 → 初始化扩展 → 注册蓝图 → 注册错误处理 → `init_database()` 检查数据库连接并创建表 → `app.run(host='0.0.0.0', port=5000, debug=True)`

#### 5. 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端服务默认运行在 <http://localhost:5173>

> **Vite 代理配置**：`/api` 和 `/uploads` 请求代理到 `http://localhost:5000`，CSP header 允许 `unsafe-eval`（Live2D SDK 需要）。

> **`frontend/dist/`** **目录说明**：`npm run build` 时 Vite 将 `src/` 源码编译打包后输出的静态文件目录，包含 `index.html`、编译后的 JS/CSS 以及 `public/` 目录的拷贝（Live2D 模型、Widget SDK 等）。此目录已被 `.gitignore` 忽略，协作者 clone 后 `npm run dev` 会自动使用源码目录运行，无需手动处理。

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

***

## 后端配置详情

| 配置项                                       | 默认值                                                                                 | 说明                 |
| ----------------------------------------- | ----------------------------------------------------------------------------------- | ------------------ |
| `SECRET_KEY`                              | `dev-secret-key-change-in-production`                                               | Flask 密钥（生产环境必须修改） |
| `SQLALCHEMY_DATABASE_URI`                 | `mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4` | 数据库连接字符串           |
| `SQLALCHEMY_TRACK_MODIFICATIONS`          | False                                                                               | 关闭修改追踪             |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_size`     | 10                                                                                  | 数据库连接池大小           |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_recycle`  | 3600                                                                                | 连接回收时间（秒）          |
| `SQLALCHEMY_ENGINE_OPTIONS.pool_pre_ping` | True                                                                                | 连接前检测可用性           |
| `JWT_SECRET_KEY`                          | `dev-jwt-secret-key-change-in-production`                                           | JWT 签名密钥（生产环境必须修改） |
| `JWT_ACCESS_TOKEN_EXPIRES`                | 24 小时                                                                               | Access Token 有效期   |
| `JWT_REFRESH_TOKEN_EXPIRES`               | 7 天                                                                                 | Refresh Token 有效期  |
| `MAX_CONTENT_LENGTH`                      | 4 GB                                                                                | 文件上传大小限制           |
| `DEFAULT_PAGE_SIZE`                       | 10                                                                                  | 默认分页大小             |
| `MAX_PAGE_SIZE`                           | 100                                                                                 | 最大分页大小             |
| `UPLOAD_FOLDER`                           | backend/uploads                                                                     | 文件上传目录             |
| `ALLOWED_EXTENSIONS`                      | png/jpg/jpeg/gif/bmp/doc/docx/ppt/pptx/pdf/mp4/avi/mov/wmv/mkv/zip/rar/7z           | 允许上传的文件类型          |

### CORS 配置

后端 CORS 仅允许以下来源访问 API：

- `http://localhost:5173`
- `http://127.0.0.1:5173`

允许的方法：GET / POST / PUT / DELETE / OPTIONS
允许的请求头：Content-Type / Authorization

### 环境配置类

| 配置类                 | 说明                 | 数据库          |
| ------------------- | ------------------ | ------------ |
| `DevelopmentConfig` | 开发环境（DEBUG=True）   | MySQL        |
| `ProductionConfig`  | 生产环境（DEBUG=False）  | MySQL        |
| `TestingConfig`     | 测试环境（TESTING=True） | SQLite 内存数据库 |

***

## 演示账号

| 用户名      | 密码         | 角色   | 真实姓名 | 邮箱                     |
| -------- | ---------- | ---- | ---- | ---------------------- |
| admin    | admin123   | 管理员  | 管理员  | <admin@example.com>    |
| student1 | student123 | 学生   | 张三   | <student1@example.com> |
| student2 | student123 | 学生   | 李四   | <student2@example.com> |
| student3 | student123 | 学生   | 王五   | <student3@example.com> |
| teacher1 | teacher123 | 指导老师 | 赵老师  | <teacher1@example.com> |
| teacher2 | teacher123 | 指导老师 | 钱老师  | <teacher2@example.com> |
| judge1   | judge123   | 评委   | 孙评委  | <judge1@example.com>   |
| judge2   | judge123   | 评委   | 周评委  | <judge2@example.com>   |

***

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

| 接口                   | 方法   | 认证  | 说明                                                                      |
| -------------------- | ---- | --- | ----------------------------------------------------------------------- |
| `/api/auth/register` | POST | 无   | 用户注册（username/password 必填，email/role/real\_name/phone/college/major 可选） |
| `/api/auth/login`    | POST | 无   | 用户登录（返回 `{token, user}`，JWT Token 存 localStorage）                       |
| `/api/auth/me`       | GET  | JWT | 获取当前登录用户信息                                                              |
| `/api/auth/logout`   | POST | JWT | 登出（前端清除 Token）                                                          |

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

| 接口                | 方法  | 认证  | 权限       | 说明       |
| ----------------- | --- | --- | -------- | -------- |
| `/api/users/`     | GET | JWT | admin    | 获取所有用户列表 |
| `/api/users/<id>` | GET | JWT | 本人或admin | 获取用户详情   |

### 竞赛接口

#### 公开接口（无需登录）

| 接口                                    | 方法  | 说明                                                            |
| ------------------------------------- | --- | ------------------------------------------------------------- |
| `/api/public/competitions`            | GET | 获取可报名竞赛列表（支持 keyword/category/level/status/page/per\_page 参数） |
| `/api/public/competitions/:id`        | GET | 获取竞赛详情（含赛道信息，自动增加浏览量）                                         |
| `/api/public/competitions/:id/tracks` | GET | 获取竞赛赛道列表                                                      |
| `/api/public/competition-categories`  | GET | 获取竞赛分类列表（10 个分类）                                              |

#### 管理员接口

| 接口                             | 方法     | 权限    | 说明                   |
| ------------------------------ | ------ | ----- | -------------------- |
| `/api/competitions`            | GET    | JWT   | 获取竞赛列表（支持 status 筛选） |
| `/api/competitions`            | POST   | admin | 创建竞赛                 |
| `/api/competitions/:id`        | PUT    | admin | 更新竞赛                 |
| `/api/competitions/:id`        | DELETE | admin | 删除竞赛                 |
| `/api/competitions/:id/tracks` | POST   | admin | 创建赛道                 |

### 报名接口

#### 学生接口

| 接口                                 | 方法     | 权限      | 说明                                   |
| ---------------------------------- | ------ | ------- | ------------------------------------ |
| `/api/registrations`               | POST   | student | 创建报名草稿（competition\_id/track\_id 必填） |
| `/api/registrations/:id`           | GET    | student | 查看报名详情（仅自己的）                         |
| `/api/registrations/:id`           | PUT    | student | 更新报名信息（已提交不可修改）                      |
| `/api/registrations/:id/members`   | POST   | student | 添加队员                                 |
| `/api/registration-members/:id`    | PUT    | student | 编辑队员                                 |
| `/api/registration-members/:id`    | DELETE | student | 删除队员                                 |
| `/api/registrations/:id/materials` | POST   | student | 上传报名材料（multipart/form-data）          |
| `/api/registration-materials/:id`  | DELETE | student | 删除报名材料                               |
| `/api/registrations/:id/submit`    | POST   | student | 提交报名（team\_name 必填）                  |
| `/api/my-registrations`            | GET    | student | 查看我的报名列表（含竞赛名/赛道名/海报）                |

#### 管理员接口

| 接口                                     | 方法   | 权限    | 说明                                                         |
| -------------------------------------- | ---- | ----- | ---------------------------------------------------------- |
| `/api/admin/registrations`             | GET  | admin | 获取所有报名记录（支持 competition\_id/status/keyword/page/per\_page） |
| `/api/admin/registrations/:id`         | GET  | admin | 查看报名详情                                                     |
| `/api/admin/registrations/:id/approve` | POST | admin | 审核通过报名                                                     |
| `/api/admin/registrations/:id/reject`  | POST | admin | 驳回报名（可附 remark）                                            |
| `/api/admin/registrations/statistics`  | GET  | admin | 报名统计数据                                                     |

### 项目接口 `/api/projects`

| 接口                         | 方法     | 权限            | 说明                                                 |
| -------------------------- | ------ | ------------- | -------------------------------------------------- |
| `/api/projects`            | GET    | JWT           | 获取项目列表（按角色过滤：学生看自己参与/负责的，教师看指导的，评委看已提交的，admin 看全部） |
| `/api/projects`            | POST   | student/admin | 创建项目（name 必填，stage 默认 idea，status 默认 draft）        |
| `/api/projects/:id`        | GET    | JWT           | 获取项目详情（含成员/文件数/任务数，需权限检查）                          |
| `/api/projects/:id`        | PUT    | JWT           | 更新项目（仅负责人或 admin，评审阶段不可修改）                         |
| `/api/projects/:id`        | DELETE | JWT           | 删除项目（仅 draft 状态，仅负责人或 admin）                       |
| `/api/projects/:id/submit` | POST   | JWT           | 提交项目进入评审（draft/need\_modify → submitted）           |

**项目查询参数**：keyword / status / stage / track / page / per\_page

### AI 分析工具 `/api/ai`

| 接口                             | 方法   | 认证  | 说明                    |
| ------------------------------ | ---- | --- | --------------------- |
| `/api/ai/project-summary`      | POST | JWT | 生成项目简介（AI 驱动，失败回退模板）  |
| `/api/ai/business-plan-advice` | POST | JWT | 商业计划书建议（AI 驱动，失败回退模板） |
| `/api/ai/risk-analysis`        | POST | JWT | 风险分析（AI 驱动，失败回退模板）    |
| `/api/ai/records`              | GET  | JWT | AI 使用记录（按时间倒序）        |

### AI 对话 `/api/ai`

| 接口                          | 方法   | 认证  | 说明                                                      |
| --------------------------- | ---- | --- | ------------------------------------------------------- |
| `/api/ai/chat`              | POST | JWT | 文本聊天（非流式，返回 reply/sessionId/model/mode）                 |
| `/api/ai/chat/stream`       | POST | JWT | 文本聊天（SSE 流式，text/event-stream，支持统一对话路由：自动识别导航/对话/智能体意图） |
| `/api/ai/voice/chat/stream` | POST | JWT | 语音聊天（SSE 流式，优先火山实时语音，回退文本模型）                            |

**请求参数**：`message`（必填）/ `question` / `scene`（默认"创新创业平台"）/ `sessionId` / `role`（当前用户角色，用于角色感知对话）

**统一对话路由机制**：

`/api/ai/chat/stream` 接口内置意图识别，根据用户消息自动分发到不同处理逻辑：

| 意图类型       | 触发条件                        | 处理方式                                    |
| ---------- | --------------------------- | --------------------------------------- |
| `navigate` | 用户输入包含导航意图（如"我想报名""帮我看看项目"） | 调用 `smart_navigate` 返回路由跳转建议，前端自动执行页面跳转 |
| `agent`    | 用户请求智能体能力（如"帮我体检商业计划书"）     | 调用对应 LangChain 智能体能力                    |
| `chat`     | 通用对话                        | 调用 qwen-plus 模型进行多轮对话                   |

**导航响应示例**：

```json
{
  "type": "navigate",
  "reply": "好的，我帮你跳转到竞赛广场~",
  "navigate": {
    "route": "/competitions",
    "reply": "好的，我帮你跳转到竞赛广场~"
  },
  "sessionId": "xxx"
}
```

**SSE 流式响应协议**：

```
sessionId:<session-id>     # 首行返回会话 ID
delta:<text-chunk>         # 增量文本
error:<error-message>      # 错误信息（不中断流）
done:1                     # 流结束标记
```

### 语音交互 `/api/ai`

| 接口                             | 方法   | 认证  | 说明                                                                          |
| ------------------------------ | ---- | --- | --------------------------------------------------------------------------- |
| `/api/ai/asr`                  | POST | JWT | 语音识别（multipart/form-data，豆包 ASR / faster-whisper 回退，返回 text/provider/model） |
| `/api/ai/tts/synthesize`       | POST | JWT | TTS 语音合成（火山 TTS，返回 audio\_url）                                              |
| `/api/ai/tts/audio/<filename>` | GET  | 无   | 获取合成音频文件（MP3）                                                               |
| `/api/ai/voice/config`         | GET  | JWT | 语音配置信息（realtime\_configured/speaker/bot\_name/input\_mod）                   |

### Live2D / 健康 `/api/ai`

| 接口                    | 方法  | 认证 | 说明                                                                |
| --------------------- | --- | -- | ----------------------------------------------------------------- |
| `/api/ai/expressions` | GET | 无  | 获取表情列表（base 10 个 + overlay 2 个含概率）                                |
| `/api/ai/model-info`  | GET | 无  | 获取 Live2D 模型信息（name: huahuo, path: /live2d/huahuo/火花.model3.json） |
| `/api/ai/health`      | GET | 无  | AI 服务健康检查（chat\_configured / voice\_realtime\_configured / model） |

### 看板接口 `/api/dashboard`

| 接口                      | 方法  | 权限    | 说明                                            |
| ----------------------- | --- | ----- | --------------------------------------------- |
| `/api/dashboard/stats`  | GET | admin | 管理员统计数据（用户/项目/文件/评审/竞赛/AI 使用，含角色分布/阶段分布/赛道分布） |
| `/api/dashboard/recent` | GET | admin | 最近数据（最近 5 个项目/文件/评审）                          |

### 系统接口

| 接口                         | 方法  | 认证 | 说明                       |
| -------------------------- | --- | -- | ------------------------ |
| `/api/health`              | GET | 无  | 系统健康检查（数据库连接状态，503 表示降级） |
| `/uploads/<path:filename>` | GET | 无  | 静态文件访问（上传文件，含海报/报名材料等）   |

### 其他接口

| 接口前缀             | 说明                                                      |
| ---------------- | ------------------------------------------------------- |
| `/api/`          | 成员（member.py）/ 文件（file.py）/ 任务（task.py）/ 评审（review\.py） |
| `/api/teams`     | 团队管理                                                    |
| `/api/materials` | 材料管理                                                    |

### AI 智能体 `/api/agent`

| 接口 | 方法 | 认证 | 权限 | 说明 |
|------|------|------|------|------|
| `/api/agent/index-materials` | POST | JWT | 所有角色 | 索引项目/报名材料（支持 .docx/.pptx/.pdf，自动解析文档并建立向量索引） |
| `/api/agent/material-qa` | POST | JWT | 所有角色 | AI 材料问答（基于已索引材料进行 RAG 检索问答） |
| `/api/agent/bp-check` | POST | JWT | 所有角色 | 商业计划书体检（多维度结构化审查，**不返回具体评分**） |
| `/api/agent/roadshow` | POST | JWT | student/teacher/admin（评委不允许） | 路演稿生成（支持 3/5/8 分钟时长，formal/passionate/concise/story 风格） |
| `/api/agent/review-assist` | POST | JWT | teacher/judge/admin | 评审辅助（项目亮点/风险/改进建议摘要，**严格不返回具体分数，仅提供定性评价参考**） |
| `/api/agent/competition-recommend` | POST | JWT | student/admin | 智能竞赛推荐（根据项目信息匹配推荐竞赛+推荐理由） |
| `/api/agent/navigate` | POST | JWT | 所有角色 | 智能引航（模糊指令识别，返回路由跳转建议） |
| `/api/agent/project-idea` | POST | JWT | student/admin | 项目创意生成（基于技能/兴趣/竞赛方向生成创意建议） |
| `/api/agent/mock-defense` | POST | JWT | student/teacher/admin | 模拟路演答辩（AI 扮演 3 位评委提问，支持 general/technical/business/tough 类型） |
| `/api/agent/batch-review` | POST | JWT | teacher/admin | 批量审核助手（批量分析待审核项目，给出审核建议） |
| `/api/agent/smart-feedback` | POST | JWT | teacher/admin | 智能反馈生成（生成项目审核反馈意见，支持 modify/approve/reject 类型） |
| `/api/agent/review-draft` | POST | JWT | judge/admin | 评审意见草稿（生成评审意见草稿，含各维度定性评价） |
| `/api/agent/score-check` | POST | JWT | judge/admin | 评分一致性检查（检查评分与文字评价是否一致） |
| `/api/agent/capabilities` | GET | JWT | 所有角色 | 获取当前角色可用的 AI 智能体能力列表 |
| `/api/agent/tasks` | GET | JWT | 所有角色 | 任务记录列表（分页，按时间倒序） |
| `/api/agent/tasks/<id>` | GET | JWT | 所有角色 | 任务详情（含输入参数和 AI 输出结果） |

**索引材料请求示例**：

```json
{
  "project_id": 1,
  "registration_id": null,
  "file_ids": [1, 2, 3]
}
```

**材料问答请求示例**：

```json
{
  "project_id": 1,
  "question": "这个项目的核心技术方案是什么？"
}
```

**商业计划书体检请求示例**：

```json
{
  "project_id": 1
}
```

**路演稿生成请求示例**：

```json
{
  "project_id": 1,
  "duration": 5,
  "style": "formal"
}
```

> 路演稿 `duration` 支持 3/5/8（分钟），`style` 支持 formal（正式）/passionate（激情）/concise（精炼）/story（故事）。

**评审辅助请求示例**：

```json
{
  "project_id": 1
}
```

> **重要**：评审辅助端点严格不返回具体分数，仅提供项目亮点、风险点和改进建议的定性评价参考，避免影响评审公正性。

**智能竞赛推荐请求示例**：

```json
{
  "project_id": 1
}
```

**智能引航请求示例**：

```json
{
  "message": "我想报名互联网+比赛"
}
```

**项目创意生成请求示例**：

```json
{
  "skills": "Python、产品设计",
  "interests": "环保、教育"
}
```

**模拟路演答辩请求示例**：

```json
{
  "project_id": 1,
  "question_type": "tough"
}
```

> `question_type` 支持 general（通用）/technical（技术）/business（商业）/tough（挑战）。

**智能反馈生成请求示例**：

```json
{
  "project_id": 1,
  "feedback_type": "modify"
}
```

> `feedback_type` 支持 modify（修改建议）/approve（建议通过）/reject（建议驳回）。

**评审意见草稿请求示例**：

```json
{
  "project_id": 1
}
```

**评分一致性检查请求示例**：

```json
{
  "review_data": {
    "innovation_score": 85,
    "feasibility_score": 80,
    "comment": "项目创新性一般，可行性较好"
  }
}
```

***

## 路由配置

### 公共路由（无需登录）

| 路径          | 组件                 | 说明  |
| ----------- | ------------------ | --- |
| `/login`    | login/index.vue    | 登录页 |
| `/register` | login/register.vue | 注册页 |

### 平台页面（所有角色，无侧边栏）

| 路径                    | 组件                            | 说明    |
| --------------------- | ----------------------------- | ----- |
| `/portal`             | portal/PortalHome.vue         | 平台首页  |
| `/competitions`       | portal/CompetitionSquare.vue  | 竞赛广场  |
| `/competitions/:id`   | portal/CompetitionDetail.vue  | 竞赛详情  |
| `/training-camps`     | portal/TrainingCamps.vue      | 训练营   |
| `/training-camps/:id` | portal/TrainingCampDetail.vue | 训练营详情 |
| `/courses`            | portal/Courses.vue            | 在线课程  |
| `/courses/:id`        | portal/CourseDetail.vue       | 课程详情  |
| `/industry-topics`    | portal/IndustryTopics.vue     | 产业命题  |

### 通用路由（所有角色）

| 路径                      | 组件                     | 说明                               |
| ----------------------- | ---------------------- | -------------------------------- |
| `/dashboard`            | dashboard/index.vue    | 工作台（按角色加载不同看板）                   |
| `/projects/:id`         | projects/detail.vue    | 项目详情                             |
| `/projects/:id/edit`    | projects/edit.vue      | 编辑项目                             |
| `/projects/:id/members` | projects/members.vue   | 团队成员                             |
| `/projects/:id/files`   | projects/files.vue     | 项目材料                             |
| `/projects/:id/tasks`   | projects/tasks.vue     | 任务进度                             |
| `/reviews/:id`          | reviews/detail.vue     | 评审详情                             |
| `/ai-assistant`         | ai-assistant/index.vue | AI 助手备用页面（hidden: true，不显示在导航菜单） |

### 学生专属路由

| 路径                           | 组件                             | 说明           |
| ---------------------------- | ------------------------------ | ------------ |
| `/my-projects`               | projects/my-projects.vue       | 我的项目         |
| `/create-project`            | projects/create.vue            | 创建项目         |
| `/competitions/:id/register` | portal/CompetitionRegister.vue | 竞赛报名         |
| `/my-registrations`          | portal/MyRegistrations.vue     | 我的赛事         |
| `/certificates`              | portal/Certificates.vue        | 证书成果         |
| `/accept-topic/:id`          | portal/AcceptTopic.vue         | 承接命题（填写承接信息） |

### 教师专属路由

| 路径                | 组件                          | 说明   |
| ----------------- | --------------------------- | ---- |
| `/guide-projects` | projects/guide-projects.vue | 指导项目 |
| `/project-review` | reviews/teacher-review\.vue | 项目审核 |

### 评委专属路由

| 路径                 | 组件                  | 说明    |
| ------------------ | ------------------- | ----- |
| `/pending-reviews` | reviews/pending.vue | 待评审项目 |
| `/review-history`  | reviews/history.vue | 评审记录  |

### 管理员专属路由

| 路径                         | 组件                               | 说明     |
| -------------------------- | -------------------------------- | ------ |
| `/user-management`         | admin/users.vue                  | 用户管理   |
| `/project-management`      | admin/projects.vue               | 项目管理   |
| `/competition-management`  | competitions/index.vue           | 比赛批次管理 |
| `/registration-management` | admin/RegistrationManagement.vue | 报名管理   |
| `/review-management`       | admin/reviews.vue                | 评审管理   |

### 路由守卫逻辑

1. **页面标题**：自动设置为 `{title} - 创新创业平台`
2. **公共页面**：已登录用户访问 /login 或 /register 时重定向到 /portal
3. **登录检查**：未登录用户重定向到 /login
4. **用户信息加载**：首次访问时调用 `userStore.init()` 加载用户信息
5. **角色权限检查**：路由 `meta.roles` 指定允许访问的角色，无权限时重定向到 /dashboard
6. **404 匹配**：未匹配路由显示 404 页面

***

## 数据库模型

### 表结构总览

| 模型                      | 表名                         | 说明         |
| ----------------------- | -------------------------- | ---------- |
| User                    | users                      | 用户信息       |
| Competition             | competitions               | 竞赛信息       |
| CompetitionTrack        | competition\_tracks        | 竞赛赛道       |
| CompetitionRegistration | competition\_registrations | 竞赛报名       |
| RegistrationMember      | registration\_members      | 报名队员       |
| RegistrationMaterial    | registration\_materials    | 报名材料       |
| Project                 | projects                   | 项目信息       |
| ProjectMember           | project\_members           | 项目成员       |
| ProjectFile             | project\_files             | 项目文件       |
| ProjectTask             | project\_tasks             | 项目任务       |
| Review                  | reviews                    | 评审记录       |
| AiRecord                | ai\_records                | AI 使用记录    |
| AgentTask               | agent\_tasks               | AI 智能体任务   |
| AgentMaterialIndex      | agent\_material\_indices   | AI 智能体材料索引 |

### 模型详细字段

#### User（用户信息）

| 字段             | 类型           | 说明                                         |
| -------------- | ------------ | ------------------------------------------ |
| id             | Integer (PK) | 用户 ID                                      |
| username       | String(80)   | 用户名（唯一，索引）                                 |
| password\_hash | String(255)  | 密码哈希（Werkzeug generate\_password\_hash）    |
| real\_name     | String(50)   | 真实姓名                                       |
| email          | String(120)  | 邮箱（唯一）                                     |
| phone          | String(20)   | 手机号                                        |
| role           | String(20)   | 角色（student/teacher/judge/admin，默认 student） |
| college        | String(100)  | 学院                                         |
| major          | String(100)  | 专业                                         |
| avatar         | String(255)  | 头像 URL                                     |
| is\_active     | Boolean      | 是否启用（默认 True）                              |
| created\_at    | DateTime     | 创建时间                                       |
| updated\_at    | DateTime     | 更新时间                                       |

**关系**：projects（负责的项目）/ teacher\_projects（指导的项目）/ reviews（评审记录）/ tasks（分配的任务）/ ai\_records（AI 使用记录）

**方法**：`set_password(password)` / `check_password(password)` / `is_admin()` / `is_teacher()` / `is_judge()` / `is_student()`

#### Competition（竞赛信息）

| 字段                  | 类型           | 说明                                                    |
| ------------------- | ------------ | ----------------------------------------------------- |
| id                  | Integer (PK) | 竞赛 ID                                                 |
| name                | String(200)  | 竞赛名称                                                  |
| description         | Text         | 竞赛描述                                                  |
| organizer           | String(200)  | 主办方                                                   |
| category            | String(50)   | 分类（创新创业/人工智能/数字经济/乡村振兴/电子商务/软件开发/智能制造/职业规划/公益实践/产业命题） |
| level               | String(20)   | 级别（校级/省级/国家级/企业命题）                                    |
| registration\_start | DateTime     | 报名开始时间                                                |
| registration\_end   | DateTime     | 报名截止时间                                                |
| competition\_start  | DateTime     | 比赛开始时间                                                |
| competition\_end    | DateTime     | 比赛结束时间                                                |
| status              | String(20)   | 状态（draft/active/ended/archived/upcoming）              |
| poster\_url         | String(500)  | 海报 URL                                                |
| tags                | String(500)  | 标签（逗号分隔，to\_dict 时转为数组）                               |
| target\_audience    | String(500)  | 目标受众                                                  |
| requirements        | Text         | 参赛要求                                                  |
| awards              | Text         | 奖项设置                                                  |
| schedule            | Text         | 赛程安排                                                  |
| view\_count         | Integer      | 浏览量（默认 0）                                             |
| registration\_count | Integer      | 报名数（默认 0）                                             |
| created\_at         | DateTime     | 创建时间                                                  |
| updated\_at         | DateTime     | 更新时间                                                  |

**关系**：projects / tracks（级联删除）/ registrations（级联删除）

#### CompetitionTrack（竞赛赛道）

| 字段                     | 类型           | 说明            |
| ---------------------- | ------------ | ------------- |
| id                     | Integer (PK) | 赛道 ID         |
| competition\_id        | Integer (FK) | 所属竞赛          |
| name                   | String       | 赛道名称          |
| description            | Text         | 赛道描述          |
| category               | String       | 赛道分类          |
| team\_min              | Integer      | 最小团队人数（默认 1）  |
| team\_max              | Integer      | 最大团队人数（默认 5）  |
| material\_requirements | Text         | 材料要求          |
| status                 | String       | 赛道状态（默认 open） |

#### CompetitionRegistration（竞赛报名）

| 字段              | 类型           | 说明                                              |
| --------------- | ------------ | ----------------------------------------------- |
| id              | Integer (PK) | 报名 ID                                           |
| competition\_id | Integer (FK) | 竞赛 ID                                           |
| track\_id       | Integer (FK) | 赛道 ID                                           |
| project\_id     | Integer      | 关联项目 ID                                         |
| leader\_id      | Integer (FK) | 队长用户 ID                                         |
| team\_name      | String       | 队伍名称                                            |
| school          | String       | 学校                                              |
| college         | String       | 学院                                              |
| major           | String       | 专业                                              |
| teacher\_name   | String       | 指导老师姓名                                          |
| teacher\_phone  | String       | 指导老师电话                                          |
| contact\_phone  | String       | 联系电话                                            |
| contact\_email  | String       | 联系邮箱                                            |
| status          | String       | 状态（draft/submitted/approved/rejected/withdrawn） |
| remark          | Text         | 备注（驳回原因等）                                       |
| submitted\_at   | DateTime     | 提交时间                                            |
| created\_at     | DateTime     | 创建时间                                            |
| updated\_at     | DateTime     | 更新时间                                            |

**关系**：members / materials

#### RegistrationMember（报名队员）

| 字段               | 类型           | 说明                            |
| ---------------- | ------------ | ----------------------------- |
| id               | Integer (PK) | 队员 ID                         |
| registration\_id | Integer (FK) | 报名记录 ID                       |
| name             | String       | 姓名                            |
| student\_no      | String       | 学号                            |
| college          | String       | 学院                            |
| major            | String       | 专业                            |
| phone            | String       | 手机号                           |
| email            | String       | 邮箱                            |
| role\_in\_team   | String       | 队内角色（leader/member，默认 member） |

#### RegistrationMaterial（报名材料）

| 字段               | 类型           | 说明            |
| ---------------- | ------------ | ------------- |
| id               | Integer (PK) | 材料 ID         |
| registration\_id | Integer (FK) | 报名记录 ID       |
| uploader\_id     | Integer (FK) | 上传者 ID        |
| material\_type   | String       | 材料类型          |
| file\_name       | String       | 文件名（UUID 重命名） |
| original\_name   | String       | 原始文件名         |
| file\_path       | String       | 文件存储路径        |
| file\_type       | String       | 文件扩展名         |
| file\_size       | Integer      | 文件大小（字节）      |

#### Project（项目信息）

| 字段              | 类型                          | 说明                                                                                  |
| --------------- | --------------------------- | ----------------------------------------------------------------------------------- |
| id              | Integer (PK)                | 项目 ID                                                                               |
| name            | String(100)                 | 项目名称                                                                                |
| description     | Text                        | 项目描述                                                                                |
| category        | String(50)                  | 项目类别                                                                                |
| track           | String(50)                  | 所属赛道                                                                                |
| stage           | String(30)                  | 当前阶段（idea/prototype/proof/development/production，默认 idea）                           |
| status          | String(30)                  | 项目状态（draft/submitted/teacher\_review/need\_modify/judging/passed/rejected，默认 draft） |
| leader\_id      | Integer (FK → users)        | 负责人 ID                                                                              |
| teacher\_id     | Integer (FK → users)        | 指导老师 ID                                                                             |
| competition\_id | Integer (FK → competitions) | 关联竞赛 ID                                                                             |
| start\_date     | Date                        | 开始日期                                                                                |
| end\_date       | Date                        | 结束日期                                                                                |
| progress        | Integer                     | 进度百分比（默认 0）                                                                         |
| created\_at     | DateTime                    | 创建时间                                                                                |
| updated\_at     | DateTime                    | 更新时间                                                                                |

**关系**：members（级联删除）/ files（级联删除）/ tasks（级联删除）/ reviews（级联删除）/ ai\_records

#### ProjectMember（项目成员）

| 字段                | 类型           | 说明    |
| ----------------- | ------------ | ----- |
| id                | Integer (PK) | 成员 ID |
| project\_id       | Integer (FK) | 项目 ID |
| user\_id          | Integer (FK) | 用户 ID |
| member\_name      | String       | 成员姓名  |
| role\_in\_project | String       | 项目角色  |
| responsibility    | String       | 职责    |

#### ProjectFile（项目文件）

| 字段             | 类型           | 说明     |
| -------------- | ------------ | ------ |
| id             | Integer (PK) | 文件 ID  |
| project\_id    | Integer (FK) | 项目 ID  |
| filename       | String       | 文件名    |
| original\_name | String       | 原始文件名  |
| file\_type     | String       | 文件类型   |
| material\_type | String       | 材料类型   |
| file\_size     | Integer      | 文件大小   |
| storage\_path  | String       | 存储路径   |
| uploader\_id   | Integer (FK) | 上传者 ID |

#### ProjectTask（项目任务）

| 字段            | 类型                   | 说明     |
| ------------- | -------------------- | ------ |
| id            | Integer (PK)         | 任务 ID  |
| project\_id   | Integer (FK)         | 项目 ID  |
| title         | String               | 任务标题   |
| description   | Text                 | 任务描述   |
| assignee\_id  | Integer (FK → users) | 负责人 ID |
| status        | String               | 任务状态   |
| priority      | String               | 优先级    |
| deadline      | DateTime             | 截止日期   |
| completed\_at | DateTime             | 完成时间   |

#### Review（评审记录）

| 字段                  | 类型                   | 说明    |
| ------------------- | -------------------- | ----- |
| id                  | Integer (PK)         | 评审 ID |
| project\_id         | Integer (FK)         | 项目 ID |
| judge\_id           | Integer (FK → users) | 评委 ID |
| innovation\_score   | Integer              | 创新性评分 |
| feasibility\_score  | Integer              | 可行性评分 |
| market\_score       | Integer              | 市场评分  |
| team\_score         | Integer              | 团队评分  |
| business\_score     | Integer              | 商业评分  |
| technology\_score   | Integer              | 技术评分  |
| presentation\_score | Integer              | 展示评分  |
| total\_score        | Float                | 总分    |
| comment             | Text                 | 评审意见  |

#### AiRecord（AI 使用记录）

| 字段          | 类型                      | 说明                                          |
| ----------- | ----------------------- | ------------------------------------------- |
| id          | Integer (PK)            | 记录 ID                                       |
| user\_id    | Integer (FK → users)    | 用户 ID                                       |
| project\_id | Integer (FK → projects) | 项目 ID                                       |
| type        | String                  | 类型（summary/business\_advice/risk\_analysis） |
| prompt      | Text                    | 输入提示                                        |
| result      | Text                    | AI 输出结果                                     |
| created\_at | DateTime                | 创建时间                                        |

#### AgentTask（AI 智能体任务）

| 字段               | 类型                      | 说明                                                                                                     |
| ---------------- | ----------------------- | ------------------------------------------------------------------------------------------------------ |
| id               | Integer (PK)            | 任务 ID                                                                                                  |
| user\_id         | Integer (FK → users)    | 发起用户 ID                                                                                                |
| project\_id      | Integer (FK → projects) | 关联项目 ID                                                                                                |
| registration\_id | Integer                 | 关联报名 ID（可选）                                                                                            |
| task\_type       | String                  | 任务类型（material\_qa / bp\_check / roadshow / review\_assist / competition\_recommend / index\_materials） |
| status           | String                  | 任务状态（pending / processing / completed / failed，默认 pending）                                             |
| input\_params    | Text                    | 输入参数（JSON 格式）                                                                                          |
| result           | Text                    | AI 输出结果                                                                                                |
| error\_message   | Text                    | 错误信息（失败时记录）                                                                                            |
| created\_at      | DateTime                | 创建时间                                                                                                   |
| updated\_at      | DateTime                | 更新时间                                                                                                   |

#### AgentMaterialIndex（AI 智能体材料索引）

| 字段               | 类型                            | 说明                                                       |
| ---------------- | ----------------------------- | -------------------------------------------------------- |
| id               | Integer (PK)                  | 索引 ID                                                    |
| project\_id      | Integer (FK → projects)       | 关联项目 ID                                                  |
| registration\_id | Integer                       | 关联报名 ID（可选）                                              |
| file\_id         | Integer (FK → project\_files) | 关联文件 ID                                                  |
| file\_name       | String                        | 文件名                                                      |
| file\_type       | String                        | 文件类型（docx/pptx/pdf）                                      |
| chunk\_count     | Integer                       | 文本分块数量                                                   |
| index\_status    | String                        | 索引状态（pending / indexing / completed / failed，默认 pending） |
| index\_path      | String                        | FAISS 索引文件路径                                             |
| created\_at      | DateTime                      | 创建时间                                                     |
| updated\_at      | DateTime                      | 更新时间                                                     |

***

## 用户角色与权限

### 角色定义

| 角色   | 标识        | 层级 | 说明           |
| ---- | --------- | -- | ------------ |
| 学生   | `student` | 1  | 项目负责人 / 团队成员 |
| 指导老师 | `teacher` | 2  | 项目指导         |
| 评委   | `judge`   | 3  | 项目评审         |
| 管理员  | `admin`   | 4  | 系统管理         |

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

| 角色   | 侧边栏菜单                                       |
| ---- | ------------------------------------------- |
| 学生   | 工作台、我的赛事、我的项目、创建项目、训练营、在线课程、产业命题、证书成果、AI 助手 |
| 指导老师 | 工作台、指导项目、项目审核、训练营、在线课程、产业命题、AI 助手           |
| 评委   | 工作台、待评审项目、评审记录、AI 助手                        |
| 管理员  | 工作台、比赛批次管理、报名管理、项目管理、评审管理、用户管理、数据看板、AI 助手   |

### AI 智能体权限矩阵

| AI 智能体能力   | 学生 | 指导老师 | 评委 | 管理员 | 说明                                      |
| ---------- | -- | ---- | -- | --- | --------------------------------------- |
| 智能引航 | ✅ | ✅ | ✅ | ✅ | 所有角色可用，模糊指令识别与页面跳转 |
| AI 材料问答    | ✅  | ✅    | ✅  | ✅   | 所有角色可对自己参与/负责的项目材料进行问答                  |
| AI 商业计划书体检 | ✅  | ✅    | ✅  | ✅   | 所有角色可对项目商业计划书进行体检                       |
| AI 路演稿生成   | ✅  | ✅    | ❌  | ✅   | 评委不允许使用路演稿生成功能                          |
| AI 评审辅助    | ❌  | ✅    | ✅  | ✅   | 仅 teacher/judge/admin 可使用，**严格不返回具体分数** |
| 智能竞赛推荐     | ✅  | ❌    | ❌  | ✅   | 仅 student/admin 可使用                     |
| 项目创意生成 | ✅ | ❌ | ❌ | ✅ | 仅 student/admin 可使用，无需关联项目 |
| 模拟路演答辩 | ✅ | ✅ | ❌ | ✅ | 学生和教师可用，AI 扮演评委进行模拟答辩 |
| 批量审核助手 | ❌ | ✅ | ❌ | ✅ | 仅 teacher/admin 可使用，批量分析待审核项目 |
| 智能反馈生成 | ❌ | ✅ | ❌ | ✅ | 仅 teacher/admin 可使用，生成项目审核反馈意见 |
| 评审意见草稿 | ❌ | ❌ | ✅ | ✅ | 仅 judge/admin 可使用，生成评审意见草稿 |
| 评分一致性检查 | ❌ | ❌ | ✅ | ✅ | 仅 judge/admin 可使用，检查评分与评价是否一致 |
| 索引项目材料     | ✅  | ✅    | ✅  | ✅   | 所有角色可索引自己参与项目的材料                        |
| 查看任务记录     | ✅  | ✅    | ✅  | ✅   | 所有角色可查看自己的任务记录                          |

***

## 设计系统

### CSS 变量体系

项目使用 `design-system.css` 定义统一的设计变量：

| 类别  | 变量前缀                                                | 说明                         |
| --- | --------------------------------------------------- | -------------------------- |
| 主色调 | `--primary-50` \~ `--primary-900`                   | Cyan 专业色系（#06b6d4）         |
| 中性色 | `--gray-50` \~ `--gray-900`                         | 灰色系（Tailwind 风格）           |
| 语义色 | `--success/warning/danger/info`                     | 成功/警告/危险/信息色               |
| 背景  | `--bg-primary/secondary/tertiary/sidebar`           | 页面/侧边栏背景色                  |
| 文字  | `--text-primary/secondary/tertiary/inverse/sidebar` | 多层级文字色                     |
| 阴影  | `--shadow-sm/md/lg/xl`                              | 4 级阴影                      |
| 字体  | `--font-heading/body`                               | Poppins + Open Sans + 中文回退 |
| 间距  | `--space-1` \~ `--space-12`                         | 0.25rem \~ 3rem            |
| 圆角  | `--radius-sm/md/lg/xl`                              | 0.375rem \~ 1rem           |
| 过渡  | `--transition-fast/normal/slow`                     | 150ms/200ms/300ms          |
| 布局  | `--sidebar-width/collapsed-width/header-height`     | 240px/64px/64px            |

### 暗黑模式预留

通过 `data-theme="dark"` 属性切换暗黑模式变量（尚未启用）。

***

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

***

## 常见问题

### 1. 数据库连接失败

1. 检查 MySQL 服务是否已启动
2. 确认数据库 `innovation_competition` 已创建（`utf8mb4` 字符集）
3. 检查 `.env` 文件中的 `DATABASE_URL` 配置
4. 确认用户名和密码正确
5. 检查 MySQL 连接池配置（pool\_size: 10, pool\_recycle: 3600）

### 2. AI 对话失败

1. 检查 `.env` 中的 `GLM_API_KEY` 是否正确（通义千问 qwen-plus 为主要对话模型）
2. 确认通义千问 DashScope API 可访问（`https://dashscope.aliyuncs.com`）
3. 检查 `GLM_BASE_URL` 是否配置为 `https://dashscope.aliyuncs.com/compatible-mode/v1`
4. 检查 `GLM_MODEL` 是否为 `qwen-plus`
5. 如使用火山方舟模型，检查 `ARK_API_KEY` 和 `ARK_BASE_URL` 是否正确
6. 检查网络连接
7. 访问 `/api/ai/health` 查看配置状态（chat\_configured / voice\_realtime\_configured / model）
8. AI 对话超时已设为 3 分钟（CHUNK\_TIMEOUT = 180000ms），含重试机制（最多 2 次）

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

### 12. AI 智能体接口超时 / 502

1. LLM 密集型接口（BP 体检、路演稿、评审辅助）耗时较长，Vite 代理超时已设为 120 秒
2. 偶发 502 可重试，通常第二次请求会成功
3. 前端 API 客户端超时已设为 120 秒（`agentTimeout`）
4. 检查 `.env` 中 `GLM_API_KEY` 和 `GLM_BASE_URL` 是否正确（通义千问为主要模型）
5. 如使用火山方舟模型，检查 `ARK_API_KEY` 和 `ARK_BASE_URL`

### 13. FAISS 向量索引不可用

1. 检查 `.env` 中 `GLM_API_KEY` 和 `GLM_BASE_URL` 是否正确配置（通义千问 Embedding）
2. FAISS Embedding 优先使用通义千问 API，不可用时回退检查 `ARK_API_KEY` 和 `ARK_BASE_URL`
3. 不可用时自动降级为 BM25 + 关键词检索
4. 检查 `backend/vector_stores/` 目录下是否有索引文件
5. BM25 中文分词依赖 jieba 库，确认已安装

### 14. AI 评审辅助返回 403

1. 评审辅助仅限 teacher / judge / admin 角色使用
2. 学生角色调用会返回 403 "权限不足，需要 teacher 及以上角色"
3. 这是预期行为，评审辅助严格不返回具体分数

***

## 当前开发状态

### 已完成功能模块

| 模块          | 状态   | 说明                                                            |
| ----------- | ---- | ------------------------------------------------------------- |
| 用户认证        | ✅ 完成 | 注册/登录/JWT Token/角色权限/账号禁用                                     |
| 竞赛广场        | ✅ 完成 | 公开竞赛列表/详情/海报/时间安排/奖项设置/分类筛选/浏览量统计                             |
| 竞赛管理        | ✅ 完成 | 管理员 CRUD/赛道管理/状态控制                                            |
| 竞赛报名        | ✅ 完成 | 学生报名/队员管理/材料上传/提交/管理员审核/驳回/统计                                 |
| 训练营         | ✅ 完成 | 列表/详情/海报/章节大纲/讲师信息                                            |
| 在线课程        | ✅ 完成 | 列表/详情/海报/章节视频/进度跟踪                                            |
| 产业命题        | ✅ 完成 | 命题列表/承接填写页/跳转创建项目                                             |
| 项目管理        | ✅ 完成 | 创建/编辑/详情/成员/文件/任务/提交评审/删除                                     |
| AI 智能对话     | ✅ 完成 | 流式输出/重试机制/3分钟超时/会话管理/回答清洗/统一对话路由/智能导航/角色感知                    |
| AI 分析工具     | ✅ 完成 | 项目简介/商业计划书/风险分析/深色主题适配                                        |
| 语音交互        | ✅ 完成 | ASR/TTS/实时语音对话/可拖拽面板                                          |
| Live2D 虚拟形象 | ✅ 完成 | 全屏拖拽/表情联动/口型驱动/位置持久化/拖拽按钮跟随                                   |
| 证书成果        | ✅ 完成 | 证书列表/获奖记录/查看详情弹窗/证书图片                                         |
| 我的赛事        | ✅ 完成 | 报名列表/海报封面/状态跟踪                                                |
| 全局引导系统      | ✅ 完成 | 首次登录引导/步骤导航/路由跳转/状态持久化                                        |
| 数据看板        | ✅ 完成 | 4 角色看板/统计图表/动态数据/最近数据                                         |
| 管理后台        | ✅ 完成 | 用户/项目/竞赛/报名/评审管理                                              |
| 首页数字雨       | ✅ 完成 | 全局 Canvas 数字雨背景/科幻风格/扫描线/全屏铺满                                 |
| Banner 动画   | ✅ 完成 | 竞赛/训练营/课程各具独特渐变色+光球动画                                         |
| AI 项目智能体 | ✅ 完成 | 12 大 AI 能力（智能引航/材料问答/BP 体检/路演稿/评审辅助/竞赛推荐/项目创意/模拟答辩/批量审核/智能反馈/评审草稿/评分检查）+ LangChain + FAISS + BM25 |
| 一键启动        | ✅ 完成 | start.bat 自动检测依赖+启动前后端                                        |

### 正在进行的开发任务

| 任务         | 优先级 | 说明                   |
| ---------- | --- | -------------------- |
| 进度条横向滚动    | 高   | 多步骤流程场景的横向拖拽/滑动查看    |
| 产业命题后端 API | 中   | 承接命题数据持久化、命题 CRUD 接口 |
| 训练营/课程学习进度 | 中   | 视频观看进度、章节完成状态        |
| 评审打分优化     | 中   | 多维度评分、评分模板、评审意见模板    |
| 移动端适配      | 低   | 响应式布局优化、触屏交互         |

### 未来规划

- **消息通知系统**：站内信、竞赛状态变更通知、报名审核通知
- **数据导出**：报名表 Excel 导出、评审结果导出、证书 PDF 下载
- **团队协作**：项目讨论区、文件版本管理、任务看板
- **AI 能力扩展**：项目匹配推荐优化、竞赛策略分析、多模态材料理解
- **性能优化**：前端懒加载、后端缓存、CDN 静态资源
- **暗黑模式**：设计系统已预留暗黑模式变量，待实现切换逻辑

***

## 调试指南

### 前端调试

#### 开发工具

| 工具              | 用途                       | 访问方式          |
| --------------- | ------------------------ | ------------- |
| Vue DevTools    | 组件树/状态/路由/事件/Pinia Store | 浏览器扩展         |
| Chrome DevTools | 网络/性能/内存/Console         | F12           |
| Vite DevServer  | HMR/代理/构建                | `npm run dev` |

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

| 日志前缀              | 位置                  | 说明              |
| ----------------- | ------------------- | --------------- |
| `[AI Stream]`     | HuahuoAssistant.vue | AI 流式对话重试/超时/错误 |
| `[CreateProject]` | create.vue          | 项目创建请求数据/错误详情   |
| `[Live2D]`        | HuahuoAssistant.vue | 模型加载/表情切换/拖拽位置  |

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

| 日志内容              | 说明                           |
| ----------------- | ---------------------------- |
| `SQLAlchemy` 查询日志 | 设置 `SQLALCHEMY_ECHO=True` 开启 |
| AI 会话管理日志         | 会话创建/清理/过期检查                 |
| TTS 缓存统计          | 缓存命中率/文件数量/总大小               |
| 流式对话日志            | SSE 连接/断开/错误                 |
| 数据库连接日志           | `init_database()` 输出连接状态     |

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

| 页面   | 填充内容                               |
| ---- | ---------------------------------- |
| 创建项目 | 项目名称/类别/赛道/简介/指导老师/日期（5 个预设名称随机选择） |
| 竞赛报名 | 团队名称/学校/学院/专业/队员信息（3 名测试队员）        |
| 承接命题 | 负责人/电话/团队人数/方案/优势                  |

### 环境变量检查清单

| 变量                 | 必需 | 说明                                                                  |
| ------------------ | -- | ------------------------------------------------------------------- |
| `DATABASE_URL`     | ✅  | MySQL 连接字符串                                                         |
| `SECRET_KEY`       | ✅  | Flask 密钥                                                            |
| `JWT_SECRET_KEY`   | ✅  | JWT 签名密钥                                                            |
| `ARK_API_KEY`      | ❌  | AI 对话（不配置则 AI 功能不可用）                                                |
| `ARK_BASE_URL`     | ❌  | 火山方舟 API 地址                                                         |
| `ARK_MODEL`        | ❌  | AI 模型名称                                                             |
| `GLM_API_KEY`      | ❌  | AI 智能体对话（通义千问 qwen-plus，不配置则智能体对话不可用）                               |
| `GLM_BASE_URL`     | ❌  | 通义千问 API 地址（默认 <https://dashscope.aliyuncs.com/compatible-mode/v1）> |
| `GLM_MODEL`        | ❌  | AI 智能体模型名称（默认 qwen-plus）                                            |
| `VOICE_REALTIME_*` | ❌  | 实时语音对话（不配置则回退文本模式）                                                  |
| `DOUBAO_ASR_*`     | ❌  | 语音识别（不配置则仅 Chrome 原生 ASR）                                           |
| `ARK_API_KEY`      | ❌  | AI 智能体向量检索 Embedding（不配置则 FAISS 向量检索不可用，需与 AI 对话共用）                 |

***

## 版本变更记录

> **变更记录撰写规范**：每条变更记录必须按以下分类组织，不可混写：
>
> | 分类         | 说明                        | 示例                                   |
> | ---------- | ------------------------- | ------------------------------------ |
> | **新增功能**   | 从无到有的全新功能/页面/组件/API/模型    | "新增 AI 材料问答功能"                       |
> | **功能修改**   | 已有功能的逻辑、交互、UI 调整（不改变功能本质） | "HuahuoAssistant 新增 agent 模式"        |
> | **Bug 修复** | 解决某个明确的错误行为，需说明复现条件       | "修复 PortalHome /ai-assistant 链接 404" |
> | **安全与稳定性** | 安全加固/性能优化/内存泄漏修复/异常处理     | "DOMPurify 安全渲染 Markdown"            |
> | **文档更新**   | README/注释/说明文档的内容同步       | "README 全量更新至 v4.0.0"                |
> | **已知问题**   | 当前版本已确认但未解决的缺陷/限制         | "FAISS 需要火山方舟 API 配置"                |
>
> **版本号规则**：`主版本.次版本.修订号` — 新增功能 → 次版本 +1；Bug 修复/文档更新 → 修订号 +1；重大架构变更 → 主版本 +1。
>
> **撰写原则**：
>
> - 每条记录必须**可追溯**，写明涉及的具体文件名或 API 端点
> - 不写"优化了部分功能""修复了一些 Bug"等模糊描述
> - 不重复记录同一改动（如已在"新增功能"中写了，不再在"功能修改"中重复）
> - 同一次提交中的所有改动归入同一个版本号，不分多条记录

### v4.1.1 - 2026-05-03（当前版本）

> AI 智能体前后端参数校验一致性修复 + Live2D 表情自动切换 + 权限矩阵/API 文档补全

#### 功能修改

- **Live2D 表情自动切换**：火花形象加载完成后，每 10 秒自动随机切换表情（AI 流式输出或朗读期间跳过，避免打断表情联动）；点击火花形象时也会随机切换一次表情（[HuahuoAssistant.vue](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/components/HuahuoAssistant.vue)）

#### Bug 修复

- **模拟答辩 question\_type 前后端不一致**：前端传 `challenge`，后端校验仅允许 `tough`，导致选择"挑战"类型时返回 400 错误。修复：前端 `AgentPanel.vue` 将 `label="challenge"` 改为 `label="tough"`（[AgentPanel.vue:158](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/views/ai-assistant/AgentPanel.vue#L158)）
- **智能反馈 feedback\_type 前后端不一致**：前端传 `encourage`/`question`，后端校验仅允许 `approve`/`reject`，导致选择"鼓励指导"/"提问引导"时返回 400 错误。修复：前端选项改为"建议通过"（`approve`）和"建议驳回"（`reject`）（[AgentPanel.vue:164-165](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/views/ai-assistant/AgentPanel.vue#L164)）
- **路演稿 duration 前后端不一致**：前端允许 8 分钟，后端校验仅允许 3/5，导致选择 8 分钟时返回 400 错误。修复：后端 `agent.py` 校验扩展为 `(3, 5, 8)`，`langchain_service.py` 新增 8 分钟对应约 2200 字目标（[agent.py:368](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/backend/routes/agent.py#L368)）
- **路演稿 style 前后端不一致**：前端传 `story`，后端校验仅允许 `formal`/`passionate`/`concise`，导致选择"故事"风格时返回 400 错误。修复：后端校验新增 `story`，`langchain_service.py` 新增故事叙述风格描述（[agent.py:369](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/backend/routes/agent.py#L369)）

#### 文档更新

- **AI 智能体权限矩阵补全**：从 5 行扩展为 12 行，新增项目创意生成/模拟答辩/批量审核/智能反馈/评审草稿/评分检查/智能引航 7 项能力的权限说明
- **AI 智能体 API 文档补全**：从 8 个端点扩展为 14 个，新增 navigate/project-idea/mock-defense/batch-review/smart-feedback/re-review-draft/score-check/capabilities 端点文档
- **AI 项目智能体特色功能描述更新**：从"5 大 AI 能力"更新为"12 大 AI 能力"

***

### v4.1.0 - 2026-05-03

> 集成通义千问 qwen-plus 大模型 + 统一对话路由 + 智能导航 + 深色主题适配 + AgentPanel 交互优化

#### 新增功能

- **通义千问 qwen-plus 大模型集成**：通过 LangChain ChatOpenAI 兼容接口接入通义千问 qwen-plus 模型（`GLM_API_KEY` / `GLM_BASE_URL` / `GLM_MODEL` 配置项），替代火山方舟 SDK 作为主要对话模型，支持多轮对话 / 意图识别 / 角色感知
- **统一对话路由**（`unified_chat`）：`ai_service.py` 新增统一对话入口，根据用户消息自动识别意图（导航 / 通用对话 / 智能体能力），分发到对应处理逻辑
- **智能导航功能**（`smart_navigate`）：`langchain_service.py` 新增智能导航能力，用户输入模糊指令（如"我想报名比赛""帮我看看项目"），AI 自动识别意图并返回路由跳转建议，前端自动执行页面跳转
- **意图检测**（`detect_intent`）：`langchain_service.py` 新增意图检测函数，支持导航意图 / 智能体意图 / 通用对话意图三类识别
- **角色感知对话**：AI 对话根据当前登录角色（学生/教师/评委/管理员）自动调整回复风格和可用能力介绍

#### 功能修改

- **ai\_service.py**：从火山方舟 SDK 直接调用改为 LangChain + ChatOpenAI 兼容接口，新增 `unified_chat` 统一对话入口、`_stream_unified_model` 统一流式输出函数
- **langchain\_service.py**：新增 `smart_navigate` 智能导航函数、`detect_intent` 意图检测函数，扩展 LangChain 编排能力
- **AgentPanel.vue**：项目选择从下拉框改为文本输入框 + 可选下拉选择组合，解决无项目数据时无法选择的问题；优化表单布局和交互流程
- **HuahuoAssistant.vue**：新增全局 CSS 样式（非 scoped），修复深色主题下表单标签、输入框、文本域的文字颜色不可见问题；输入框背景改为透明，去除黑框背景
- **agent.py**：新增 AI 智能体相关 API 端点
- **.env**：新增 `GLM_API_KEY` / `GLM_BASE_URL` / `GLM_MODEL` 配置项

#### Bug 修复

- **AI 对话不回复**：原火山方舟 SDK 连接不稳定，替换为 LangChain + qwen-plus 模型后对话稳定可用
- **项目选择框无法选择**：AgentPanel 中 el-select 下拉框在无数据时无法操作，改为 el-input 文本输入 + 可选 el-select 组合
- **深色背景下字体颜色看不清**：HuahuoAssistant 和 AgentPanel 中表单标签、输入框文字在深色背景下不可见，添加全局 CSS 覆盖样式
- **输入框黑框背景**：AI 分析工具输入框背景色与深色主题冲突，改为透明背景
- **AI 回复带 Markdown 特殊符号**：回答清洗逻辑增加去除 `#`、`**`、`*` 等 Markdown 格式符号的处理

#### 文档更新

- **README 更新**：AI 智能对话章节补充 qwen-plus 模型和统一对话路由说明；后端技术栈新增通义千问 qwen-plus；环境变量配置新增 GLM\_API\_KEY / GLM\_BASE\_URL / GLM\_MODEL；环境变量检查清单新增 3 项；常见问题更新 AI 对话失败排查步骤；版本变更记录新增 v4.1.0

***

### v4.0.0 - 2026-05-02

> AI 项目智能体全量上线：5 大 AI 能力、LangChain + FAISS + BM25 混合检索、文档解析服务、AgentPanel 组件

#### 新增功能

- **AI 材料问答**：上传项目/报名材料（.docx/.pptx/.pdf），自动解析文档内容并建立 FAISS 向量索引，支持基于 RAG 检索的自然语言问答
- **AI 商业计划书体检**：对商业计划书进行多维度结构化审查（执行摘要/市场分析/商业模式/团队/财务/风险），给出改进建议，不给出具体评分
- **AI 路演稿生成**：根据项目信息和材料内容，自动生成结构化路演演讲稿，支持自定义时长和风格
- **AI 评审辅助**（仅 teacher/judge/admin）：辅助评审人员快速了解项目全貌，生成亮点/风险/改进建议摘要，**严格不返回具体分数，仅提供定性评价参考**
- **智能竞赛推荐**（仅 student/admin）：根据项目类别/赛道/阶段智能匹配推荐竞赛，给出推荐理由和匹配度分析
- **AgentPanel.vue 组件**：AI 智能体前端面板组件，集成材料索引/问答/体检/路演/评审辅助/推荐 6 大功能入口
- **文档解析服务**（`document_parser.py`）：支持 .docx（python-docx）/ .pptx（python-pptx）/ .pdf（pypdf）三种格式文本提取 + RecursiveCharacterTextSplitter 分块
- **向量存储服务**（`vector_store.py`）：FAISS 向量索引 + BM25 稀疏检索混合方案，支持 Embedding 向量化 + 相似度搜索
- **LangChain 编排服务**（`langchain_service.py`）：基于 LangChain 的 RAG 问答 / BP 体检 / 路演稿 / 评审辅助 / 竞赛推荐 5 大能力编排
- **agent 路由蓝图**（`agent.py`）：8 个 API 端点（index-materials / material-qa / bp-check / roadshow / review-assist / competition-recommend / tasks / tasks/<id>）
- **AgentTask 模型**：AI 智能体任务记录（task\_type / status / input\_params / result / error\_message）
- **AgentMaterialIndex 模型**：AI 智能体材料索引记录（file\_type / chunk\_count / index\_status / index\_path）

#### 功能修改

- **HuahuoAssistant.vue**：新增 agent 模式，点击火花形象可切换到 AI 智能体面板
- **PortalHome.vue / judge.vue / teacher.vue**：AI 助手入口改为全局事件触发（`emit('open-ai-assistant')`），不再使用路由跳转
- **ai-assistant/index.vue**：新增 Tab 3（AI 智能体），集成 AgentPanel 组件，并添加备用提示（推荐使用全局浮动火花入口）

#### Bug 修复

- **修复 PortalHome / judge / teacher 中 /ai-assistant 链接 404**：移除直接路由跳转，改为全局事件触发打开 AI 助手面板

#### 安全与稳定性

- **评审辅助严格不返回具体分数**：后端 review-assist 端点在 Prompt 和后处理中双重保障，仅返回定性评价参考，避免影响评审公正性
- **DOMPurify 安全渲染 Markdown**：前端 Markdown 渲染引入 DOMPurify 净化 HTML 输出，防止 XSS 攻击
- **事件监听 onBeforeUnmount 清理**：AgentPanel 和相关组件在卸载时完整清理全局事件监听器，避免内存泄漏

#### 文档更新

- **README 全量更新**：技术栈新增 9 个后端依赖 + 1 个前端依赖；特色功能新增 AI 项目智能体小节；项目结构新增 8 个文件 + 1 个目录；API 文档新增 AI 智能体章节；数据库模型新增 2 个模型；路由配置新增备用路由；权限矩阵新增 AI 智能体权限；版本号更新为 v4.0.0

#### 已知问题

- **FAISS Embedding 需要通义千问 API 配置**：向量索引优先使用通义千问 Embedding API（`GLM_API_KEY` + `GLM_BASE_URL`），也可使用火山方舟 API（`ARK_API_KEY` + `ARK_BASE_URL`），均未配置时向量检索降级为 BM25/关键词检索
- **BP 体检 / 路演稿等 LLM 密集型接口偶发 502**：Vite 代理超时 120 秒，LLM 调用耗时较长时可能触发，重试通常可成功

#### Chrome DevTools MCP 调试验证（2026-05-02）

| 验收项                                       | 结果 | 说明                                                |
| ----------------------------------------- | -- | ------------------------------------------------- |
| student1 登录                               | ✅  | API 登录成功，JWT Token 正确                             |
| Portal AI 入口打开火花 Agent 模式                 | ✅  | `open-huahuo-agent` 全局事件触发，面板自动打开并切换到 agent 模式    |
| chat / analysis / agent 三模式切换             | ✅  | 三种模式均可正常切换，无状态污染                                  |
| 全局事件 detail 参数自动选中能力                      | ✅  | `capability: 'competition_recommend'` → 🎯 智能竞赛推荐 |
| 材料索引 `/api/agent/index-materials`         | ✅  | 200，索引成功                                          |
| 材料问答 `/api/agent/material-qa`             | ✅  | 200，返回问答结果                                        |
| 商业计划书体检 `/api/agent/bp-check`             | ✅  | 200，返回体检报告，不返回具体评分                                |
| 路演稿生成 `/api/agent/roadshow`               | ✅  | 200，返回路演稿                                         |
| 智能竞赛推荐 `/api/agent/competition-recommend` | ✅  | 200，返回推荐结果                                        |
| judge1 评审辅助 `/api/agent/review-assist`    | ✅  | 200，严格不返回具体分数                                     |
| student1 评审辅助被拦截                          | ✅  | 403 "权限不足，需要 teacher 及以上角色"                       |
| Console 无新增关键错误                           | ✅  | 仅 403 为学生角色访问管理看板（预期行为）                           |
| Network /api/agent/\* 无 404/500           | ✅  | 偶发 502 为 LLM 超时，重试可成功                             |
| 返回格式 {code, message, data}                | ✅  | 所有 API 均符合统一响应格式                                  |
| /ai-assistant 备用页面                        | ✅  | 三个 Tab 可切换，顶部有备用提示                                |
| student 角色权限                              | ✅  | 仅显示 4 个能力卡片（无评审辅助）                                |
| 复制/朗读/表情联动                                | ⚠️ | 需用户在浏览器中手动验证（MCP 无法模拟剪贴板和音频输出）                    |

***

### v4.0.1 - 2026-05-02（引导系统全面修订）

> 四角色引导系统 Bug 修复 + AI 智能体能力接入 + routePath 补全

#### Bug 修复

- **学生引导第 2 步路由指向空白页**：`routePath: '/'` 改为 `routePath: '/portal'`，导航到 `/` 只渲染空白的 MainLayout 不显示首页内容（[guide.js](file:///E:/LEAR-CODE-NEW/软件工程/my-keshe/innovation-competition-platform/frontend/src/stores/guide.js) 第 2 步）
- **所有角色引导欢迎标题版本号过时**：学生写 v3.0、教师/评委/管理员写 v2.0，全部移除版本号统一为「欢迎使用创新创业平台」

#### 功能修改

- **四角色引导全部接入 AI 智能体能力**：学生新增"AI 项目智能体"步骤（介绍 5 大能力 + 快捷入口提示）；教师新增 AI 智能体步骤（评审辅助/BP 体检/材料问答）；评委新增 AI 智能体步骤（带"评审辅助仅返回定性分析"提示）；管理员新增 AI 智能体步骤（全部 5 大能力）
- **教师第 4 步「项目审核」补充** **`routePath: '/project-review'`**：引导不再停在空中心步骤，自动导航到审核页
- **评委第 5 步「评审记录」补充** **`routePath: '/review-history'`**：引导自动跳转到评审记录页
- **管理员第 5/7 步补充** **`routePath`**：报名管理和评审管理步骤补充导航路径
- **引导步骤总数重新统计**：学生 12 步 / 教师 9 步 / 评委 8 步 / 管理员 11 步

#### 文档更新

- **README 变更记录撰写规范**：在版本变更记录板块顶部新增 6 分类标准 + 版本号规则 + 撰写原则
- 全局引导系统描述从"学生 14 步"更新为实际步数
- `.gitignore` 新增 `frontend/dist/` 和 `backend/vector_stores/` 忽略规则
- `start.bat` 每次启动强制 `npm install` 确保依赖最新

***

### v3.0.0 - 2026-05-01

> AI流式输出优化、项目创建修复、引导内容更新、产业命题承接、动态数据、头部卡片动画

#### 新增功能

- **竞赛报名表单快速生成**：队伍信息一键填充 + 队员信息一键生成（3 名测试队员完整信息）
- **产业命题承接功能**：新增 `AcceptTopic.vue` 承接命题填写页面（负责人/联系电话/团队人数/项目方案等），确认后跳转创建项目页面
- **证书与获奖记录查看详情弹窗**：证书卡片和获奖记录卡片添加"查看详情"按钮，`el-dialog` 显示高清图片
- **首页数据流粒子动画增强 + 烟花效果**：8 种颜色粒子 + 径向渐变发光 + 烟花爆炸效果
- **首页数据流动画改为科幻数字雨风格**：《黑客帝国》风格数字雨（十六进制字符 + 编程符号 + 头部高亮 + 拖尾残影 + 水平扫描线）
- **数字雨全屏铺满 + 速度加快**：单个全局画布 `global-rain-canvas`，下落速度提升到 0.8-2.3px/帧
- **创建项目页面一键快速填充**：5 个预设名称随机选择 + 类别/赛道/阶段/简介自动生成
- **页面头部卡片渐变色 + 动画**：竞赛广场深蓝渐变 + 双光球呼吸、训练营紫罗兰渐变 + 光球漂浮、课程翠绿渐变 + 光球浮动
- **系统数值动态化**：首页 Banner 统计改为调用 `getDashboardStats()` API 获取实时数据

#### 功能修改

- **竞赛详情页海报宽度占满 + 去掉中央文字**：`aspect-ratio: 16/9` 占满全宽，移除 `max-height`，去掉海报中央叠加文字
- **导航栏与海报间距移除**：移除 `padding-top: 64px`，海报紧贴导航栏底部
- **首页推荐竞赛改用海报封面**：卡片使用 `<img>` 标签显示对应海报，竞赛名移到下方信息区域
- **我的赛事卡片使用海报图**：导入本地竞赛图片映射，卡片优先使用本地图片
- **训练营/课程详情页海报修复**：移除 `padding-top: 64px`，`object-fit: contain` + `aspect-ratio: 16/9`
- **引导窗口内容适配更新**：更新为 v3.0 功能路径，删除已移除功能，补充新增功能
- **产业命题承接流程完善**：点击「承接命题」跳转至填写页面（而非直接确认弹窗）
- **项目列表动态更新**：`my-projects.vue` 添加 `onActivated` 钩子，返回时自动刷新

#### Bug 修复

- **详情页海报被导航栏遮盖**：竞赛/训练营/课程详情页统一添加 `padding-top: 64px`（后续版本又移除）
- **竞赛详情页时间安排和奖项设置缺失**：API 返回空数组时 fallback 未正确触发，改为强制调用生成函数
- **竞赛海报裁切**：`object-fit: cover` → `object-fit: contain`，移除 `overflow: hidden`
- **Live2D 引导后关闭加载不出来**：移除对 `window.initWidget` 的破坏性删除，改为隐藏 waifu 元素
- **Live2D 全屏拖拽修复**：`startModelDrag` 添加 `e.stopPropagation()`，手柄定位改用 `transform`
- **Live2D 拖拽按钮点击对话后不消失**：`v-if` 改为常驻 + `opacity: 0` 隐藏
- **Live2D 拖拽按钮跟随形象移动**：`applyModelPosition` 中同步计算按钮位置
- **Live2D 全屏拖拽坐标系修复**：`bottom` 定位改为 `top` 定位，拖拽方向与鼠标一致
- **侧边栏「我的项目」选中状态 BUG**：`/create-project` 路由单独精确匹配，不再误高亮「我的项目」
- **AI 对话流式输出稳定性**：添加重试机制（最大 2 次）+ 3 分钟超时 + 缓冲区处理 + 错误隔离
- **项目创建失败 500 错误**：`teacher_id`/`competition_id` 字符串转整数，空字符串转 null
- **导航栏 AI 助手入口删除**：从 topNavConfig 和 menuGroups 中移除 `/ai-assistant` 入口

#### 安全与稳定性

- **AI 流式输出重试 + 超时**：最大重试 2 次，递增间隔 1s/2s，单 chunk 超时 3 分钟
- **项目创建数据预处理**：提交前类型转换和空值处理，详细错误提示

#### 文档更新

- 引导步骤更新为 v3.0 功能路径

***

### v2.10.0 - 2026-05-01

> Live2D拖拽按钮常驻、侧边栏选中状态修复、创建项目快速填充、产业命题承接功能

#### 新增功能

- **创建项目一键快速填充**：5 个预设名称随机选择 + 类别/赛道/阶段/简介自动生成
- **产业命题承接功能**：`AcceptTopic.vue` 承接命题填写页面（负责人/联系电话/团队人数/项目方案等），确认后跳转创建项目

#### Bug 修复

- **Live2D 拖拽按钮点击对话后不消失**：`v-if` 改为常驻 + `opacity: 0` 隐藏
- **侧边栏「我的项目」选中状态 BUG**：`/create-project` 路由单独精确匹配

#### 安全与稳定性

- **项目创建数据预处理**：`teacher_id`/`competition_id` 字符串转整数，空字符串转 null，详细错误提示

***

### v2.9.0 - 2026-05-01

> 训练营/课程海报修复、数字雨全屏铺满、速度加快

#### 功能修改

- **数字雨全屏铺满**：改为单个全局画布 `global-rain-canvas`，动态高度检测
- **数字雨速度加快**：下落速度从 `0.3-1.1px/帧` 提升到 `0.8-2.3px/帧`

#### Bug 修复

- **训练营/课程详情页海报裁切**：`object-fit: cover` → `contain`，移除 `padding-top: 64px`

***

### v2.8.0 - 2026-05-01

> 首页数据流动画改为科幻数字雨风格

#### 功能修改

- **数字雨风格重设计**：《黑客帝国》风格数字雨（十六进制字符 + 编程符号 + 头部高亮 + 拖尾残影 + 水平扫描线），替代原粒子动画

***

### v2.7.0 - 2026-05-01

> 海报宽度占满修复、Live2D拖拽按钮跟随、导航栏间距移除、推荐竞赛海报封面

#### 功能修改

- **竞赛详情页海报宽度占满**：`aspect-ratio: 16/9` 占满全宽，去掉海报中央叠加文字
- **推荐竞赛改用海报封面**：卡片使用 `<img>` 标签显示对应海报
- **导航栏与海报间距移除**：移除 `padding-top: 64px`

#### Bug 修复

- **Live2D 拖拽按钮跟随形象移动**：`applyModelPosition` 中同步计算按钮位置

***

### v2.6.0 - 2026-05-01

> 竞赛详情数据强制生成、海报裁切修复、Live2D全屏拖拽优化、我的赛事海报图、证书查看详情弹窗、首页烟花数据流

#### 新增功能

- **证书与获奖记录查看详情弹窗**：`el-dialog` 显示高清图片
- **首页数据流粒子动画增强 + 烟花效果**：8 种颜色粒子 + 径向渐变发光 + 烟花爆炸效果

#### Bug 修复

- **竞赛详情页时间安排和奖项设置缺失**：API 返回空数组时强制调用生成函数
- **竞赛海报裁切**：`object-fit: cover` → `contain`，移除 `overflow: hidden`
- **Live2D 全屏拖拽坐标系修复**：`bottom` 定位改为 `top` 定位
- **我的赛事卡片图片**：导入本地竞赛图片映射

### v2.4.0 - 2026-05-01

> Live2D全屏拖拽、竞赛/训练营/课程详情页完善、导航栏侧边栏补全、首页背景动画补充

#### 新增功能

- **Live2D 形象全屏可拖拽**：拖拽手柄 + 全屏拖拽 + 位置持久化（localStorage）+ 边界约束 + 触摸支持
- **训练营详情页开发**：`TrainingCampDetail.vue` 独立页面，4 大训练营完整数据（课程大纲/讲师团队/学习安排/结业奖励）
- **在线课程详情页开发**：`CourseDetail.vue` 独立页面，5 门课程完整数据（课程简介/章节目录/学习计划/学习成果）
- **首页下板块背景动画**：浮动圆形装饰 + 底部波浪动画 + 点阵动画（CSS 动画，GPU 加速）

#### 功能修改

- **竞赛详情页完善**：时间安排从 2 项扩展为 6 阶段、奖项从 1 项扩展为 6 级、封面海报使用本地图片
- **导航栏和侧边栏补全**：新增产业命题/AI助手/证书成果等入口，活跃状态检测，响应式适配

#### Bug 修复

- **竞赛详情页封面海报缺失**：使用本地竞赛海报图片替代渐变色占位

***

### v2.3.0 - 2026-05-01

> 图片资源替换优化、导航与侧边栏入口补全、页面背景美化与动效增强、Live2D表情系统修复、引导窗口优化

#### 新增功能

- **首页粒子动画**：20 个 CSS 粒子动画效果，Cyan 主色调适配，IntersectionObserver 懒加载

#### 功能修改

- **图片资源替换与优化**：竞赛/训练营/课程卡片封面图全部替换为本地真实图片，图片加载失败时渐变色占位图
- **导航与侧边栏入口优化**：补全核心功能模块导航入口，合理排序，响应式适配（桌面/平板/移动端 + 汉堡菜单）
- **引导窗口优化**：宽度调整为 820px，左侧步骤指示器 + 右侧内容区域双栏布局

#### Bug 修复

- **Live2D 表情按钮点击无响应**：重新实现表情控制逻辑
- **月卡/水印表情无法与其他表情共存**：设计表情叠加系统（`__expressionOverlayRules`），支持多修饰效果并行
- **CSP 阻止 Live2D SDK 加载**：`vite.config.js` 添加 Content-Security-Policy header 允许 `unsafe-eval`

#### 安全与稳定性

- **CSP 配置修复**：允许 Live2D SDK 执行 eval，加载时长 ≤ 3 秒

***

### v2.2.0 - 2026-05-01

> AI 助手与 Live2D 形象整合为全局浮动组件，CSP 修复，四角色引导更新

#### 新增功能

- **HuahuoAssistant.vue 全局浮动组件**：整合 Live2D 看板娘 + AI 对话面板 + 语音交互 + AI 分析工具，任何页面均可使用

#### 功能修改

- **AI 助手不再是独立页面**：移除 `/ai-assistant` 路由和导航入口，改为全局浮动组件
- **四角色引导更新**：AI 助手相关步骤从"页面导航"改为"点击左下角火花"，合并对话/语音/Live2D 为一个步骤

#### Bug 修复

- **CSP 阻止 Live2D 加载**：Vite 开发服务器 CSP 策略阻止 `eval()` 执行，添加 Content-Security-Policy header
- **AI 对话和 Live2D 功能重复**：原来 AI 对话独立页面 + Live2D 独立浮动组件 + VoiceChat 又是另一个组件，三者功能重叠，整合为 `HuahuoAssistant.vue`

***

### v2.1.0 - 2026-05-01

> 修复竞赛详情数据缺失、训练营/课程按钮无响应、Live2D 加载优化、引导系统全面升级、四角色页面全面补全

#### 新增功能

- **竞赛详情页完整数据**：时间安排 5 项 + 奖项 5 级 + 智能内容生成
- **训练营学习系统**：4 大主题训练营完整实现（课程大纲/讲师团队/播放按钮）
- **在线课程详情系统**：5 门课程完整实现（课程简介/章节目录/免费/会员标签）
- **使用引导系统 v2**：学生 14 步引导 + CSS 选择器高亮 + 路由跳转 + 四角色同步更新
- **一键启动脚本**：`start.bat` 双击启动前后端服务
- **四角色页面全面补全**：教师仪表盘/指导项目、评委仪表盘/待评审、管理员用户/竞赛/项目管理

#### Bug 修复

- **竞赛详情页信息缺失**：fallback 数据过于简略，补充为完整 5 阶段时间线和 5 级奖项体系
- **训练营"开始学习"按钮无响应**：缺少 `@click` 事件绑定
- **课程"查看课程"按钮无响应**：同上
- **Live2D 形象不显示**：改为分步加载 + 轮询检测 + canvas 渲染检测 + 错误重试（最多 3 次）
- **教师/评委/管理员大量页面空壳**：6 个页面从"功能开发中"补全为完整交互界面
- **评委"开始评审"按钮无响应**：`pending.vue` 缺少 `@click` 绑定

***

### v2.0.0 - 2026-04-30

> 从 my\_huahuo 项目集成 Live2D 形象、语音交互、AI 大模型等核心功能

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
- `requirements.txt`：新增 volcengine-python-sdk\[ark]、opencc-python-reimplemented、langchain、langchain-core、websockets、requests、cryptography
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
- AI 健康检查 `/api/ai/health`：通过（chat\_configured: true, voice\_realtime\_configured: true）
- 登录功能（admin / admin123）：通过（JWT Token 正确生成）
- Dashboard 数据：通过（8 用户 / 6 项目 / 10 竞赛 / 4 评审）
- AI 流式对话：通过（SSE 流式响应正常）
- Live2D 资源访问：通过（waifu-tips.js / waifu.css / 模型文件均可访问）
- 前端构建：通过（0 错误，2315 模块编译成功）

***

### v1.0.0 - 初始版本

> 基础创新创业竞赛服务平台，AI 功能为 Mock 实现

- 竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分
- 四种角色（学生 / 指导老师 / 评委 / 管理员）
- 竞赛广场、项目工作室、训练营、在线课程、产业命题
- AI 分析工具（Mock 模板实现）
- 全局引导系统
- 双模式布局（平台页无侧边栏 / 工作台有侧边栏）

***

## 许可证

MIT License
