# 火花智创 SparkAI Innovate

> 🔥 高校创新创业竞赛智能服务平台 / University Innovation and Entrepreneurship Competition AI Service Platform
>
> GitHub: https://github.com/DearJIAN/sparkai-innovate

一个面向高校的**创新创业竞赛全流程服务平台**，覆盖竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分、AI 辅助的完整流程。平台采用**前后端分离架构**，支持学生、指导老师、评委、管理员四种角色，提供竞赛广场、项目工作室、训练营、在线课程、产业命题、**AI 材料评估**、**在线测评**等多元化功能。

平台集成了 **Live2D 虚拟形象「火花」**、**语音交互**、**AI 智能对话**、**AI 项目智能体**、**AI 材料评估**等特色功能，为用户提供沉浸式智能辅助体验。其中 AI 项目智能体提供智能引航、材料问答、商业计划书体检、路演稿生成、评审辅助、竞赛推荐、项目创意生成、模拟答辩、批量审核、智能反馈、评审草稿、评分检查 12 大 AI 能力，基于 LangChain + FAISS + BM25 混合检索技术实现。AI 材料评估支持路演 PPT 和项目报告的 PDF 智能上传评估，自动生成 8 维度评分报告并支持 PDF 报告下载。

**品牌视觉**：「火花智创 SparkAI」品牌 Logo 采用动态渐变色彩（红-橙-黄-粉-紫-蓝六色流动渐变）+ 底部粒子浮动效果 + 奖杯呼吸光晕，悬停时加速闪烁，呈现烟花般的视觉氛围。

---

## 目录

- [项目环境依赖](#项目环境依赖)
- [技术栈](#技术栈)
- [特色功能](#特色功能)
  - [Live2D 虚拟形象「火花」](#live2d-虚拟形象火花)
  - [AI 智能对话](#ai-智能对话)
  - [语音交互](#语音交互)
  - [AI 分析工具](#ai-分析工具)
  - [AI 项目智能体](#ai-项目智能体)
  - [火山实时语音对话](#火山实时语音对话)
  - [全局引导系统](#全局引导系统)
  - [双模式布局](#双模式布局)
  - [数字雨背景动画](#数字雨背景动画)
  - [AI 材料评估](#ai-材料评估)
- [项目结构](#项目结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [后端配置详情](#后端配置详情)
- [演示账号](#演示账号)
- [API 接口文档](#api-接口文档)
  - [统一响应格式](#统一响应格式)
  - [认证接口 /api/auth](#认证接口-apiauth)
  - [用户接口 /api/users](#用户接口-apiusers)
  - [竞赛接口](#竞赛接口)
  - [报名接口](#报名接口)
  - [项目接口 /api/projects](#项目接口-apiprojects)
  - [AI 分析工具 /api/ai](#ai-分析工具-apiai)
  - [AI 对话 /api/ai](#ai-对话-apiai)
  - [语音交互 /api/ai](#语音交互-apiai)
  - [Live2D / 健康 /api/ai](#live2d--健康-apiai)
  - [看板接口 /api/dashboard](#看板接口-apidashboard)
  - [系统接口](#系统接口)
  - [其他接口](#其他接口)
  - [AI 智能体 /api/agent](#ai-智能体-apiagent)
  - [AI 材料评估 /api/material-evaluation](#ai-材料评估-apimaterial-evaluation)
- [路由配置](#路由配置)
- [数据库模型](#数据库模型)
- [用户角色与权限](#用户角色与权限)
- [设计系统](#设计系统)
- [开发规范](#开发规范)
- [常见问题](#常见问题)
- [当前开发状态](#当前开发状态)
- [调试指南](#调试指南)
- [版本变更记录](#版本变更记录)

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

> **📚 详细技术文档**：关于 Live2D 表情系统与语音交互的完整实现机制、叠加效果共存逻辑、情绪关键词触发机制等详细说明，请参阅 [Live2D-表情与语音交互系统实现文档.md](./Live2D-表情与语音交互系统实现文档.md)。

- 全局浮动 Live2D 看板娘，支持全屏拖拽（通过 `HuahuoAssistant.vue` 组件 + `MainLayout.vue` 集成）
- 拖拽位置持久化到 localStorage，刷新页面后自动恢复
- 10 种基础表情（黑脸 / 脸红爱心 / 生气 / 晕 / ＞＜ / 0.0 / 星星眼 / 流泪 / 捧心 / 要饭）+ 2 种叠加效果（月卡 / 水印）
- AI 对话时基于文本关键词自动切换表情（开心 / 害羞 / 生气 / 难过 / 晕 / 惊讶），不在开始/结束时强制设置表情
- 每 10 秒自动随机切换表情（AI 流式输出或朗读期间跳过），点击形象时也会随机切换
- 可拖拽、可隐藏、可切换表情
- 表情 / 情绪联动逻辑抽取为共享 composable（`useLive2d.js`）
- 组件卸载时完整清理（CSS link / DOM 元素 / 全局变量），避免内存泄漏
- Live2D 初始化带并发锁，账号/角色切换时通过 `MainLayout.vue` 的用户维度 key 强制重挂载，降低全局状态残留风险
- AI Markdown 输出通过 DOMPurify 净化后再渲染，降低 `v-html` 带来的 XSS 风险

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
- **亮色清爽主题**：AI 助手窗口采用纯白背景 `#ffffff` + 蓝色系强调色 `#3b82f6`，消息气泡区分用户（浅蓝）和助手（浅灰），整体视觉清爽科技
- **右下角拖拽缩放**：缩放手柄位于窗口右下角，鼠标向右下拖动时窗口自然变大，尺寸范围 320-800px 宽 / 400-900px 高，持久化到 localStorage
- **标题栏拖拽分离**：仅标题文字区域可拖拽移动，按钮区域独立不触发拖拽
- **移动端自适应**：屏幕宽度 ≤768px 时自动缩小面板尺寸并固定到底部

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

> **📚 详细技术文档**：关于 AI 项目智能体的完整技术架构、实现原理、LangChain 使用方式、RAG 检索流程等详细说明，请参阅 [AI-Agent功能分析报告.md](./AI-Agent功能分析报告.md)。该文档包含：
> - 项目真实架构图与 Agent 层架构图
> - LangChain 在本项目中的实际作用与使用方式
> - RAG 检索流程详解（FAISS + BM25 混合检索）
> - 12 大 AI 能力的实现原理与代码示例
> - 固定功能型 AI Agent 的设计思路

### 火山实时语音对话

- 通过 WebSocket 连接火山实时语音对话服务（`volc_realtime_bridge.py`）
- 自定义二进制协议编解码（`volc_realtime_protocol.py`）
- 支持 Gzip 压缩的 JSON 序列化
- 文本输入模式，流式回复输出
- 可配置发音人、bot 名称、系统角色、说话风格

### 全局引导系统

- 首次登录引导（`GuideSystem.vue`）
- 高亮指引 + 拖拽弹窗 + 路由自动跳转（`routePath` 配置）
- 引导弹窗支持键盘 Esc 跳过、Enter 下一步/完成，弹窗定位会钳制在视口内，进度节点可横向/纵向滚动查看
- 引导状态持久化（Pinia `guide.js`）
- 四角色独立引导步骤（学生 12 步 / 教师 9 步 / 评委 8 步 / 管理员 11 步）
- 各角色引导均包含 AI 智能体能力介绍（AgentPanel 入口 + 各角色可用能力说明）

### 双模式布局

- 平台页面（首页 / 竞赛广场 / 训练营等）：无侧边栏，顶部导航，优先通过路由 `meta.platformPage` 判定平台页，避免布局清单和路由清单重复维护
- 工作台页面（项目 / 评审 / 管理等）：左侧边栏 + 顶部导航
- 侧边栏可折叠，响应式适配

### 数字雨背景动画

- 全局 Canvas 数字雨效果（《黑客帝国》风格）
- 十六进制字符 + 编程符号，头部高亮 + 拖尾残影
- 水平扫描线增强科幻感
- 全屏铺满，动态高度检测
- IntersectionObserver 懒加载触发

### AI 材料评估

- 支持路演 PPT 和项目报告两种类型的 PDF 智能评估
- 上传 PDF 后自动进入 AI 分析进度页（含分阶段进度动画）
- 评分报告页采用飞入动画，各模块从上下左右四个方向飞入组合
- 8 维度评分体系（PPT：内容完整性/表达逻辑/视觉设计/创新性/可行性/市场价值/团队表现/答辩准备；报告：内容深度/数据支撑/论证逻辑/创新性/可行性/市场分析/团队能力/写作规范）
- 综合评分 + 等级评定 + 分项维度雷达图
- PDF 报告下载（reportlab 生成，含深蓝封面 + 评分维度表 + 核心评价卡片 + 改进建议，支持中文 CID 字体回退）
- 仅允许上传 PDF 文件（扩展名 + MIME type 双重校验，最大 50MB）

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
│   │
│   ├── models/                       # 数据模型（15 个）
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
│   │   ├── agent_material_index.py  # AI 智能体材料索引（agent_material_indices 表）
│   │   └── material_evaluation.py   # AI 材料评估（material_evaluations 表）
│   │
│   ├── routes/                       # API 路由（15 个蓝图）
│   │   ├── __init__.py               # 蓝图包初始化
│   │   ├── auth.py                   # /api/auth    认证接口（注册/登录/当前用户/登出）
│   │   ├── user.py                   # /api/users   用户接口（列表/详情/创建/更新/删除/状态切换）
│   │   ├── project.py                # /api/projects 项目接口（CRUD/提交）
│   │   ├── member.py                 # /api         成员接口
│   │   ├── file.py                   # /api         文件接口
│   │   ├── material.py               # /api/materials 材料接口
│   │   ├── team.py                   # /api/teams   团队接口
│   │   ├── task.py                   # /api         任务接口
│   │   ├── review.py                 # /api         评审接口
│   │   ├── dashboard.py              # /api/dashboard 看板接口（统计/最近数据/公开统计）
│   │   ├── ai.py                     # /api/ai      AI 接口（聊天/语音/ASR/TTS/分析/表情/健康）
│   │   ├── competition.py            # /api         竞赛接口（公开+管理+赛道）
│   │   ├── registration.py           # /api         报名接口（学生+管理员）
│   │   ├── agent.py                  # /api/agent   AI 智能体接口（材料索引/问答/体检/路演/评审辅助/推荐/任务）
│   │   └── material_evaluation.py    # /api/material-evaluation  AI 材料评估接口（上传/进度/报告/PDF 下载）
│   │
│   ├── services/                     # 业务逻辑
│   │   ├── __init__.py
│   │   ├── ai_service.py             # AI 核心（通义千问 qwen-plus + LangChain + 统一对话路由 + 智能导航 + 意图识别 + 会话管理 + 流式输出 + 回答清洗）
│   │   ├── ai_prompt_service.py      # AI Prompt 服务（手工拼接 Prompt + 调用 LLM）
│   │   ├── document_parser.py        # 文档解析服务（.docx / .pptx / .pdf 文本提取 + 分块）
│   │   ├── vector_store.py           # 向量存储服务（FAISS 索引 + BM25 混合检索 + Embedding）
│   │   ├── tts_service.py            # TTS 语音合成（火山 TTS HTTP API + 文件缓存 + 缓存统计/清理）
│   │   ├── volc_realtime_bridge.py   # 火山实时语音对话桥（WebSocket + 流式回复 + 回答清洗）
│   │   ├── volc_realtime_protocol.py # 火山实时语音二进制协议（编解码 + Gzip）
│   │   ├── material_evaluation_service.py # AI 材料评估评分服务（PPT/报告各 8 维度评分体系 + 等级评定）
│   │   └── material_report_pdf.py     # AI 材料评估 PDF 报告生成（reportlab 封面+维度表+评价卡片+中文 CID 字体回退）
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
│   ├── index.html                    # HTML 入口（标题：火花智创 SparkAI Innovate）
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
│       ├── api/                      # API 接口封装（13 个模块）
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
│       │   ├── agent.js              # AI 智能体 API（材料索引/问答/体检/路演/评审辅助/推荐/任务）
│       │   └── materialEvaluation.js # AI 材料评估 API（上传/进度/报告/PDF 下载）
│       │
│       ├── components/               # 公共组件
│       │   ├── SparkLogo.vue         # 品牌 Logo 组件（彩色渐变文字+粒子浮动+奖杯光晕，烟花视觉效果）
│       │   ├── GuideSystem.vue       # 全局引导系统（首次登录引导/高亮/拖拽弹窗/路由跳转）
│       │   ├── HuahuoAssistant.vue   # Live2D 虚拟形象「火花」（全屏拖拽/AI对话/语音/关键字表情联动/完整清理/亮色主题/右下角缩放）
│       │   ├── VoiceChat.vue         # 语音交互面板（流式对话/语音识别/TTS/可拖拽/深色毛玻璃）
│       │   ├── TestButton.vue        # 测试按钮组件
│       │   ├── TestButtonDemo.vue    # 测试按钮演示
│       │   └── HelloWorld.vue        # 示例组件
│       │
│       ├── data/                      # 数据配置文件
│       │   ├── assessmentVisualThemes.js  # 在线测评视觉主题（8 套 SVG 装饰 + 渐变色 + 图标）
│       │   └── assessmentQuestionnaires.js # 在线测评问卷题库
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
│       │       ├── courses/          # 在线课程图片（5 张）
│       │       └── Off-campus_competitions/ # 校外竞赛官方海报（中国国际大学生创新大赛 / 挑战杯 / 三创赛）
│       │
│       └── views/                    # 页面视图（43 个 Vue 文件）
│           ├── ai-assistant/         # AI 助手（双标签页：分析工具 + 对话）
│           │   ├── index.vue
│           │   └── AgentPanel.vue    # AI 智能体面板（12 大 AI 能力：智能引航/材料问答/体检/路演/评审辅助/竞赛推荐/项目创意/模拟答辩/批量审核/智能反馈/评审草稿/评分检查/亮色主题适配）
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
│           ├── portal/               # 平台页面（19 个，无侧边栏）
│           │   ├── PortalHome.vue    # 平台首页（全局数字雨背景 + 功能入口 + 推荐竞赛 + 动态统计）
│           │   ├── CompetitionCenter.vue # 竞赛报名中心（校外/校内双入口分流页 + 蓝紫/青色双卡片）
│           │   ├── ExternalCompetitions.vue # 校外竞赛（国家级赛事聚合 + 分类筛选 + 官方外链 + 官方海报封面）
│           │   ├── ExternalCompetitionDetail.vue # 校外竞赛详情（真实海报 Hero + 8 大板块 + 右侧吸附卡）
│           │   ├── CompetitionSquare.vue # 竞赛广场/校内竞赛（深蓝渐变 Banner + 双光球呼吸动画 + 海报封面卡片）
│           │   ├── CompetitionDetail.vue # 校内竞赛详情（海报占满宽度 + 完整时间/奖项/材料 + 智能内容生成）
│           │   ├── CompetitionRegister.vue # 竞赛报名（快速填充 + 团队信息 + 队员管理）
│           │   ├── MyRegistrations.vue # 我的赛事（海报封面卡片 + 状态跟踪）
│           │   ├── TrainingCamps.vue # 训练营（紫罗兰渐变 Banner + 光球漂浮动画 + 海报封面）
│           │   ├── TrainingCampDetail.vue # 训练营详情（海报占满宽度 + 课程大纲 + 讲师团队）
│           │   ├── Courses.vue       # 在线课程（翠绿渐变 Banner + 光球浮动动画 + 海报封面）
│           │   ├── CourseDetail.vue   # 课程详情（海报占满宽度 + 章节目录 + 学习计划）
│           │   ├── IndustryTopics.vue # 产业命题（承接命题跳转填写页）
│           │   ├── AcceptTopic.vue   # 承接命题（填写承接信息 + 快速填充 + 跳转创建项目）
│           │   ├── Certificates.vue  # 证书成果（查看详情弹窗 + 证书图片）
│           │   ├── OnlineAssessment.vue   # 在线测评（8 套主题 SVG 卡片 + 10 题问卷 + 40 分制评分 + 维度分析）
│           │   ├── AssessmentResult.vue   # 测评结果（40 分制雷达图 + 综合评级 + 分项解读）
│           │   ├── AIMaterialEvaluation.vue           # AI 材料评估中心（任务面板 + 状态筛选 + 空状态引导）
│           │   ├── AIMaterialEvaluationUpload.vue     # AI 材料评估上传页（文件拖拽/选择 + 类型选择 + 名称编辑）
│           │   ├── AIMaterialEvaluationProgress.vue   # AI 材料评估进度页（分阶段进度动画 + 实时状态轮询）
│           │   └── AIMaterialEvaluationReport.vue     # AI 材料评估报告页（飞入动画 + 8 维度评分 + 雷达图 + PDF 下载）
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

| 接口                            | 方法   | 认证  | 权限       | 说明         |
| ----------------------------- | ---- | --- | -------- | ---------- |
| `/api/users/`                 | GET  | JWT | admin    | 获取所有用户列表   |
| `/api/users/`                 | POST | JWT | admin    | 创建用户       |
| `/api/users/<id>`             | GET  | JWT | 本人或admin | 获取用户详情     |
| `/api/users/<id>`             | PUT  | JWT | admin    | 更新用户信息     |
| `/api/users/<id>`             | DELETE | JWT | admin    | 删除用户       |
| `/api/users/<id>/toggle-status` | POST | JWT | admin    | 切换用户启用/禁用状态 |

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

| 接口                            | 方法  | 权限      | 说明                                            |
| ----------------------------- | --- | ------- | --------------------------------------------- |
| `/api/dashboard/stats`        | GET | admin   | 管理员统计数据（用户/项目/文件/评审/竞赛/AI 使用，含角色分布/阶段分布/赛道分布） |
| `/api/dashboard/recent`       | GET | admin   | 最近数据（最近 5 个项目/文件/评审）                          |
| `/api/dashboard/public-stats` | GET | JWT     | 公开统计数据（竞赛数/用户数/项目数/报名数/赛道数），不限角色              |

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

### AI 材料评估 `/api/material-evaluation`

| 接口 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/material-evaluation/tasks` | GET | JWT | 获取当前用户的评估任务列表 |
| `/api/material-evaluation/upload` | POST | JWT | 上传 PDF 文件并创建评估任务 |
| `/api/material-evaluation/tasks/<id>` | GET | JWT | 获取评估任务详情和进度 |
| `/api/material-evaluation/tasks/<id>/status` | GET | JWT | 轮询评估任务状态（pending/processing/completed/failed） |
| `/api/material-evaluation/reports/<id>` | GET | JWT | 获取评估报告数据（评分、维度、评价内容） |
| `/api/material-evaluation/reports/<id>/pdf` | GET | JWT | 下载 PDF 报告（已有缓存则直接返回，无缓存则生成后返回，约需 30~60s） |

**上传请求示例**：

```json
// multipart/form-data
{
  "file": "（PDF 文件，最大 50MB）",
  "evaluation_type": "ppt",  // 或 "report"
  "file_name": "项目路演PPT"
}
```

**报告响应示例**：

```json
{
  "code": 200,
  "message": "获取成功",
  "data": {
    "id": 1,
    "evaluation_type": "ppt",
    "file_name": "项目路演PPT",
    "total_score": 85.5,
    "level": "优秀",
    "summary": "整体表现优秀...",
    "dimension_scores": {
      "content_integrity": 88,
      "expression_logic": 82,
      ...
    },
    "advantages": ["内容完整", "表达清晰"],
    "problems": ["市场数据不足"],
    "suggestions": ["补充市场规模数据"]
  }
}
```

> **注意**：PDF 生成使用 Reportlab 库，首次加载 CID 中文字体（STSong-Light）需要约 30~60 秒。下载时不会返回 502（代理超时已设为 300s），已有缓存则秒级返回。

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

| 路径                          | 组件                                   | 说明       |
| --------------------------- | ------------------------------------ | -------- |
| `/portal`                   | portal/PortalHome.vue                | 平台首页     |
| `/competition-center`       | portal/CompetitionCenter.vue         | 竞赛报名中心   |
| `/external-competitions`    | portal/ExternalCompetitions.vue      | 校外竞赛     |
| `/external-competitions/:slug` | portal/ExternalCompetitionDetail.vue | 校外竞赛详情   |
| `/competitions`             | portal/CompetitionSquare.vue         | 校内竞赛     |
| `/competitions/:id`         | portal/CompetitionDetail.vue         | 校内竞赛详情   |
| `/training-camps`           | portal/TrainingCamps.vue             | 训练营      |
| `/training-camps/:id`       | portal/TrainingCampDetail.vue        | 训练营详情    |
| `/courses`                  | portal/Courses.vue                   | 在线课程     |
| `/courses/:id`              | portal/CourseDetail.vue              | 课程详情     |
| `/industry-topics`          | portal/IndustryTopics.vue            | 产业命题     |

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
| project\_id     | Integer (FK → projects) | 关联项目 ID（可空）                                    |
| leader\_id      | Integer (FK → users) | 队长用户 ID                                         |
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
| innovation\_score   | Float                | 创新性评分 |
| feasibility\_score  | Float                | 可行性评分 |
| market\_score       | Float                | 市场评分  |
| team\_score         | Float                | 团队评分  |
| business\_score     | Float                | 商业评分  |
| technology\_score   | Float                | 技术评分  |
| presentation\_score | Float                | 展示评分  |
| total\_score        | Float                | 总分    |
| comment             | Text                 | 评审意见  |
| created\_at         | DateTime             | 创建时间  |
| updated\_at         | DateTime             | 更新时间  |

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

| 字段               | 类型                      | 说明                                                                                       |
| ---------------- | ----------------------- | ---------------------------------------------------------------------------------------- |
| id               | Integer (PK)            | 任务 ID                                                                                    |
| user\_id         | Integer (FK → users)    | 发起用户 ID                                                                                  |
| project\_id      | Integer (FK → projects) | 关联项目 ID（可空）                                                                              |
| registration\_id | Integer                 | 关联报名 ID（可空，FK → competition\_registrations）                                               |
| capability       | String(50)              | 能力类型（material\_qa / bp\_check / roadshow / review\_assist / competition\_recommend / navigate 等） |
| input\_params    | Text                    | 输入参数（JSON 格式）                                                                            |
| result           | Text                    | AI 输出结果                                                                                  |
| status           | String(20)              | 任务状态（pending / processing / completed / failed，默认 pending）                               |
| error\_message   | Text                    | 错误信息（失败时记录）                                                                              |
| created\_at      | DateTime                | 创建时间                                                                                     |
| completed\_at    | DateTime                | 完成时间（可空）                                                                                |

#### AgentMaterialIndex（AI 智能体材料索引）

| 字段               | 类型                            | 说明                                                         |
| ---------------- | ----------------------------- | ---------------------------------------------------------- |
| id               | Integer (PK)                  | 索引 ID                                                      |
| source\_type     | String(30)                    | 来源类型（project / registration / file 等）                     |
| source\_id       | Integer                       | 来源 ID                                                      |
| project\_id      | Integer (FK → projects)       | 关联项目 ID（可空）                                               |
| registration\_id | Integer                       | 关联报名 ID（可空，FK → competition\_registrations）                |
| file\_hash       | String(64)                    | 文件哈希值（用于去重，可空）                                            |
| index\_path      | String(500)                   | FAISS 索引文件路径                                               |
| status           | String(20)                    | 索引状态（pending / indexing / completed / failed，默认 pending）   |
| error\_message   | Text                          | 错误信息（失败时记录）                                               |
| indexed\_at      | DateTime                      | 索引完成时间（可空）                                                |
| created\_at      | DateTime                      | 创建时间                                                       |
| updated\_at      | DateTime                      | 更新时间                                                       |

#### MaterialEvaluation（AI 材料评估）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer (PK) | 评估记录 ID |
| user\_id | Integer (FK → users) | 用户 ID |
| evaluation\_type | String(20) | 评估类型（ppt / report） |
| file\_name | String(255) | 原始文件名 |
| status | String(20) | 状态（pending / processing / completed / failed） |
| total\_score | Float | 综合评分（百分制） |
| level | String(20) | 等级评定（优秀 / 良好 / 一般 / 待改进） |
| advantages\_json | Text | 核心优势列表（JSON 数组） |
| problems\_json | Text | 主要风险列表（JSON 数组） |
| suggestions\_json | Text | 优化方向列表（JSON 数组） |
| dimension\_scores\_json | Text | 8 维度评分数据（JSON 对象） |
| summary | Text | 综合评价摘要 |
| pdf\_path | String(500) | PDF 报告存储路径 |
| created\_at | DateTime | 创建时间 |
| updated\_at | DateTime | 更新时间 |

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

### 统一卡片设计（SparkPortalCard）

竞赛广场、训练营、课程、产业命题 4 个门户列表页使用统一的 [SparkPortalCard](frontend/src/components/portal/SparkPortalCard.vue) 卡片组件：

| 卡片属性       | 规范值 / 说明                                                  |
| -------------- | -------------------------------------------------------------- |
| 圆角           | `border-radius: 20px`                                          |
| 封面高度       | `170px`                                                        |
| 封面图片       | 使用 `<img>` + `object-fit: contain` 展示真实海报，避免关键文字被裁切；有图片时不再叠加重复封面标题 |
| 卡片最小宽度   | `300px`（grid `minmax(300px, 1fr)`）                           |
| hover 上浮     | `translateY(-6px)`                                             |
| hover 阴影     | `0 16px 32px -8px rgba(0,0,0,0.12)`                           |
| 渐变封面动画   | `background-size: 300%`, `sparkGradientFlow` 8s ease infinite  |
| 无障碍         | `prefers-reduced-motion: reduce` 时关闭持续动画                 |
| 主按钮样式     | 蓝紫渐变 `linear-gradient(135deg, #2563eb, #7c3aed)`，圆角 12px |
| 标签样式       | `border-radius: 8px`, `background: #f1f5f9`, `font-size: 11px` |
| 布局           | `display: flex; flex-direction: column`，按钮固定底部          |

**各业务模块渐变色方案**：

| 业务模块   | 渐变配色                                     | 说明             |
| ---------- | -------------------------------------------- | ---------------- |
| 校外竞赛   | 蓝紫/青绿/橙红渐变 + 官方海报图               | 国家级赛事，列表和详情页接入 `externalCompetitions.js` 的 `posterImage` |
| 校内竞赛   | 分类动态渐变（青蓝/紫蓝/翠绿/橙红等 11 种）  | 按竞赛类别自动匹配 |
| 训练营     | 各训练营独立渐变（蓝青/紫粉/橙红/翠绿）      | 按训练营主题区分   |
| 课程       | 各课程独立渐变（青蓝/紫粉/翠绿/橙红/靛蓝）   | 按课程主题区分     |
| 产业命题   | 各命题独立渐变（青蓝/翠绿/紫粉/橙红）        | 按企业命题区分     |

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

### 12. 接口超时 / 502

**AI 智能体接口超时**
1. LLM 密集型接口（BP 体检、路演稿、评审辅助）耗时较长，Vite 代理超时已设为 120 秒
2. 偶发 502 可重试，通常第二次请求会成功
3. 前端 API 客户端超时已设为 120 秒（`agentTimeout`）
4. 检查 `.env` 中 `GLM_API_KEY` 和 `GLM_BASE_URL` 是否正确（通义千问为主要模型）
5. 如使用火山方舟模型，检查 `ARK_API_KEY` 和 `ARK_BASE_URL`

**PDF 下载超时**
1. PDF 报告首次生成需要加载 CID 中文字体，耗时约 30~60 秒
2. 已去掉 `refresh=1` 强制刷新参数，已有缓存 PDF 秒级下载
3. Vite 代理超时已设为 300 秒，前端 Axios 超时已设为 300 秒
4. 如仍遇 502，等待 30 秒后重试即可

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
| Live2D 虚拟形象 | ✅ 完成 | 全屏拖拽/关键字表情联动/位置持久化/拖拽按钮跟随/面板开关联动 |
| 证书成果        | ✅ 完成 | 证书列表/获奖记录/查看详情弹窗/证书图片                                         |
| 我的赛事        | ✅ 完成 | 报名列表/海报封面/状态跟踪                                                |
| 全局引导系统      | ✅ 完成 | 首次登录引导/步骤导航/路由跳转/状态持久化                                        |
| 数据看板        | ✅ 完成 | 4 角色看板/统计图表/动态数据/最近数据                                         |
| 管理后台        | ✅ 完成 | 用户/项目/竞赛/报名/评审管理                                              |
| 首页数字雨       | ✅ 完成 | 全局 Canvas 数字雨背景/科幻风格/扫描线/全屏铺满                                 |
| Banner 动画   | ✅ 完成 | 竞赛/训练营/课程各具独特渐变色+光球动画                                         |
| AI 项目智能体 | ✅ 完成 | 12 大 AI 能力（智能引航/材料问答/BP 体检/路演稿/评审辅助/竞赛推荐/项目创意/模拟答辩/批量审核/智能反馈/评审草稿/评分检查）+ LangChain + FAISS + BM25 |
| AI 材料评估   | ✅ 完成 | PPT/报告 PDF 智能评估（上传→AI 分析→评分报告→PDF 下载），含飞入动画报告页、reportlab 专业化 PDF 报告生成 |
| 在线测评      | ✅ 完成 | 8 套主题化测评卡片（SVG 装饰+CSS 动画）+ 10 题×4 选项问卷 + 40 分制评分 + 维度分析 + PDF 导出 |
| 一键启动      | ✅ 完成 | start.bat 自动检测依赖+停止旧进程+启动前后端 |

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


### v4.10.2 - 2026-07-02（当前版本）

> 修复 Live2D 模型对话时眼睛高频闪烁（“星星眼”）问题

#### 🐛 Bug 修复

- **Live2D 对话表情闪烁**：修复了在 AI 对话播放语音时，由于 Live2D Widget 底层音频分析器自动驱动 `ParamMouthOpenY`（嘴部张合参数），且当前模型的嘴部参数意外关联了眼睛放大，导致眼睛高频闪烁“星星眼”的问题。通过在 `HuahuoAssistant.vue` 的 `__applyOverlayStateToCore` 渲染拦截器中，强制将每一帧的 `ParamMouthOpenY` 锁定为 0，彻底切断了音频到眼睛的污染链路，稳定了对话期间的表情显示。

***

### v4.10.1 - 2026-07-01

> AI 语音 TTS 发音精细化清洗 + 重播防超时降级机制恢复 + 提示词极致精简瘦身

- **功能修改**
  - AI 大模型系统提示词优化（`backend/services/ai_service.py`：新增强制使用全中文标点及严格禁止输出无必要英文单词、Emoji表情和代码块的底层规则；要求 AI 仅输出最终精简回答，彻底省略中间思路与分析说明，大幅削减无用文字输出以节省 Token 并加速音频合成）

- **Bug 修复**
  - 语音合成 (TTS) 异常中英文混读与乱码播报（`backend/services/ai_service.py` & `frontend/src/components/HuahuoAssistant.vue`：针对流式文本中的 Markdown 列表破折号、英文省略号 `...`、斜杠 `/` 及独立句号进行了深层正则清洗与中文顿号/句号替换，强制剔除所有超出中英文字符圈的扩展 Unicode 符号及代码块标签符，彻底杜绝发声引擎在朗读时穿插“减减”、“dot”、“slash”等毫无逻辑的英文解析发音）
  - AI 回答完毕后重播点击无响应/超时（`frontend/src/components/HuahuoAssistant.vue`：撤销前端 `speakText` 重读时激进的“整段合流请求”方案，恢复 `splitSpeakableSegments` 按换行符分片流式请求音频的队列机制，解决文字较长时因调用云端长文本音频合成接口过久导致的前端死锁不发声问题）
  - Live2D 表情异常闪烁回退（`frontend/src/components/HuahuoAssistant.vue`：拦截多次同级情绪调用，修复了在语音流式渲染中，若语句中包含多个不同情绪关键词导致的表情闪跳并高频重置回默认表情 06 0.0 的视觉缺陷）

### v4.10.0 - 2026-06-30

> AI 助手权限校验全面解耦 + 前端全局权限拦截升级 + 撤回逻辑闭环优化

- **功能修改**
  - 前端路由全局拦截器支持动态角色提示（`frontend/src/router/index.js`：从原“仅限学生操作”与“权限不足”升级为基于 `meta.roles` 的枚举拼装提示，跨角色跳转将弹出诸如“此功能仅限【教师或评委】操作，已为您返回工作台”的精准引导）
  - 门户“竞赛及命题”非学生视角样式锁定（`CompetitionSquare.vue`、`IndustryTopics.vue` 等：非学生角色下“立即报名/承接命题”主按钮置灰并变更为“当前角色不可报名”，消除功能可用性歧义）
  - 竞赛报名撤回流程重做（`backend/routes/registration.py`：修复报名记录为 withdrawn 状态时前端无法复用编辑的问题，现在用户撤销报名后可以正常点击“继续完善表单”）

- **Bug 修复**
  - 评委 (Judge) AI 助手权限过度阻断（`backend/routes/agent.py`：移除了 `_check_project_access` 中评委必须是 submitted/judging/reviewing 状态才可访问的硬编码限制，现在非草稿(draft)状态均可放行，恢复了评委对“已通过 (passed)”等项目的“材料解析、QA问答、评审草稿生成、一致性检查”所有能力）
  - 教审端评审意见跨库流转脱节（`backend/routes/review.py` 等：填补了针对已审核项目老师意见 `remark` 不可见的问题，以及完善了提交时 201 Created 的 RESTful 响应状态匹配）
  - 教师批量评审越权漏洞修复（`backend/routes/agent.py`：修复 `/batch-review` 接口未强制校验指导教师身份的问题，增加 `_check_project_access` 判断，防止平行越权查询其他项目的数据）

- **安全与稳定性**
  - 强化本地秘钥防泄漏机制（全局及子目录 `.gitignore`：修正了原错误的不忽略 `.env` 规则，强制忽略所有环境配置和本地数据库文件，防止 API Key 被意外推送到远端仓库）


### v4.9.0 - 2026-05-13

> PDF 首页封面重构 + 在线测评卡片主题化 + PDF 下载 502 修复 + 全链路稳定性优化

- **新增功能**
  - 在线测评 8 套独立 SVG 主题装饰系统（[assessmentVisualThemes.js](innovation-competition-platform/frontend/src/data/assessmentVisualThemes.js)：创业精神/创业性格/创业能力/职业规划/专业技能/团队协作/沟通表达/解决问题，每套含独特 SVG 装饰图案）
  - 测评卡片 5 种 CSS 动画效果（svgPulse 脉冲呼吸、svgFloat 悬浮漂移、svgRotateSlow 缓慢旋转、svgBarGrow 柱状生长、svgPulseDelay 交错脉冲）

- **功能修改**
  - PDF 报告封面彻底重构（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：封面改为垂直三卡片排布（核心优势/主要风险/优化方向），标题字号全面提升（品牌 11pt→14pt、报告标题 20pt→28pt、总分 32pt→40pt），内容整体居中布局，每模块有独立圆角卡片+内容居中视觉）
  - 在线测评卡片封面重新设计（[OnlineAssessment.vue](innovation-competition-platform/frontend/src/views/portal/OnlineAssessment.vue)：封面高度 160→180px，居中大白字改为左上角 cover-tag + 左下角 cover-sub，SVG 装饰成为主视觉）

- **Bug 修复**
  - 修复 PDF 下载返回 502 Bad Gateway（[materialEvaluation.js](innovation-competition-platform/frontend/src/api/materialEvaluation.js)：去掉 `refresh=1` 强制刷新参数，不再每次下载都删除缓存 PDF 重新生成；[vite.config.js](innovation-competition-platform/frontend/vite.config.js)：代理超时从 120s 提升至 300s 应对 CID 字体渲染慢场景；[material_evaluation.py](innovation-competition-platform/backend/routes/material_evaluation.py)：去掉 force_refresh 逻辑，优先使用已有缓存 PDF 直接返回）
  - 修复 student1 密码与登录页演示账号不一致（fix_password.py：重置为 student123 与登录页一键填充匹配）

- **安全与稳定性**
  - PDF 生成请求超时保护（Vite proxyTimeout 300s + Axios timeout 300s，防止慢请求被截断为 502）
  - 后端启动脚本恢复完整版本（[start.bat](innovation-competition-platform/start.bat)：含端口清理/依赖检查/前后端顺序启动）

- **文档更新**
  - README 全量更新至 v4.9.0：新增 AI材料评估特色功能章节、补充 material-evaluation 路由和 API 端点、更新项目结构、更新当前开发状态

### v4.8.0 - 2026-05-12

> 在线测评卡片视觉升级 + PDF 报告模板专业化重构 + PDF 下载全链路安全性增强

- **新增功能**
  - 在线测评卡片主题化视觉系统（[OnlineAssessment.vue](innovation-competition-platform/frontend/src/views/portal/OnlineAssessment.vue)：每种测评类型独立 SVG 主题装饰：spark-energy、radar-dots、balance-scale、path-direction、geometric-diamond、growth-spiral、speech-bubbles、wave-balance）
  - 测评卡片 5 种 CSS 动画（svgPulse 脉冲呼吸、svgFloat 悬浮漂移、svgRotateSlow 缓慢旋转、svgBarGrow 柱状生长、svgPulseDelay 交错脉冲）
  - PDF 报告生成三种不同维度说明（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：PPT 评估侧重"路演表达的完整性、逻辑性和说服力"，报告评估侧重"材料内容的论证深度、数据支撑和商业可行性"）
  - PDF 下载安全全链路增强（[material_evaluation.py](innovation-competition-platform/backend/routes/material_evaluation.py)：后端文件大小检查、自动删除 0KB 缓存重试、Content-Length / Content-Disposition 头；[request.js](innovation-competition-platform/frontend/src/api/request.js)：blob 响应 Content-Type 错误检测与 JSON 错误解析回退；[AIMaterialEvaluationReport.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationReport.vue)：双重 disabled 禁用 + 函数首行 guard 防并行触发）

- **功能修改**
  - 在线测评卡片封面全面重构（[OnlineAssessment.vue](innovation-competition-platform/frontend/src/views/portal/OnlineAssessment.vue)：移除居中大白字 `cover-label`，改为左上角小号标签 `cover-tag` + 左下角主题副标题 `cover-sub`，SVG 装饰成为主视觉；封面高度从 160px 提升至 180px）
  - PDF 报告封面专业化重构（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：深蓝全幅 Navy 封面 + 火花图标 Logo + 24pt 标题 + 48pt 总分 + 色块等级标签 + 文件元信息 + 报告编号 + 综合评价一句话 + 三栏核心优势/风险/优化方向 + 品牌落款）
  - PDF 评分维度表改进（紫色表头 #6366F1 + 120° 条形进度条 + 得分率百分比 + 绿/橙/红三色得分标注）
  - PDF 章节标题改为紫色短横线分隔（14mm * 3pt）
  - 评估页面页面新增三个 SVG 主题配置（[assessmentVisualThemes.js](innovation-competition-platform/frontend/src/data/assessmentVisualThemes.js)：新增创业精神、创业性格、创业能力、职业规划、专业技能、团队协作、沟通表达、解决问题共 8 套独立主题）

- **Bug 修复**
  - 修复 PDF 下载可能产生 0KB 文件的根因（[material_evaluation.py](innovation-competition-platform/backend/routes/material_evaluation.py)：下载前检查 `os.path.getsize`，0KB 则删除缓存重建，重新生成后二次验证文件大小）

- **安全与稳定性**
  - PDF 下载接口增加文件大小检查，防止缓存 0KB 文件被下载
  - 前端 request 拦截器增强 blob 错误处理：Content-Type 为 HTML/JSON 时自动解析错误信息并拒绝下载
  - 前端下载按钮新增双重禁用防护（`:disabled` + 函数首行 guard），消除并行触发可能

- **Bug 修复**
  - 修复 PDF 下载误报"PDF报告内容为空"错误（[AIMaterialEvaluationReport.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationReport.vue)：简化 Blob 校验逻辑，去除导致误判的 `blob.size === 0` 和 `blob.type` 检查，仅在 blob 为 null/undefined 时报错）
  - 修复下载按钮导致 0KB 空文件问题（[AIMaterialEvaluationReport.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationReport.vue)：两个下载按钮添加 `:disabled="downloadingPDF"` 禁用状态 + `downloadPDF()` 首行 `if (downloadingPDF.value) return` 防重复触发，避免同一函数并行执行两次产生空 blob）
  - 修复 PDF 封面顶部内容被截断问题（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：移除 `ColorBlock` + 无效的负间距 `Spacer(1, -92*mm)`，改用自绘 `CoverFlowable` 在 240pt 高的单一 Flowable 内完成封面全内容渲染，避免 reportlab 不支持负 Spacer 导致的布局偏移）

- **功能修改**
  - SparkAI 品牌 Logo 嵌入封面（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：`CoverFlowable` 使用 canvas 路径绘制 8 角火花图标，紫色 #A78BFA）
  - 封面全幅 Navy 色块 + Logo + 标题 + 大号总分 + 色块等级标签 + 文件元信息 + 品牌落款，一次性渲染不截断
  - 完全重写 PDF 报告生成模块（[material_report_pdf.py](innovation-competition-platform/backend/services/material_report_pdf.py)：基于 ui-ux-pro-max 专业设计系统重构）
  - 深蓝配色封面页（#0F172A 全幅色块标题区 + 大白字报告标题 + SUBTITLE + 大号总分 + 色块分级标签 + 文件信息 + SparkAI 品牌落款）
  - 专业评分维度表（#0369A1 蓝色表头 + 交替行背景色 + 分数按阈值绿/橙/红三色显示）
  - 核心评价卡片（浅灰背景 #F8FAFC + 蓝色左边框强调）
  - 四色分点列表：绿色圆点「主要优势」+ 橙色圆点「待改进项」+ 蓝色圆点「优化建议」+ 蓝色序号「下一步行动」
  - 章节标题带蓝色短横线（18mm * 3pt）可识别分隔
  - 统一使用 A4 标准纸张尺寸 + 18mm 舒展边距

### v4.7.1 - 2026-05-12

> AI材料评估 Bug 修复与体验优化：修复 PDF 下载失败、上传状态不同步问题，优化评估中心、上传页、报告页布局

- **Bug 修复**
  - 修复 PDF 下载失败问题（[AIMaterialEvaluationReport.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationReport.vue)：前端 Blob 错误检测增强；[material_evaluation.py](innovation-competition-platform/backend/routes/material_evaluation.py)：下载接口增加目录创建和文件存在性检查）
  - 修复第一次上传不生效问题（[AIMaterialEvaluationUpload.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationUpload.vue)：重构文件输入方式，隐藏 input → 程序化触发 click，清除 value 以支持同一文件重复选择）

- **功能修改**
  - 优化 AI材料评估中心布局（[AIMaterialEvaluation.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluation.vue)：移除负边距重叠，Cards 区域 padding 48px 与 Hero 自然分离）
  - 优化上传页布局（[AIMaterialEvaluationUpload.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationUpload.vue)：移除负边距，padding 48px 上下间距，上传卡片成为视觉中心）
  - 优化报告页总分摘要区域布局（[AIMaterialEvaluationReport.vue](innovation-competition-platform/frontend/src/views/portal/AIMaterialEvaluationReport.vue)：移除 report-body 负边距，Hero 底部 padding 增加至 32px）

- **安全与稳定性**
  - PDF 下载接口增加 `os.makedirs(output_dir, exist_ok=True)` 确保输出目录存在

### v4.7.0 - 2026-05-12

> 新增 AI材料评估功能：支持路演PPT和项目报告的PDF智能评估，含进度动画、飞入式报告页、PDF报告下载

- **新增功能**
  - 新增 AI材料评估功能入口（PortalHome 新增 AI材料评估卡片）
  - 新增 PPT评估流程：上传PDF → AI分析进度页 → 评分报告页
  - 新增 报告评估流程：上传PDF → AI分析进度页 → 评分报告页
  - 新增 评分报告页飞入动画：各模块从上下左右四个方向飞入组合成完整报告
  - 新增 PDF 报告下载（后端 reportlab 生成含封面、维度表、建议、行动计划的标准报告）
  - 新增 MaterialEvaluation 数据模型（backend/models/material_evaluation.py）
  - 新增 material_evaluation 蓝图路由（backend/routes/material_evaluation.py，7 个端点）
  - 新增 material_evaluation_service 评分服务（backend/services/material_evaluation_service.py，PPT/报告不同的 8 维度评分体系）
  - 新增 material_report_pdf 报告生成服务（backend/services/material_report_pdf.py）

- **功能修改**
  - MainLayout 顶栏和 platformPages 新增 AI材料评估入口
  - PortalHome allCards 新增 material-evaluation 卡片（violet 配色）

- **安全与稳定性**
  - 仅允许上传 PDF 文件（扩展名 + MIME type 双重校验，最大 50MB）
  - 用户只能查看和下载自己的评估报告（JWT 身份校验）

- **已知问题**
  - PPT评估和报告评估的评分结果基于规则模拟生成，非真实 AI 模型输出
  - PDF 关键词命中统计需要 PyPDF 或 PyMuPDF 库支持

### v4.6.0 - 2026-05-12

> 在线测评问卷重构：题库结构改为 10 题 × 4 选项 A/B/C/D，评分满分调整为 40，卡片封面添加艺术字，简化展示元素

#### 新增功能

- **独立题库文件**：新增 [assessmentQuestionnaires.js](frontend/src/data/assessmentQuestionnaires.js)，5 个真实问卷（创业精神/创业性格/创业兴趣/创业能力/团队合作），每个严格 10 题 × 4 选项 A/B/C/D，选项分数 1-4，含自动校验函数 `validateAllQuestionnaires()`
- **独立评分工具**：新增 [assessmentScoring.js](frontend/src/utils/assessmentScoring.js)，满分 40 分计分体系，4 级等级（优秀 35+ / 良好 28+ / 发展中 19+ / 待提升 10+）、维度分析（动态百分比柱状图）、智能综合评价生成、改进建议自动生成、sessionStorage 存取 API（`saveResult/getResult/clearResult`）+ 临时答题进度暂存（`persistTempAnswers/getTempAnswers`）
- **卡片封面艺术字**：卡片渐变封面居中显示测评关键词艺术字（28px 字号 font-weight 900，大字符间距 0.12em，白色半透明 + 双重文字阴影，采用中空留白字间距样式如"创 业 精 神"），替代旧右上角标签模式

#### 功能修改

- **OnlineAssessment.vue** 界面简化：删除 Banner 统计数据区（真实测评数/即将开放数/总题目数），删除卡片底部"真实可测/即将开放"标签和标签容器，卡片按钮改为右对齐（`justify-content: flex-end`），封面区域改为居中对齐（`align-items: center; justify-content: center`），移除 `card-cover-pattern` 装饰层
- **AssessmentDetail.vue** 答题交互重构：5 点量表改为 4 选项 A/B/C/D（圆形 radio 按钮 + 字母 key + 选项文本），必须选择后才能点下一题（未选时显示黄色提醒 + fadeIn 动画），第 10 题自动显示"提交测评"，slide-fade 方向动画（切入从右 +30px，切出向左 -20px），提升到 0.23s/0.18s 手感，选项 hover scale(1.01) / active scale(0.99) 微交互
- **AssessmentResult.vue** 评分体系更新：适配满分 40 分，等级改为优秀/良好/发展中/待提升（35+/28+/19+/10+），维度分值 75%/50% 色阶分界，移除旧"优势突出""需要重点培养"等 5 级术语
- **assessmentBank.js** 数据层重构：移除内联 `questions` 数组和旧评分导出，改为导入 `getQuestionnaireById` / `validateQuestionnaire`（来自 `assessmentQuestionnaires.js`）+ `calculateScore` / `saveResult` / `getResult` / `clearResult` / `getLevel`（来自 `assessmentScoring.js`），纯卡片元数据文件
- **路由配置** / **MainLayout.vue** / **PortalHome.vue** 保持不变（路由仍为 /assessment 系列 4 条）

#### 文档更新

- **README.md**：版本变更记录新增 v4.6.0；v4.5.x 系列版本标记整理，旧版本"当前版本"标记清理

***


### v4.5.4 - 2026-05-12

> 在线测评功能上线：新增在线测评中心、答题页、结果页、建设中页面，支持 5 个真实测评（各 10 题）

#### 新增功能

- **在线测评模块**：在现有项目中新增「在线测评」完整产品功能，首页顶部导航和功能卡片区同时新增入口，点击进入 `/assessment` 测评中心
- **在线测评中心页**：新增 [OnlineAssessment.vue](frontend/src/views/portal/OnlineAssessment.vue)，包含蓝色渐变大 Banner（标题 + 统计数据）、左侧分类侧栏（全部分类/创业测评/就业测评/能力测评）、右侧双列卡片网格（带渐变封面、元信息、标签、搜索框），支持分类筛选和关键词搜索，响应式适配移动端
- **答题页**：新增 [AssessmentDetail.vue](frontend/src/views/portal/AssessmentDetail.vue)，真实测评进入逐题答题模式。包含 sticky 顶部导航（题目进度条 + 计时器）、题目卡片（第 N 题标签 + 维度标签 + 5 点量表选项）、右侧信息面板（测评信息 + 题目导航网格 + 图例）、底部操作栏（上一题/下一题/提交/返回）
- **测评结果页**：新增 [AssessmentResult.vue](frontend/src/views/portal/AssessmentResult.vue)，提交后展示完整分析报告。包含蓝色渐变 Header（标题 + 副标题）、综合评估卡片（SVG 环形分数图 + count-up 动画 + 等级标签 + 得分/完成率统计）、综合评价、改进建议（编号列表）、维度分析（条形图带动态填充 + 颜色分级）
- **建设中页面**：新增 [AssessmentComingSoon.vue](frontend/src/views/portal/AssessmentComingSoon.vue)，非真实测评进入，展示测评名称、所属分类、预计开放方向、即将开放标签、返回中心和查看已开放按钮
- **测评数据与评分引擎**：新增 [assessmentBank.js](frontend/src/data/assessmentBank.js)，集中管理 12 个测评卡片、3 个分类、5 套真实题库（各 10 题含维度/反向标识）、统一的评分逻辑和 sessionStorage 存取 API

#### 功能修改

- **路由配置**（`frontend/src/router/index.js`）：新增 4 条路由——`/assessment`（测评中心，`public: true`）、`/assessment/:id`（答题页，hidden + public）、`/assessment/:id/result`（结果页，hidden + public）、`/assessment/:id/coming-soon`（建设中，hidden + public），全部设置 `platformPage: true` 无侧边栏
- **MainLayout.vue**：顶部导航 `topNavConfig` 新增「在线测评」入口（所有角色可见，位于产业命题之后），`isTopNavActive` 新增 `/assessment` 匹配规则，`platformPages` 数组新增 `/assessment` 以支持平台布局
- **PortalHome.vue**：功能入口卡片 `allCards` 数组新增「在线测评」卡片（indigo 色，TrendCharts 图标，描述"获取创业能力、团队协作等能力画像"），所有角色可见

***


### v4.5.3 - 2026-05-12

> 竞赛详情页海报显示修复：校内竞赛/校外竞赛海报改为自适应高度，与课程详情页保持一致

#### Bug 修复

- **校内竞赛详情页海报显示不全**（`frontend/src/views/portal/CompetitionDetail.vue`）：`.detail-poster` 移除固定 `min-height: 400px` 和 `overflow: hidden`；`.poster-img` 改为 `height: auto` + `aspect-ratio: 16/9`；`.poster-fallback` 移除绝对定位，改为自适应高度布局
- **校外竞赛详情页海报显示不全**（`frontend/src/views/portal/ExternalCompetitionDetail.vue`）：`.detail-hero` 移除固定 `min-height: 400px` 和 `overflow: hidden`；`.hero-image` 改为 `height: auto` + `aspect-ratio: 16/9`；`.hero-overlay` 改为只覆盖底部区域

#### 文档更新

- **README.md**：版本变更记录新增 v4.5.3；v4.5.2 移除"当前版本"标记

***


### v4.5.2 - 2026-05-12

> 产业命题模块补齐：新增产业命题详情页 + 数据抽离 + 列表页改造

#### 新增功能

- **产业命题详情页**：新增 [IndustryTopicDetail.vue](frontend/src/views/portal/IndustryTopicDetail.vue)，产业命题模块拥有与校外竞赛、校内竞赛、训练营、课程一致的独立详情展示页。页面结构包含：深青蓝渐变 Hero（标题、企业、难度/周期/预算标签、摘要、承接 CTA + 返回列表）、面包屑导航、左右分栏布局（16:8）、8 个内容章节（命题背景、需求说明、技术方向标签、交付物要求、周期安排时间线、奖励与支持高亮区、适合团队信息网格、评分验收标准列表）、右侧 sticky 吸附操作卡（命题信息 + 承接命题 + 返回列表 + 命题标签）、底部再度 CTA 引导区、空状态友好提示页。视觉风格与现有详情页保持统一（18px 大圆角卡片、靛紫点缀色、36px 章节图标、柔和阴影、移动端 768px 断点自适应）
- **产业命题数据抽离**：新增 [industryTopics.js](frontend/src/data/industryTopics.js)，将 4 个命题的完整数据从组件内联抽离到独立数据文件，包含 `getIndustryTopicById(id)` 查询函数。每个命题数据从原始的 10 个字段扩展为 17 个字段：新增 `status`、`summary`、`techDirections`、`schedule`（5 阶段时间线）、`evaluation`（评分权重）、`support`（企业支持）、`suitableTeam`（团队画像），数据字段从 `bonus` 改为语义化字段 `reward`/`budget`。列表页和详情页共享同一份数据源，避免重复维护
- **产业命题详情路由**：新增 `/industry-topics/:id` 路由，注册为 `IndustryTopicDetail`（组件懒加载），meta 设置 `platformPage: true` + `hidden: true`（与校外竞赛详情、校内竞赛详情路由配置一致），`/accept-topic/:id` 承接路由不受影响

#### 功能修改

- **IndustryTopics.vue 列表页改造**：卡片新增 `secondaryActionText="查看详情"` 按钮（含 `View` 图标），新增 `onCardClick` 卡片主体点击跳转详情页，`onPrimaryClick`（承接命题）保留 `@click.stop` 阻止冒泡；数据引用从内联 `ref([])` 改为导入 `@/data/industryTopics`；`handleAccept` 简化为直接路由跳转 `/accept-topic/:id`（带 query 参数 `topic_title`/`topic_company`），移除旧的 ElMessageBox 确认弹窗和异步延迟逻辑；移除约 100 行内联数据定义

#### 文档更新

- **README.md**：版本变更记录新增 v4.5.2；v4.5.1 移除"当前版本"标记

***


### v4.5.1 - 2026-05-12

> 门户列表卡片样式影响链审查与修复、统一 Grid 尺寸、公开访问

#### 功能修改

- **统一列表页 Grid 最小宽度**（`frontend/src/views/portal/TrainingCamps.vue`、`frontend/src/views/portal/Courses.vue`、`frontend/src/views/portal/CompetitionSquare.vue`）：训练营、课程、校内竞赛列表页的 grid 布局统一从 `minmax(300px/280px/320px, 1fr)` 调整为 `minmax(360px, 1fr)`，与校外竞赛保持一致，确保卡片尺寸统一。

#### Bug 修复

- **修复训练营/课程卡片样式不生效问题**：经审查发现各页面 grid 的 `minmax` 值不一致导致卡片尺寸差异，已统一为 360px。

#### 安全与稳定性

- **门户列表页公开访问**（`frontend/src/router/index.js`）：将 `/portal`、`/external-competitions`、`/competitions`、`/training-camps`、`/courses`、`/industry-topics` 及其详情页路由添加 `public: true` meta 标记，无需登录即可访问。

---


### v4.5.1 - 2026-05-11

> AI 助手窗口全面亮色化改造 + 拖拽缩放交互修复 + 项目智能体面板主题适配

#### 功能修改

- **AI 助手窗口亮色主题改造**（`frontend/src/components/HuahuoAssistant.vue`）：主背景从 `rgba(15, 23, 42, 0.96)` 暗色改为 `#ffffff` 纯白；强调色从 `#06b6d4`（青色）统一替换为 `#3b82f6`（蓝色）；主文字色从 `#e2e8f0`（浅色）改为 `#1e293b`（深色）；次要文字色从 `#94a3b8`/`#cbd5e1` 改为 `#475569`/`#64748b`；用户消息气泡从青色半透明改为蓝色半透明 `rgba(59, 130, 246, 0.12)`；助手消息气泡从深色半透明改为浅灰 `#f1f5f9`；输入区域背景从深色改为 `#f8fafc`；表情面板、分析结果区、markdown 渲染区全部适配亮色主题；所有 Element Plus 组件覆盖样式（表单标签、输入框、单选按钮、下拉菜单、分割线）同步更新为蓝色系亮色风格
- **项目智能体面板亮色适配**（`frontend/src/views/ai-assistant/AgentPanel.vue`）：能力卡片背景从青色半透明改为蓝色半透明；文字颜色从浅色改为深色；导航结果、能力结果区域背景从深色半透明改为 `#f8fafc`；所有 Element Plus 组件覆盖样式同步更新为蓝色系亮色风格

#### Bug 修复

- **拖拽缩放方向反直觉**：缩放手柄原在左上角，`dx = resizeState.startX - e.clientX` 导致鼠标向右下拖动时窗口变小。修复：手柄移至右下角，`dx = e.clientX - resizeState.startX`，鼠标向右下拖动时窗口自然变大（`frontend/src/components/HuahuoAssistant.vue`）
- **拖拽与缩放事件冲突**：缩放时拖拽事件同时触发导致窗口位置异常跳动。修复：`startDrag`/`startDragTouch` 增加 `resizeState.resizing` 检查；`onDrag`/`onDragTouch` 增加边界限制（`Math.max(0, Math.min(newX, maxX))`）；`startResize` 添加 `e.stopPropagation()` 阻止事件冒泡（`frontend/src/components/HuahuoAssistant.vue`）
- **标题栏按钮误触发拖拽**：整个 `panel-header` 区域都可拖拽，导致点击按钮时也触发窗口移动。修复：将拖拽事件从 `panel-header` 移到独立的 `.header-drag-area`（仅标题和标签区域），按钮区域不再触发拖拽（`frontend/src/components/HuahuoAssistant.vue`）

#### 安全与稳定性

- **移动端适配**：新增 `isMobile` 检测（`window.innerWidth <= 768`），移动端自动调整面板尺寸为 `min(360, 屏幕宽-20) × min(520, 屏幕高-100)`，位置固定在屏幕底部；桌面端与移动端状态切换时自动恢复/重置持久化数据（`frontend/src/components/HuahuoAssistant.vue`）

#### Bug 修复

- **退出登录后页面不跳转**：点击退出登录确认后，页面仍停留在首页且无反应。根因：`router.push('/login')` 跳转后，路由守卫检测到 `userStore.token` 和 `userStore.userInfo` 的响应式状态尚未同步更新，仍认为用户已登录，于是重定向回 `/portal`。修复：将 `router.push('/login')` 改为 `window.location.href = '/login'`，强制页面刷新，确保所有 Pinia 状态和组件实例完全重置（`frontend/src/layouts/MainLayout.vue`）
- **AI 助手窗口拖拽范围受限**：窗口只能完全在屏幕内拖动，无法拖到屏幕边缘外。修复：放宽边界限制，允许窗口部分超出屏幕（保留 100px 最小可见区域），实现全屏自由拖动（`frontend/src/components/HuahuoAssistant.vue`）
- **拖拽 Live2D 形象时误打开 AI 助手面板**：按住 Live2D 人物拖拽结束后，AI 助手面板会自动打开。根因：`mouseup` 事件触发时，虽然内部状态判定为拖拽，但 `openPanel()` 函数未被正确阻止。修复：新增全局 `isModelDragging` 标志，在拖拽开始时置为 `true`，`openPanel()` 函数中检测到该标志时直接返回不打开面板；`mouseup`/`touchend` 后延迟 100ms 重置标志，确保 click 事件也能正确检测（`frontend/src/components/HuahuoAssistant.vue`）
- **Live2D 形象眼睛闪烁**：Live2D 模型眼睛出现快速闪烁。根因：`__syncExpressionState` 函数中强制重置 `ParamEyeOpen` 等表情参数为 0，然后调用 `setExpression` 设置新表情；同时 `core.update` 每帧调用 `__applyOverlayStateToCore` 也会重置这些参数。两套系统互相干扰，导致眼睛参数在 0 和表情值之间快速切换。修复：① `__syncExpressionState` 中移除对 `ParamEyeOpen`/`ParamEyeSmile`/`ParamTear` 的强制重置，让 `setExpression` 自行管理表情参数；② `__applyOverlayStateToCore` 中跳过表情相关参数，只处理 overlay 特有的参数；③ `__syncExpressionState` 增加 150ms 防抖，避免短时间内多次切换；④ `startAutoExpression` 改用递归 `setTimeout` 实现 15-25 秒随机间隔，减少切换频率（`frontend/src/components/HuahuoAssistant.vue`）
- **竞赛详情页海报显示不全**：校外竞赛和校内竞赛详情页的 Hero 海报上半部分被裁切，无法完整显示。根因：海报图片使用 `object-fit: cover` 会裁剪图片以填充固定高度容器（`min-height: 520px`）。修复：将 `object-fit: cover` 改为 `object-fit: contain`，添加 `object-position: center top` 确保海报从顶部开始完整显示；降低 `min-height` 从 520px 到 400px，允许容器自适应图片比例（`frontend/src/views/portal/ExternalCompetitionDetail.vue`、`frontend/src/views/portal/CompetitionDetail.vue`）

#### 文档更新

- **README.md**：版本变更记录新增 v4.5.1；v4.5.0 移除"当前版本"标记

***


### v4.5.0 - 2026-05-12

> 统一列表卡片尺寸与结构、封面海报铺满、按钮对齐优化

#### 功能修改

- **统一卡片尺寸与结构**（`frontend/src/components/portal/SparkPortalCard.vue`、`frontend/src/views/portal/ExternalCompetitions.vue`）：校外竞赛、校内竞赛、训练营、课程、产业命题列表卡片尺寸统一；卡片容器添加 `display: flex; flex-direction: column`，内容区使用 `flex: 1`，元信息区和按钮区使用 `margin-top: auto` 固定在底部，确保不同卡片高度一致时按钮对齐。
- **统一列表卡片封面尺寸**（`frontend/src/components/portal/SparkPortalCard.vue`、`frontend/src/views/portal/ExternalCompetitions.vue`）：封面统一使用 `aspect-ratio: 16/9`；图片圆角移除，改为容器顶部圆角 `border-radius: 20px 20px 0 0`；图片使用 `object-fit: cover` 铺满封面区域。
- **产业命题详情页海报展示优化**（`frontend/src/views/portal/IndustryTopicDetail.vue`）：移除 `.detail-hero` 固定高度和 `overflow: hidden`，海报图片改用 `height: auto` + `aspect-ratio: 16/9` + `object-fit: contain` 完整显示，不裁切；内容区改为 `position: absolute` 定位在底部，渐变遮罩从下往上渐变。


### v4.5.0 - 2026-05-11

> UI 统一改版：新增 SparkPortalCard 统一卡片组件，改造校内竞赛/训练营/课程/产业命题 4 个门户列表页，实现与校外竞赛页面一致的圆角渐变卡片风格

#### 新增功能

- **SparkPortalCard 统一卡片组件**：新增 [SparkPortalCard.vue](frontend/src/components/portal/SparkPortalCard.vue)，抽取为全校竞赛/训练营/课程/产业命题 4 个列表页的可复用卡片组件。支持以下 props：`gradient`（动态渐变背景）、`coverImage`（封面图）、`coverTitle`（封面标题）、`level`/`status`（等级/状态角标）、`title`、`description`、`tags`（标签数组，支持 maxTags 控制显示数量）、`metaItems`（元信息列表，含 icon + text）、`primaryActionText`/`primaryActionIcon`（主按钮）、`secondaryActionText`/`secondaryActionIcon`（次按钮）、`clickable`/`onCardClick`（卡片点击）。卡片采用 20px 大圆角、170px 渐变封面区、flex column 布局使按钮固定在底部、hover 上浮 6px + 阴影增强 + 边框变色效果。渐变封面支持 `background-size: 300%` 动态流动动画，且尊重 `prefers-reduced-motion` 用户偏好（[SparkPortalCard.vue](frontend/src/components/portal/SparkPortalCard.vue)）

#### 功能修改

- **CompetitionSquare.vue（校内竞赛）改造**：替换旧 `.competition-card` 卡片为 SparkPortalCard 组件。新增 `competitionGradients` 渐变映射对象（按竞赛分类自动匹配青蓝/紫蓝/翠绿/橙红等 11 种渐变色），数据加载时同步计算 `posterGradient`。原有分页、分类筛选、搜索、状态筛选、路由跳转、报名逻辑全部保留（[CompetitionSquare.vue](frontend/src/views/portal/CompetitionSquare.vue)）
- **TrainingCamps.vue（训练营）改造**：替换旧训练营卡片为 SparkPortalCard 组件。每个训练营保留独立 `gradient` 配置（蓝青/紫粉/橙红/翠绿 4 色区分），训练营封面图通过 `campCoverMap` 映射到 `coverImage` 属性。原有课程详情弹窗（讲师团队、课程章节展开/折叠、课时播放）全部保留（[TrainingCamps.vue](frontend/src/views/portal/TrainingCamps.vue)）
- **Courses.vue（课程）改造**：替换旧课程卡片为 SparkPortalCard 组件。每个课程保留独立 `gradient` 配置（青蓝/紫粉/翠绿/橙红/靛蓝 5 色区分），课程封面图通过 `courseCoverMap` 映射。原有课程详情弹窗（课程简介、章节展开/折叠、学习数据统计）全部保留（[Courses.vue](frontend/src/views/portal/Courses.vue)）
- **IndustryTopics.vue（产业命题）改造**：替换旧命题卡片为 SparkPortalCard 组件。每个命题保留独立 `gradient` 配置（青蓝/翠绿/紫粉/橙红 4 色），新增 `industry` 字段（教育科技/环保双碳/金融科技/企业服务）用于标签展示。原有承接命题 ElMessageBox 确认弹窗、项目创建跳转逻辑全部保留（[IndustryTopics.vue](frontend/src/views/portal/IndustryTopics.vue)）
- **旧卡片 CSS 清理**：4 个页面中不再使用的旧卡片样式全部移除（CompetitionSquare 移除 `.competition-card` 等 7 条规则、TrainingCamps 移除 `.camp-card` 等 15 条规则 + 孤立的 `.camp-progress` 3 条规则、Courses 移除 `.course-card` 等 10 条规则、IndustryTopics 移除 `.topic-card` 等 8 条规则），共计约 250 行冗余 CSS 被清理

#### 文档更新

- **README.md**：版本变更记录新增 v4.5.0；v4.4.1 移除"当前版本"标记


### v4.4.1 - 2026-05-11

#### Bug 修复

- **Live2D 切换账户后加载不出来**：修复 `HuahuoAssistant.vue` 中 `loadLive2DLibraries()` 函数的脚本缓存问题。组件 `onBeforeUnmount` 时 `delete window.initWidget`，但重新挂载时因页面上残留旧 `<script>` 标签而跳过加载新脚本，导致 `initWidget` 为 `undefined`。修复方案：加载脚本前先检测并移除旧标签，然后无条件重新创建 `<script type="module">` 加载 `waifu-tips.js`，确保每次组件挂载都能拿到可用的 `initWidget`（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **启动后首页不是登录页**：修复 `router/index.js` 中根路径 `/` 无子路由导致显示空白布局的问题。新增 `{ path: '', redirect: '/portal' }` 重定向规则，使得访问根路径时自动跳转到 `/portal`；`beforeEach` 守卫会检查 token 有效性，无 token 时进一步重定向到 `/login`（[index.js](frontend/src/router/index.js)）

#### 文档更新

- **README.md**：版本变更记录新增 v4.4.1；v4.4.0 移除"当前版本"标记


### v4.4.0 - 2026-05-11

> 引导窗口、校外竞赛海报、Live2D 生命周期、登录路由回跳与统一卡片展示修复

#### 新增功能

- **校外竞赛官方海报接入**（`frontend/src/data/externalCompetitions.js`、`frontend/src/views/portal/ExternalCompetitions.vue`、`frontend/src/views/portal/ExternalCompetitionDetail.vue`）：为中国国际大学生创新大赛、挑战杯创业计划竞赛、三创赛新增 `posterImage` 字段，列表卡片和详情 Hero 使用 `src/assets/images/Off-campus_competitions/` 下的真实海报资源展示。

#### 功能修改

- **引导窗口交互强化**（`frontend/src/components/GuideSystem.vue`、`frontend/src/stores/guide.js`）：引导弹窗新增 `role="dialog"`、可聚焦、Esc 跳过、Enter 下一步/完成，弹窗定位钳制在视口内，进度节点可滚动查看，并对 `goToStep` 做边界约束。
- **统一卡片封面展示调整**（`frontend/src/components/portal/SparkPortalCard.vue`、`frontend/src/views/portal/CompetitionSquare.vue`、`frontend/src/views/portal/TrainingCamps.vue`、`frontend/src/views/portal/Courses.vue`、`frontend/src/views/portal/IndustryTopics.vue`）：封面图片从 `background-image` 改为 `<img>` + `object-fit: contain`，避免真实海报关键文字裁切；有封面图时不再重复显示封面标题，标题仅保留在卡片正文。
- **平台页布局判定统一**（`frontend/src/router/index.js`、`frontend/src/layouts/MainLayout.vue`）：为门户类路由增加 `meta.platformPage`，`MainLayout.vue` 优先读取路由 meta 判断无侧边栏平台页，减少路由表和布局清单重复维护。
- **登录后回跳体验完善**（`frontend/src/router/index.js`、`frontend/src/views/login/index.vue`、`frontend/src/api/request.js`）：未登录访问受保护页面时携带 `redirect` 查询参数，登录成功或 401 重新登录后可回到原访问路径。
- **Live2D 生命周期稳定性增强**（`frontend/src/components/HuahuoAssistant.vue`、`frontend/src/layouts/MainLayout.vue`、`frontend/src/composables/useLive2d.js`）：新增初始化并发锁，重试失败保留错误状态并提示刷新；按用户/角色 key 重挂载 `HuahuoAssistant`；修正 `window.__syncExpressionState(expression)` 字符串参数同步语义。

#### Bug 修复

- **修复引导按钮拖拽监听无法移除**（`frontend/src/components/GuideSystem.vue`）：修正 `stopBtnDragFn` 未定义导致 `mouseup` 监听残留的问题，组件卸载时同步清理弹窗和按钮拖拽监听。

#### 安全与稳定性

- **AI Markdown 安全渲染**（`frontend/src/components/HuahuoAssistant.vue`）：`marked.parse()` 结果改为通过 DOMPurify 净化后再进入 `v-html`，降低 AI 回复或分析结果中恶意 HTML 注入风险。

#### 文档更新

- **README 同步更新至 v4.4.0**（`README.md`）：同步更新 Live2D、全局引导、双模式布局、项目结构、统一卡片设计与版本变更记录。

#### 已知问题

- **校外竞赛数据仍为静态维护**（`frontend/src/data/externalCompetitions.js`）：赛事时间、状态、官网入口和海报仍需随官方通知手动更新，暂未接入后端管理接口。


### v4.4.0 - 2026-05-11

> 竞赛模块拆分：新增校外竞赛独立入口，实现校外/校内竞赛双入口分流架构

#### 新增功能

- **竞赛报名中心页**：新增 [CompetitionCenter.vue](frontend/src/views/portal/CompetitionCenter.vue)，作为竞赛入口分流页，提供「校外竞赛」与「校内竞赛」两张视觉差异化入口卡片。左侧校外竞赛采用蓝紫渐变并聚合国家级赛事资讯，右侧校内竞赛沿用青色主色并支持平台内报名、团队、材料、审核全流程
- **校外竞赛数据模块**：新增 [externalCompetitions.js](frontend/src/data/externalCompetitions.js) 静态数据文件，包含 3 个真实国家级赛事（中国国际大学生创新大赛、挑战杯创业计划竞赛、三创赛）的完整信息：赛事简介、赛道/类别、时间安排、奖项设置、参赛要求、材料要求、官网链接
- **校外竞赛列表页**：新增 [ExternalCompetitions.vue](frontend/src/views/portal/ExternalCompetitions.vue)，以卡片式布局展示校外竞赛，包含分类筛选（全部/创新创业/创业计划/电子商务）、赛事封面渐变、标签、主办方、时间、简介，每张卡片提供「查看详情」和「前往官网」按钮
- **校外竞赛详情页**：新增 [ExternalCompetitionDetail.vue](frontend/src/views/portal/ExternalCompetitionDetail.vue)，复用校内详情页版式，包含 Hero 首屏、面包屑导航、赛事简介、赛道/类别、时间安排时间线、奖项设置、参赛要求、材料要求、官方入口 8 大内容板块。右侧吸附信息卡和操作卡提供「前往官网」按钮及「以官网通知为准」提示。支持 slug 不存在时的友好空状态展示
- **三个新路由**：注册 `/competition-center`、`/external-competitions`、`/external-competitions/:slug` 路由，均属平台页面不显示侧边栏（[index.js](frontend/src/router/index.js)）

#### 功能修改

- **顶部导航重构**：[MainLayout.vue](frontend/src/layouts/MainLayout.vue) 中「竞赛」更名为「校内竞赛」，并在其之前新增「校外竞赛」导航项。导航顺序调整为：首页 / 校外竞赛 / 校内竞赛 / 训练营 / 课程 / 产业命题
- **首页入口变更**：[PortalHome.vue](frontend/src/views/portal/PortalHome.vue) 中「竞赛报名」功能卡片跳转目标从 `/competitions` 改为 `/competition-center`，引导用户先到分流页选择竞赛类型
- **侧边栏菜单更新**：[MainLayout.vue](frontend/src/layouts/MainLayout.vue) 侧边栏中「竞赛广场」更名为「校内竞赛」，与顶部导航保持一致
- **平台页面列表扩展**：[MainLayout.vue](frontend/src/layouts/MainLayout.vue) 中 `platformPages` 数组新增 `/competition-center` 和 `/external-competitions`，确保新页面不显示侧边栏
- **导航 active 状态更新**：[MainLayout.vue](frontend/src/layouts/MainLayout.vue) 中 `isTopNavActive` 函数新增校外竞赛路由判断：访问 `/external-competitions` 及其详情页时高亮「校外竞赛」；访问 `/competitions`、校内详情页、报名页及 `/competition-center` 时高亮「校内竞赛」

#### 文档更新

- **README.md**：版本变更记录新增 v4.4.0；v4.3.4 移除"当前版本"标记


### v4.3.4 - 2026-05-07

> HuahuoAssistant.vue 构建语法错误修复

#### Bug 修复

- **HuahuoAssistant.vue 构建失败**：`initLive2D` 函数存在不完整的嵌套 `try` 语句结构，外层 `try` 缺少对应的 `catch` 或 `finally` 子句，导致 Vue 编译器报错 "Missing catch or finally clause"。修复：移除外层多余的 `try`，保留内层 `try...catch` 用于捕获初始化错误（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）

#### 文档更新

- **README.md**：版本变更记录新增 v4.3.4；v4.3.3 移除"当前版本"标记


### v4.3.3 - 2026-05-04

> 全项目死代码大清理：删除未使用组件/常量/空函数/调试日志/未使用导入

#### 代码清理

- **删除 `Live2dWidget.vue`**：该组件已被 `HuahuoAssistant.vue` 完全替代，项目中无任何导入引用。删除文件（[Live2dWidget.vue](frontend/src/components/Live2dWidget.vue)——已删除）
- **删除 `useLive2d.js` 中 3 个死常量**：`META_LINE_PREFIXES`（14 项）、`META_LINE_KEYWORDS`（7 项）、`ANSWER_MARKERS`（7 项）三个数组常量定义后从未被任何代码引用，为旧的回答清洗逻辑残留（[useLive2d.js](frontend/src/composables/useLive2d.js)）
- **删除 `HuahuoAssistant.vue` 中 6 项死代码**：① 空函数 `startStreamMouthPulse()` ② 空函数 `stopStreamMouthPulse()` ③ 空函数 `startSpeechMouthPulse()` ④ 空函数 `stopSpeechMouthPulse()`（v4.3.2 中改为空函数，现直接删除定义和所有调用点）；⑤ 未使用变量 `speechPulseInterval` ⑥ 未使用变量 `streamMouthPulseId`（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **删除 `VoiceChat.vue` 中 3 项口型脉冲死代码**：① 函数 `startSpeechMouthPulse()` ② 函数 `stopSpeechMouthPulse()` ③ 变量 `speechPulseInterval`。v4.3.2 将 Live2D 语音钩子改为空操作后，`notifyLive2dHook('onSpeechPulse', ...)` 不再生效，口型正弦波驱动完全废弃。删除函数定义、变量声明、以及 `utterance.onstart/onend/onerror` 和 `onBeforeUnmount` 中的全部调用点（[VoiceChat.vue](frontend/src/components/VoiceChat.vue)）
- **删除 3 处调试日志**：`console.log('[Live2D] initWidget found...')`（HuahuoAssistant.vue）、`console.log('[CreateProject] Submitting data:...')`（projects/create.vue）、`console.log('[AgentPanel] fetchProjects got...')`（ai-assistant/AgentPanel.vue）
- **删除 `HuahuoAssistant.vue` 中未使用导入 `Rank`**：从 `@element-plus/icons-vue` 导入但模板/脚本均未使用

#### 文档更新

- **README.md**：项目结构中移除 `Live2dWidget.vue` 条目；版本变更记录新增 v4.3.3；v4.3.2 移除"当前版本"标记


### v4.3.2 - 2026-05-04

> 浏览器兼容性统一（Firefox 滚动条）+ 口型动画系统全量禁用（移除诡异眼部动画）+ 关键字表情切换恢复（仅 onDelta 关键词驱动）

#### Bug 修复

- **Firefox 浏览器兼容性修复**：`-webkit-scrollbar` 伪元素在 Firefox 中无效，导致 `.expression-panel` 和 `.chat-messages` 滚动条样式丢失。修复：新增 Firefox 标准属性 `scrollbar-width: thin` 和 `scrollbar-color: rgba(6, 182, 212, 0.3) transparent`，与 Chrome 保持视觉一致（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Live2D 朗读时眼部异常一开一合**：三重根因叠加——① `onStreamStart` 和 `onSpeechStart` 强制设置 `setBaseExpression('07 星星眼')`，每次流式对话/语音朗读开始时将眼睛切换为星星眼；② `startStreamMouthPulse` / `startSpeechMouthPulse` 以正弦波驱动 `ParamMouthOpenY`（幅度 0.3-0.8，60-80ms 间隔），但模型不具备口型素材，参数值泄漏到眼部参数导致眼睛不自然开合；③ `onStreamEnd` 和 `onSpeechEnd` 强制重置为 `setBaseExpression('06 0.0')`，与入场时的星星眼形成反复切换。修复：全量禁用口型脉冲函数（改为空函数）；移除 monkey-patch `core.update` 中 `__applySpeechStateToCore` 调用；移除流式/语音开始结束的强制表情设置（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）

#### 功能修改

- **关键字驱动表情切换恢复**：`onDelta` 钩子恢复情绪关键词检测逻辑，AI 流式输出时根据文本内容自动匹配表情——开心/高兴/棒 →「02 脸红爱心」、生气/愤怒 →「03 生气」、难过/伤心 →「08 流泪」、晕/困惑 →「04 晕」、惊讶/震惊 →「07 星星眼」。不再在流式开始/结束时强制切换表情，仅通过文本关键词自然触发（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)、[useLive2d.js](frontend/src/composables/useLive2d.js)）

#### 文档更新

- **README.md**：版本变更记录新增 v4.3.2；v4.3.1 移除"当前版本"标记

***


### v4.3.1 - 2026-05-04

> Live2D 拖拽按钮彻底修复（坐标系统 + 事件冒泡）+ Chrome 跳动根因修复（残留 CSS + 异步时序）+ MCP 浏览器自动化回归验证

#### Bug 修复

- **Live2D 拖拽按钮点击后消失（第二轮彻底修复）**：三重根因——① `applyModelPosition()` 和 `restorePos()` 将视口坐标的 `left`/`top` 写入拖拽按钮（`#waifu` 子元素，`position: absolute`），导致按钮定位到视口外；② 按钮 click 事件冒泡到 `#waifu` 触发 `openPanel()` → 添加 `panel-open` class → 按钮被隐藏；③ 第 ① 点导致按钮仅在 CSS 默认位置短暂可见，一点击就被冒泡隐藏。修复：完全移除 JS 对拖拽按钮的手动定位（按钮作为 `#waifu` 子元素自动跟随）；为按钮添加 `stopPropagation()` 阻止事件冒泡（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Chrome Live2D 滑入后跳动（第二轮根因修复）**：三重根因——① `onMounted()` 中 `setTimeout(restorePos, 2000)` 在入场动画结束后 2 秒强制将 waifu 跳回保存位置；② 残留 CSS 规则 `#wafu, #waifu { transform: translateY(320px); opacity: 0; transition: ... }` 永久生效——JS 设 `transform: ''` 后 CSS cascade 的 `translateY(320px)` 重新接管，导致 waifu 瞬间偏移；③ `initWidget` 内部的 `r()` 函数异步添加 `waifu-active` class，重新触发 CSS `bottom: 0` 3 秒过渡，与 JS 动画竞争。修复：移除 `setTimeout`，将位置恢复到入场动画之前执行；移除 `#wafu, #waifu` 规则中残留的 `opacity` / `transform` / `transition` 声明；添加 `MutationObserver` 监听 `waifu-active` class，确保 JS inline 样式在所有 CSS 过渡之后作为最终样式生效（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Chrome 跳动辅助修复**：`applyModelPosition()` 中 `bottom: 0` 设置增加条件判断——当保存位置使用 `top` 定位时跳过 `bottom: 0`，避免 `top`/`bottom` 同时生效导致布局冲突（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）

#### 安全与稳定性

- **MCP 浏览器自动化回归验证**：使用 chrome-devtools MCP 工具在真实浏览器环境中完成 6 项验证——初始加载位置正确 ✓ / 拖拽按钮可见 ✓ / 拖拽保存位置成功 ✓ / 刷新后位置恢复无跳动 ✓ / 面板开关按钮显隐正确 ✓ / 按钮点击不触发面板打开 ✓

#### 文档更新

- **README.md**：版本变更记录新增 v4.3.1；v4.3.0 移除"当前版本"标记

***


### v4.3.0 - 2026-05-04

> 品牌升级：项目全面更名为「火花智创 SparkAI Innovate」+ 动态 Logo 组件 + Live2D 加载修复 + 项目名称统一替换

#### 新增功能

- **动态品牌 Logo 组件**（`SparkLogo.vue`）：全新品牌视觉组件，采用彩色渐变文字（红-橙-黄-粉-紫-蓝六色流动渐变）+ 底部粒子浮动效果 + 奖杯呼吸光晕，悬停时加速闪烁，呈现烟花般的视觉氛围。支持 small / normal / large 三种尺寸，应用于顶部导航、侧边栏、登录页（[SparkLogo.vue](frontend/src/components/SparkLogo.vue)）
- **品牌升级**：项目中文名从「高校创新创业竞赛服务平台」更名为「火花智创」，英文名从「University Innovation and Entrepreneurship Competition Service Platform」更名为「SparkAI Innovate」，GitHub 仓库同步更名为 `sparkai-innovate`

#### 功能修改

- **首页标题动态效果**：PortalHome.vue Banner 标题「火花智创 SparkAI」采用彩色渐变 + 发光动画，与品牌 Logo 视觉统一（[PortalHome.vue](frontend/src/views/portal/PortalHome.vue)）
- **项目名全量替换**：前端所有页面（login / register / MainLayout / PortalHome / guide.js / router / ai-assistant 等）和后端所有 AI Prompt（ai_service.py / ai_prompt_service.py / ai.py / volc_realtime_bridge.py）中的旧项目名称全部替换为「火花智创 SparkAI Innovate」
- **README.md & AI-Agent功能分析报告.md 迁移**：两份文档从 `innovation-competition-platform/` 子目录移至项目根目录 `my-keshe/`，并相互添加引用链接

#### Bug 修复

- **Live2D 加载失败**：`Live2dWidget.vue` 中 index.js 和 index2.js 脚本缺少 `onload` 回调，导致初始化时序错误。修复：为两个脚本添加 `onload = checkAndResolve`，确保库加载完成后再调用 `initWidget`（[Live2dWidget.vue](frontend/src/components/Live2dWidget.vue)）
- **SparkLogo 悬停文字消失**：原逐字动画与悬停动画冲突，导致鼠标悬停时文字消失。修复：移除逐字浮现动画，改为整体渐变 + 粒子效果，悬停仅增强发光强度（[SparkLogo.vue](frontend/src/components/SparkLogo.vue)）
- **侧边栏 Logo 文字截断**：原 Logo 文字宽度超出侧边栏导致显示不全。修复：SparkLogo 组件添加 `white-space: nowrap` 和 `flex-shrink: 0`，确保文字完整显示
- **Live2D 拖拽按钮 Firefox 不显示**：`panel-resize-handle` 使用 CSS 伪元素 `::before` + `border` 画 L 形图标，Firefox 对伪元素渲染有兼容性问题。修复：改用内联 SVG 图标（三条斜线），所有浏览器兼容（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Live2D 形象拖拽按钮 Firefox 不显示**：拖拽按钮用 `position: fixed` 独立定位在 `<teleport>` 内，Firefox 中 `backdrop-filter` + `fixed` + `teleport` 堆叠上下文冲突导致不渲染。修复：改为 JS 动态创建 `createElement` 并 `appendChild` 到 `#waifu` 内部，CSS 改为 `position: absolute; right: -16px; top: 50%` 相对于 waifu 定位，移除 `backdrop-filter`（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Live2D 拖拽按钮点击后消失**：按钮改为动态创建后，Vue 模板的 `:class="{ 'panel-open': panelOpen }"` 绑定失效。修复：添加 `watch(panelOpen)` 手动切换动态元素的 `panel-open` class（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Chrome Live2D 滑入后跳动**：`waifu.css` 设置了 `#waifu { bottom: -500px; transition: bottom 3s; }`，`initWidget` 模型加载后添加 `waifu-active` → `bottom: 0` 触发 3 秒过渡，与我们的 `transform` 动画竞争导致跳动。修复：JS 显式设置 inline `bottom: 0`；在 `transitionend` 后清除我们的过渡并重置 `transform`，确保后续只有 `left`/`top` 过渡生效（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Live2D 点击形象切换表情无效**：`openPanel()` 中 `notifyLive2dHook('onStreamEnd')` 触发 `setBaseExpression('06 0.0')` 覆盖随机表情。修复：从 `openPanel()` 移除该调用（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **PortalHome handleResize TypeError**：`flowAnimFrames` 混存函数和 `requestAnimationFrame` 返回的数字 ID，`handleResize()` 遍历时调用数字为函数导致 `f is not a function`。修复：添加 `typeof f === 'function'` 类型检查（[PortalHome.vue](frontend/src/views/portal/PortalHome.vue)）
- **Live2D lappmodel.js `_modelSetting is null`**：模型未加载完时鼠标移动触发 `hitTest`。修复：初始 `pointer-events: none`，动画结束后恢复（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **AI 助手窗口只能改变宽度不能改变高度**：`updatePanelStyle()` 中设置的是 `maxHeight` 而非 `height`，导致高度无法调整。修复：改为设置 `height` 属性，宽度和高度均可自由调整（320-800px 宽，400-900px 高）（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）

#### 文档更新

- **README.md**：项目标题更新为「火花智创 SparkAI Innovate」；新增 GitHub 仓库链接；新增品牌视觉描述；AI-Agent功能分析报告.md 引用链接更新；版本变更记录新增 v4.3.0
- **AI-Agent功能分析报告.md**：标题更新为「火花智创 SparkAI Innovate — AI 智能与 Agent 功能分析报告」；新增文档定位说明（README.md 的技术补充文档）；图片路径更新为 `innovation-competition-platform/docs_and_images/`

***


### v4.2.0 - 2026-05-04

> 评委评审记录实现 + Live2D 重登录修复 + 口型动画修复 + AI 助手窗口可调整大小 + 管理员页面 API 对接 + 引导系统更新

#### 新增功能

- **评委评审记录页面**：实现 `history.vue` 完整功能，调用 `getMyReviews` API 展示评审记录列表，包含各维度评分条形图、总分标签、评审意见、评审时间，支持跳转项目详情（[history.vue](frontend/src/views/reviews/history.vue)）
- **AI 助手窗口拖拽调整大小**：HuahuoAssistant 面板左上角新增 resize 手柄，支持拖拽调整宽度（320-800px）和高度（400-900px），尺寸持久化到 localStorage（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **管理员用户管理 API 对接**：后端新增 `POST /users/`（创建用户）、`PUT /users/<id>`（更新用户）、`POST /users/<id>/toggle-status`（切换状态）、`DELETE /users/<id>`（删除用户）4 个端点；前端 `users.vue` 从硬编码数据改为调用真实 API（[user.py](backend/routes/user.py)、[users.vue](frontend/src/views/admin/users.vue)、[user.js](frontend/src/api/user.js)）
- **管理员项目管理 API 对接**：前端 `projects.vue` 从硬编码数据改为调用 `getProjects` / `deleteProject` 真实 API（[projects.vue](frontend/src/views/admin/projects.vue)）
- **管理员评审管理页面**：后端新增 `GET /reviews/all` 端点；前端 `reviews.vue` 从空页面改为完整评审管理页面，展示评审统计、评审列表、评委筛选（[review.py](backend/routes/review.py)、[reviews.vue](frontend/src/views/admin/reviews.vue)）
- **公开统计 API**：后端新增 `GET /dashboard/public-stats` 端点，仅需 JWT 认证不限角色，返回平台首页所需统计数据（[dashboard.py](backend/routes/dashboard.py)）

#### Bug 修复

- **登录演示账号弹窗"权限不足，需要角色: admin"**：PortalHome.vue 调用 `getDashboardStats()`（需 admin 权限）导致非 admin 用户登录时 403 弹窗。修复：新增 `/dashboard/public-stats` 公开端点，PortalHome 改用 `getPublicStats()`（[dashboard.py](backend/routes/dashboard.py)、[PortalHome.vue](frontend/src/views/portal/PortalHome.vue)）
- **退出后切换角色再登录 Live2D 不加载**：`onBeforeUnmount` 仅隐藏 `#waifu` DOM（display:none），未移除 DOM 和清理全局状态，导致重新挂载时 `initWidget` 创建重复 `#waifu` 元素。修复：`onBeforeUnmount` 彻底移除 DOM 元素、清理所有全局变量（`__live2dWidgetModelManager`、`initWidget` 等）、清理 localStorage；`initLive2D` 启动前先清理残留 DOM（[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）
- **Live2D 口型动画无法触发**：三重问题叠加——① `火花.model3.json` 中 LipSync 组 Ids 为空（SDK 标准 LipSync 不工作）；② `onDelta` 口型计算值过小（textLen/20 对 1-3 字符 delta 仅 0.05-0.15）；③ 流式输出时无持续口型脉冲。修复：① model3.json LipSync Ids 加入 `ParamMouthOpenY`；② 新增 `startStreamMouthPulse` / `stopStreamMouthPulse` 函数，流式输出时以 60ms 间隔正弦波驱动口型（幅度 0.3-0.8）；③ onDelta 仅负责情绪检测和表情切换（[火花.model3.json](frontend/public/live2d/huahuo/火花.model3.json)、[HuahuoAssistant.vue](frontend/src/components/HuahuoAssistant.vue)）

#### 功能修改

- **引导系统更新**：4 种角色引导步骤全面更新——学生步骤新增 AI 模拟答辩/项目创意生成/智能引航描述，教师步骤新增批量审核/智能反馈描述，评委步骤新增评审意见草稿/评分一致性检查描述，管理员步骤从"5 大 AI 能力"更新为"12 大 AI 能力"；所有角色新增语音交互、表情联动、窗口拖拽调整大小等新功能描述（[guide.js](frontend/src/stores/guide.js)）

***


### v4.1.1 - 2026-05-03

> AI 智能体前后端参数校验一致性修复 + Live2D 表情自动切换 + 权限矩阵/API 文档补全

#### 功能修改

- **Live2D 表情自动切换**：火花形象加载完成后，每 10 秒自动随机切换表情（AI 流式输出或朗读期间跳过，避免打断表情联动）；点击火花形象时也会随机切换一次表情（[HuahuoAssistant.vue](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/components/HuahuoAssistant.vue)）

#### Bug 修复

- **模拟答辩 question\_type 前后端不一致**：前端传 `challenge`，后端校验仅允许 `tough`，导致选择"挑战"类型时返回 400 错误。修复：前端 `AgentPanel.vue` 将 `label="challenge"` 改为 `label="tough"`（[AgentPanel.vue:158](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/views/ai-assistant/AgentPanel.vue#L158)）
- **智能反馈 feedback\_type 前后端不一致**：前端传 `encourage`/`question`，后端校验仅允许 `approve`/`reject`，导致选择"鼓励指导"/"提问引导"时返回 400 错误。修复：前端选项改为"建议通过"（`approve`）和"建议驳回"（`reject`）（[AgentPanel.vue:164-165](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/frontend/src/views/ai-assistant/AgentPanel.vue#L164)）
- **路演稿 duration 前后端不一致**：前端允许 8 分钟，后端校验仅允许 3/5，导致选择 8 分钟时返回 400 错误。修复：后端 `agent.py` 校验扩展为 `(3, 5, 8)`，`ai_prompt_service.py` 新增 8 分钟对应约 2200 字目标（[agent.py:368](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/backend/routes/agent.py#L368)）
- **路演稿 style 前后端不一致**：前端传 `story`，后端校验仅允许 `formal`/`passionate`/`concise`，导致选择"故事"风格时返回 400 错误。修复：后端校验新增 `story`，`ai_prompt_service.py` 新增故事叙述风格描述（[agent.py:369](file:///e:/软件工程课设/my-keshe/innovation-competition-platform/backend/routes/agent.py#L369)）

#### 文档更新

- **AI 智能体权限矩阵补全**：从 5 行扩展为 12 行，新增项目创意生成/模拟答辩/批量审核/智能反馈/评审草稿/评分检查/智能引航 7 项能力的权限说明
- **AI 智能体 API 文档补全**：从 8 个端点扩展为 14 个，新增 navigate/project-idea/mock-defense/batch-review/smart-feedback/review-draft/score-check/capabilities 端点文档
- **AI 项目智能体特色功能描述更新**：从"5 大 AI 能力"更新为"12 大 AI 能力"

***


### v4.1.0 - 2026-05-03

> 集成通义千问 qwen-plus 大模型 + 统一对话路由 + 智能导航 + 深色主题适配 + AgentPanel 交互优化

#### 新增功能

- **通义千问 qwen-plus 大模型集成**：通过 LangChain ChatOpenAI 兼容接口接入通义千问 qwen-plus 模型（`GLM_API_KEY` / `GLM_BASE_URL` / `GLM_MODEL` 配置项），替代火山方舟 SDK 作为主要对话模型，支持多轮对话 / 意图识别 / 角色感知
- **统一对话路由**（`unified_chat`）：`ai_service.py` 新增统一对话入口，根据用户消息自动识别意图（导航 / 通用对话 / 智能体能力），分发到对应处理逻辑
- **智能导航功能**（`smart_navigate`）：`ai_prompt_service.py` 新增智能导航能力，用户输入模糊指令（如"我想报名比赛""帮我看看项目"），AI 自动识别意图并返回路由跳转建议，前端自动执行页面跳转
- **意图检测**（`detect_intent`）：`ai_prompt_service.py` 新增意图检测函数，支持导航意图 / 智能体意图 / 通用对话意图三类识别
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
- **AI Prompt 服务**（`ai_prompt_service.py`）：手工拼接 Prompt + 调用 LLM 的 RAG 问答 / BP 体检 / 路演稿 / 评审辅助 / 竞赛推荐 5 大能力
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

### v2.0.1 - 2026-06-30

#### Bug 修复

- **Live2D 表情反复闪烁横跳修复**：深入修复在特定交互场景下（如“07 星星眼”及高频情感分析切换时），会导致虚拟形象表情从目标状态反复回退到默认 “0.0” 的异常现象。增加了状态追踪与多级表情锁定，消除了无谓的重置调用。

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
- `index.html`：页面标题从 "frontend" 改为 "火花智创 SparkAI Innovate"
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

> 基础高校创新创业竞赛服务平台，AI 功能为 Mock 实现

- 竞赛发现、报名、项目创建、团队管理、材料上传、任务进度、评审打分
- 四种角色（学生 / 指导老师 / 评委 / 管理员）
- 竞赛广场、项目工作室、训练营、在线课程、产业命题
- AI 分析工具（Mock 模板实现）
- 全局引导系统
- 双模式布局（平台页无侧边栏 / 工作台有侧边栏）

***

## 许可证

MIT License
