# Live2D + LangChain Agent 集成方案（最终修订版）

> 适用项目：高校创新创业竞赛服务平台  
> 方案用途：指导 AI Coder 在现有系统中安全引入 LangChain Agent，避免与现有 Live2D「火花」AI 助手重复。  
> Python 环境要求：后端所有 Python 命令一律使用 `newyolo` conda 环境。  
> 阶段输出要求：每个阶段完成后，必须将阶段总结写入 `E:\LEAR-CODE-NEW\软件工程\my-keshe\keshe\各自阶段输出.md`。  
> README 更新要求：任务完成后更新 `E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\README.md`，且整篇 README 的“现有功能、接口、项目结构、数据库模型、启动说明、当前状态、版本更迭”必须和最新代码一致，不能只在版本更迭中写新功能而正文仍停留在旧版本。

---

## 一、方案背景

当前系统已经存在全局 Live2D 虚拟形象「火花」作为主要 AI 交互入口，`HuahuoAssistant.vue` 已集成：

- Live2D 形象展示与拖拽
- AI 对话
- SSE 流式回复
- AI 分析工具
- 语音识别
- TTS 朗读
- 表情联动
- 口型动画
- 全局浮动面板

因此，本次引入 LangChain Agent 的核心目标不是再造一个新的 AI 助手，而是为「火花」增加一组专业工具能力：

- AI 材料问答
- AI 商业计划书体检
- AI 路演稿生成
- AI 评审辅助
- 智能竞赛推荐

最终对用户的表达应是：

> 火花新增了“项目智能体能力”。

而不是：

> 系统新增了另一个 AI Agent 助手。

---

## 二、现状排查结果

### 2.1 路由状态

| 位置 | `/ai-assistant` 路由 | 说明 |
|---|---|---|
| `router/index.js` | 不存在或已移除 | 现有系统主入口应为 `HuahuoAssistant.vue` |
| `PortalHome.vue` | 可能残留 `/ai-assistant` | 点击可能 404，需要修复 |
| `judge.vue` | 可能残留 `$router.push('/ai-assistant')` | 点击可能 404，需要修复 |
| `teacher.vue` | 可能残留 `$router.push('/ai-assistant')` | 点击可能 404，需要修复 |

### 2.2 AI 入口现状

| 入口 | 类型 | 功能 | 处理策略 |
|---|---|---|---|
| `HuahuoAssistant.vue` | 全局浮动组件 | Live2D + 对话 + AI 分析 + 语音 + 表情 | 保留为唯一主要 AI 入口 |
| `ai-assistant/index.vue` | 旧页面 / 孤儿页面 | 双 Tab：分析工具 + 对话 | 可恢复为备用入口，但不能作为主入口 |
| `VoiceChat.vue` | 语音面板组件 | 语音对话 | 保留，不重写 |
| `/api/ai/*` | 后端 AI 蓝图 | 对话、SSE、ASR、TTS、分析、表情、健康 | 保留，不重写 |

---

## 三、核心原则：12 条红线

| # | 原则 | 说明 |
|---|---|---|
| 1 | LangChain Agent 不替代 HuahuoAssistant | 火花仍是前端唯一主要 AI 入口 |
| 2 | 不新增第二套 AI 助手体系 | 不允许出现多个功能重合的 AI 助手入口 |
| 3 | `/api/ai/*` 保留不动 | 普通对话、语音、TTS、ASR、原有 AI 分析全部保留 |
| 4 | `/api/agent/*` 只做专项能力 | 材料问答、BP 体检、路演稿、评审辅助、竞赛推荐 |
| 5 | AgentPanel 是子组件 | 可以被 HuahuoAssistant 和备用页复用，但不能自成一套助手 |
| 6 | `/ai-assistant` 只能作为备用入口 | 不放入主菜单、Portal 卡片、侧边栏，不成为主入口 |
| 7 | 复用 Live2D 表情联动和朗读 | Agent 结果可触发表情和朗读，但不重写 Live2D 逻辑 |
| 8 | 评审辅助不自动填分 | 只给参考建议，不替代评委人工评分 |
| 9 | 评审辅助不返回具体建议分数 | 不返回 `suggested_score`、`suggested: 82` 等字段 |
| 10 | 不破坏现有对话/语音/SSE/Live2D | 所有现有功能必须零影响 |
| 11 | Markdown 渲染必须安全处理 | `marked.parse()` 后必须使用 DOMPurify 等方式过滤 |
| 12 | 每阶段必须写阶段输出 | 写入 `E:\LEAR-CODE-NEW\软件工程\my-keshe\keshe\各自阶段输出.md` |

---

## 四、目标功能边界

### 4.1 保留的现有 AI 能力

`/api/ai/*` 与 `HuahuoAssistant.vue` 原有能力保持不变：

- 普通 AI 对话
- SSE 流式回复
- 语音识别 ASR
- TTS 语音合成
- 实时语音对话
- 项目简介生成
- 商业计划书建议
- 风险分析
- 表情列表
- Live2D 模型信息
- AI 健康检查

### 4.2 新增 LangChain Agent 专项能力

`/api/agent/*` 只负责：

- `material-qa`：AI 材料问答
- `bp-check`：AI 商业计划书体检
- `roadshow`：AI 路演稿生成
- `review-assist`：AI 评审辅助
- `competition-recommend`：智能竞赛推荐
- `index-materials`：索引项目材料 / 报名材料
- `tasks`：智能体任务记录查询

---

## 五、整体架构

### 5.1 前端入口层级

```text
用户交互层
│
├── HuahuoAssistant.vue（唯一主要 AI 入口，全局浮动）
│   ├── mode === 'chat'        → 对话模式，现有，不动
│   ├── mode === 'analysis'    → AI 分析模式，现有，不动
│   └── mode === 'agent'       → AI 智能体模式，新增
│       └── AgentPanel.vue     → 5 个专项能力面板，子组件
│
├── /ai-assistant 页面（备用入口，不作为主入口）
│   ├── Tab 1: AI 分析工具，现有
│   ├── Tab 2: AI 对话，现有
│   └── Tab 3: AI 智能体，复用 AgentPanel.vue
│
└── 其他页面快捷入口
    ├── PortalHome.vue → 触发 open-huahuo-agent 全局事件
    ├── 项目详情页 → 可触发 open-huahuo-agent 并传 projectId
    ├── 项目材料页 → 可触发 open-huahuo-agent 并传 capability/material 信息
    ├── judge.vue / 评审详情页 → 可触发 review_assist
    └── teacher.vue → 可触发 review_assist 或 material_qa
```

### 5.2 后端 API 分层

```text
/api/ai/*
负责现有通用 AI：
- chat
- chat/stream
- voice/chat/stream
- asr
- tts/synthesize
- project-summary
- business-plan-advice
- risk-analysis
- expressions
- model-info
- health

/api/agent/*
负责新增 LangChain Agent：
- material-qa
- bp-check
- roadshow
- review-assist
- competition-recommend
- index-materials
- tasks
- tasks/<id>
```

### 5.3 数据流

```text
用户打开火花 → 切换到 AI 智能体模式
    ↓
AgentPanel.vue 渲染能力卡片
    ↓
用户选择能力并填写参数
    ↓
调用 /api/agent/*
    ↓
后端 document_parser.py 解析材料
    ↓
vector_store.py / BM25 降级检索材料上下文
    ↓
langchain_service.py 组织 Prompt 并调用 LLM
    ↓
返回 Markdown 结果 + 来源 + 任务记录
    ↓
AgentPanel 展示结果
    ↓
结果触发 Live2D 表情联动、复制、朗读
```

---

## 六、后端设计

### 6.1 新增文件

```text
backend/
├── services/
│   ├── langchain_service.py        # LangChain 核心服务
│   ├── document_parser.py          # 文档解析服务
│   └── vector_store.py             # FAISS / BM25 检索服务
├── routes/
│   └── agent.py                    # /api/agent 蓝图
└── models/
    ├── agent_task.py               # 智能体任务记录
    └── agent_material_index.py     # 可选：材料索引状态记录
```

### 6.2 依赖建议

后端新增或确认依赖：

```text
langchain
langchain-core
langchain-community
langchain-openai
langchain-text-splitters
faiss-cpu
rank-bm25
python-docx
python-pptx
pypdf 或 PyPDF2
```

注意：

1. 所有 Python 命令一律在 `newyolo` conda 环境中执行。
2. 如果 `faiss-cpu` 在 Windows 环境安装失败，不能阻塞主功能，必须降级到 BM25 / 关键词检索。
3. 不允许为了本地兜底强制下载 HuggingFace 大模型，避免环境不稳定。

### 6.3 Python 环境要求

后端相关命令必须使用：

```bash
conda activate newyolo
```

或在脚本中明确使用：

```text
D:\TOOLS\anaconda\envs\newyolo\python.exe
```

典型命令：

```bash
conda activate newyolo
cd E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\backend
pip install -r requirements.txt
flask db migrate -m "add langchain agent models"
flask db upgrade
python app.py
```

---

## 七、数据库模型设计

### 7.1 AgentTask

用于记录每次智能体调用。

```python
class AgentTask(db.Model):
    __tablename__ = 'agent_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('competition_registrations.id'), nullable=True)
    capability = db.Column(db.String(50), nullable=False)
    input_params = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True)
```

`capability` 可选值：

```text
material_qa
bp_check
roadshow
review_assist
competition_recommend
index_materials
```

### 7.2 AgentMaterialIndex（推荐新增）

用于记录材料是否已索引、索引是否过期、索引路径在哪里。

```python
class AgentMaterialIndex(db.Model):
    __tablename__ = 'agent_material_indexes'

    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(30), nullable=False)  # project_file / registration_material
    source_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, nullable=True)
    registration_id = db.Column(db.Integer, nullable=True)
    file_hash = db.Column(db.String(64), nullable=True)
    index_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending / indexed / failed / outdated
    error_message = db.Column(db.Text, nullable=True)
    indexed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
```

### 7.3 不推荐把所有 chunk 都强制入库

第一版可以优先将 FAISS/BM25 索引落到本地目录，并用 `AgentMaterialIndex` 记录索引状态。避免把大量 chunk 文本写入 MySQL 导致数据库膨胀。

---

## 八、文档解析与索引

### 8.1 支持格式

| 格式 | 支持 | 说明 |
|---|---|---|
| `.txt` | 支持 | 直接读取文本 |
| `.pdf` | 支持 | 使用 `pypdf` 或 `PyPDF2` 提取文本 |
| `.docx` | 支持 | 使用 `python-docx` 提取段落文本 |
| `.pptx` | 支持 | 使用 `python-pptx` 提取幻灯片文本 |
| `.doc` | 暂不支持 | 提示转换为 `.docx` |
| `.ppt` | 暂不支持 | 提示转换为 `.pptx` |
| 图片 | 暂不支持 | 可后续接 OCR |
| 视频 | 暂不支持 | 可后续接 ASR |
| 压缩包 | 暂不支持 | 提示解压后上传内部文档 |

### 8.2 source_type

`index-materials` 必须支持两类材料：

```json
{
  "source_type": "project",
  "project_id": 1,
  "force_reindex": false
}
```

```json
{
  "source_type": "registration",
  "registration_id": 3,
  "force_reindex": false
}
```

### 8.3 索引空间

不能只按项目 ID 隔离。

必须支持：

```text
backend/vector_stores/project_<id>/
backend/vector_stores/registration_<id>/
```

### 8.4 降级策略

| 场景 | 处理 |
|---|---|
| 单个文件解析失败 | 跳过该文件，写入 `skipped_details` |
| 文件类型不支持 | 返回友好提示，不报 500 |
| Embedding 不可用 | 降级 BM25 或关键词检索 |
| FAISS 不可用 | 降级 BM25 或关键词检索 |
| LLM 调用失败 | 返回模板化结果，并标注“AI 服务不可用，已使用模板分析” |
| 没有可解析材料 | 基于项目基础信息生成简版结果，并提示“材料不足” |

---

## 九、后端 API 设计

### 9.1 接口列表

| 接口 | 方法 | 权限 | 说明 |
|---|---|---|---|
| `/api/agent/index-materials` | POST | JWT + 材料访问权限 | 索引项目或报名材料 |
| `/api/agent/material-qa` | POST | JWT + 项目/报名访问权限 | AI 材料问答 |
| `/api/agent/bp-check` | POST | JWT + 项目/报名访问权限 | 商业计划书体检 |
| `/api/agent/roadshow` | POST | student/teacher/admin | 路演稿生成 |
| `/api/agent/review-assist` | POST | teacher/judge/admin | 评审辅助 |
| `/api/agent/competition-recommend` | POST | student/admin | 智能竞赛推荐 |
| `/api/agent/tasks` | GET | JWT | 当前用户任务记录 |
| `/api/agent/tasks/<id>` | GET | JWT | 任务详情 |

### 9.2 统一响应格式

所有新增接口必须遵守现有格式：

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {}
}
```

错误响应：

```json
{
  "code": 400,
  "message": "参数缺失：project_id",
  "data": null
}
```

### 9.3 AI 评审辅助返回格式

禁止返回具体分数。

正确格式：

```json
{
  "code": 200,
  "message": "生成成功",
  "data": {
    "summary": "项目整体摘要...",
    "highlights": ["创新亮点1", "创新亮点2"],
    "risks": {
      "innovation": "创新性方面的关注点...",
      "feasibility": "可行性风险...",
      "market": "市场风险...",
      "team": "团队风险...",
      "business": "商业模式风险..."
    },
    "questions": ["建议追问问题1", "建议追问问题2"],
    "dimension_references": {
      "innovation": "评审时可关注项目是否有技术或模式差异化。",
      "feasibility": "评审时可关注实施路径、资源条件和时间计划。"
    },
    "disclaimer": "AI 结果仅供评审参考，最终评分由评委人工决定。",
    "task_id": 1
  }
}
```

错误格式示例，不允许：

```json
{
  "scores": {
    "innovation": {"suggested": 82}
  }
}
```

---

## 十、权限设计

| 能力 | student | teacher | judge | admin |
|---|---|---|---|---|
| AI 材料问答 | 自己负责/参与项目、自己的报名材料 | 自己指导项目 | 自己可评审项目 | 全部 |
| 商业计划书体检 | 自己负责/参与项目、自己的报名材料 | 自己指导项目 | 自己可评审项目 | 全部 |
| 路演稿生成 | 自己负责/参与项目 | 自己指导项目 | 不可用 | 全部 |
| AI 评审辅助 | 不可用 | 自己指导项目 | 自己可评审项目 | 全部 |
| 智能竞赛推荐 | 可用 | 默认不可用 | 默认不可用 | 可用 |
| 材料索引 | 有访问权限即可 | 有访问权限即可 | 有访问权限即可 | 全部 |

注意：

1. 前端隐藏按钮不是权限控制，后端必须再次校验。
2. `judge` 可以索引自己可评审项目的材料，否则 AI 评审辅助无法基于材料工作。
3. `admin` 需要具备测试和演示能力。

---

## 十一、前端集成设计

### 11.1 HuahuoAssistant.vue 新增 mode

新增：

```text
mode === 'agent'
```

保留：

```text
mode === 'chat'
mode === 'analysis'
```

### 11.2 顶部按钮

现有按钮：

```text
[MagicStick] [表情] [收起]
```

新增后：

```text
[Agent] [MagicStick] [表情] [收起]
```

### 11.3 AgentPanel 作为子组件

```vue
<AgentPanel
  :user-role="userRole"
  :initial-context="agentInitialContext"
  compact
  @result="onAgentResult"
  @speak="onAgentSpeak"
/>
```

### 11.4 open-huahuo-agent 全局事件

必须支持 `detail` 参数。

示例：

```js
window.dispatchEvent(new CustomEvent('open-huahuo-agent', {
  detail: {
    capability: 'review_assist',
    projectId: project.id,
    registrationId: null,
    source: 'review_detail'
  }
}))
```

监听：

```js
function handleOpenHuahuoAgent(event) {
  panelOpen.value = true
  mode.value = 'agent'
  agentInitialContext.value = event.detail || {}
}

onMounted(() => {
  window.addEventListener('open-huahuo-agent', handleOpenHuahuoAgent)
})

onBeforeUnmount(() => {
  window.removeEventListener('open-huahuo-agent', handleOpenHuahuoAgent)
})
```

### 11.5 模式切换状态隔离

必须保证：

1. Agent 执行不影响 chat 消息列表。
2. Agent 朗读不覆盖正在流式输出的对话。
3. 切回 chat 后原会话仍保留。
4. 正在语音识别时进入 agent，要提示或停止识别。
5. Agent loading 时禁止重复点击执行按钮。
6. 切换模式不清空当前 Agent 结果，除非用户手动清空。

---

## 十二、AgentPanel.vue 设计

### 12.1 定位

- `AgentPanel.vue` 不是独立 AI 助手页面。
- 它是 `HuahuoAssistant.vue` 的子组件。
- 它也可被 `/ai-assistant` 备用页复用。
- 不包含 Live2D、语音、SSE 逻辑。
- 只负责参数输入、API 调用和结果展示。

### 12.2 Props & Events

```js
const props = defineProps({
  userRole: { type: String, default: 'student' },
  initialContext: { type: Object, default: () => ({}) },
  compact: { type: Boolean, default: false }
})

const emit = defineEmits(['result', 'speak'])
```

### 12.3 能力卡片

```js
const capabilities = computed(() => {
  const all = [
    { key: 'material_qa', name: 'AI 材料问答', roles: ['student', 'teacher', 'judge', 'admin'] },
    { key: 'bp_check', name: '商业计划书体检', roles: ['student', 'teacher', 'judge', 'admin'] },
    { key: 'roadshow', name: '路演稿生成', roles: ['student', 'teacher', 'admin'] },
    { key: 'review_assist', name: 'AI 评审辅助', roles: ['teacher', 'judge', 'admin'] },
    { key: 'competition_recommend', name: '智能竞赛推荐', roles: ['student', 'admin'] }
  ]
  return all.filter(c => c.roles.includes(props.userRole))
})
```

### 12.4 紧凑模式与完整模式

| 模式 | 使用位置 | UI 策略 |
|---|---|---|
| 紧凑模式 | HuahuoAssistant 内 | 小面板、内部滚动、简化布局 |
| 完整模式 | `/ai-assistant` 备用页 | 宽屏展示、更多历史记录、完整结果区 |

长结果处理：

1. 结果区域设置最大高度并内部滚动。
2. 提供“复制全文”。
3. 提供“朗读结果”。
4. 可选提供“在备用页查看完整结果”。

---

## 十三、Markdown 安全渲染

项目已有 AI 输出 Markdown 渲染需求，新增 Agent 结果也会返回 Markdown。

必须遵守：

1. 不允许直接 `v-html="marked(result)"`。
2. 必须统一封装安全渲染函数。
3. 推荐安装并使用 DOMPurify。

前端依赖：

```bash
npm install dompurify
```

示例：

```js
import { marked } from 'marked'
import DOMPurify from 'dompurify'

function renderSafeMarkdown(text) {
  return DOMPurify.sanitize(marked.parse(text || ''))
}
```

所有 Agent 结果展示必须使用：

```vue
<div class="agent-result" v-html="renderSafeMarkdown(resultText)"></div>
```

如果项目已有类似安全 Markdown 渲染工具，应复用，不要重复实现。

---

## 十四、残留链接修复

### 14.1 PortalHome.vue

不要再跳转 `/ai-assistant` 作为主入口。

改为：

```js
function openAgentFromPortal() {
  window.dispatchEvent(new CustomEvent('open-huahuo-agent', {
    detail: {
      capability: 'material_qa',
      source: 'portal'
    }
  }))
}
```

### 14.2 judge.vue / teacher.vue

```js
function openReviewAgent(projectId) {
  window.dispatchEvent(new CustomEvent('open-huahuo-agent', {
    detail: {
      capability: 'review_assist',
      projectId,
      source: 'review_dashboard'
    }
  }))
}
```

### 14.3 /ai-assistant 备用页

可以恢复路由，但必须满足：

1. 不放入主菜单。
2. 不放入 Portal 主入口卡片。
3. 不作为侧边栏入口。
4. 页面顶部显示：

```text
备用 AI 页面：推荐使用右下角火花助手。此页面用于调试和完整结果查看。
```

5. 所有智能体逻辑复用 `AgentPanel.vue`，不要重复写。

---

## 十五、Live2D 表情与朗读复用

### 15.1 Agent 结果触发表情

`AgentPanel.vue`：

```js
emit('result', resultText)
```

`HuahuoAssistant.vue`：

```js
function onAgentResult(text) {
  updateExpressionByText(text)
}
```

### 15.2 Agent 结果触发朗读

`AgentPanel.vue`：

```js
emit('speak', agentResult.value)
```

`HuahuoAssistant.vue`：

```js
function onAgentSpeak(text) {
  if (isStreaming.value) {
    ElMessage.warning('当前正在生成对话回复，请稍后再朗读智能体结果')
    return
  }
  currentReplyText.value = text
  toggleSpeech()
}
```

### 15.3 不重写的部分

| 功能 | 处理 |
|---|---|
| Live2D 加载 | 不改 |
| 表情控制系统 | 不改 |
| 对话模式 | 不改 |
| AI 分析模式 | 不改 |
| 语音识别 | 不改 |
| 语音朗读 | 复用现有逻辑 |
| SSE 流式对话 | 不改 |
| 拖拽逻辑 | 不改 |
| VoiceChat | 不改 |

---

## 十六、MCP 调试验收

任务完成后必须使用 Chrome DevTools MCP 调试。

如果当前 AI Coder 环境没有 MCP，必须明确写：

```text
Chrome DevTools MCP 不可用，无法完成本步骤。
```

不能假装已调试。

### 16.1 MCP 必测流程

1. 打开 `http://localhost:5173`。
2. 使用 `student1 / student123` 登录。
3. 确认登录后进入 `/portal`。
4. 点击 Portal 的 AI 相关入口，确认打开火花 Agent 模式。
5. 检查 `chat / analysis / agent` 三种模式切换无报错。
6. 在 Agent 模式选择项目。
7. 调用材料索引。
8. 调用材料问答。
9. 调用商业计划书体检。
10. 调用路演稿生成。
11. 调用智能竞赛推荐。
12. 点击推荐竞赛，确认跳转竞赛详情。
13. 退出学生账号，登录 `judge1 / judge123`。
14. 进入待评审项目或评审详情页。
15. 点击 AI 评审辅助，确认打开火花 Agent 模式且自动选择当前项目。
16. 调用评审辅助。
17. 确认评审辅助没有自动填写评分表。
18. 点击结果复制。
19. 点击结果朗读，确认火花口型动画或朗读逻辑正常。
20. 检查 Live2D 拖拽、表情、收起仍正常。

### 16.2 MCP 必查项

| 检查项 | 要求 |
|---|---|
| Console | 无新增关键错误 |
| Network | `/api/agent/*` 无 404/500 |
| 认证 | 无异常 401，权限错误时应有友好 403 提示 |
| 响应格式 | 符合 `{code, message, data}` |
| 模式切换 | `chat / analysis / agent` 无状态污染 |
| Markdown | 渲染正常，无明显 XSS 风险 |
| 资源 | 无新增 404 静态资源 |
| 交互 | 按钮可点击，loading 正常，禁止重复提交 |
| 截图/记录 | 记录关键页面或操作结果 |

---

## 十七、阶段输出要求

每个 Phase 完成后，必须追加写入：

```text
E:\LEAR-CODE-NEW\软件工程\my-keshe\keshe\各自阶段输出.md
```

### 17.1 阶段输出模板

```markdown
# Phase X：阶段名称

## 完成时间
YYYY-MM-DD HH:mm

## 本阶段目标
说明本阶段要解决什么问题。

## 修改文件
- backend/xxx.py：修改说明
- frontend/xxx.vue：修改说明

## 新增文件
- backend/xxx.py：用途

## 新增或修改接口
- POST /api/agent/xxx：用途、请求参数、响应字段

## 新增或修改数据库模型
- AgentTask：字段说明
- AgentMaterialIndex：字段说明

## 执行命令
```bash
conda activate newyolo
...
```

## 测试方式
说明如何测试本阶段功能。

## 测试结果
- 通过项
- 失败项
- 已修复项

## 对旧功能影响
说明是否影响 `/api/ai/*`、HuahuoAssistant、语音、Live2D、SSE。

## 遗留问题
列出未解决问题和下一步计划。
```

---

## 十八、README 更新要求

任务完成后，必须更新：

```text
E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\README.md
```

### 18.1 总体要求

README 不是只写版本更迭笔记，而是要整体同步到最新项目状态。

必须保证以下章节和代码一致：

- 项目简介
- 技术栈
- 特色功能
- 项目结构
- 环境要求
- 快速开始
- 后端配置
- API 接口文档
- 路由配置
- 数据库模型
- 用户角色与权限
- 设计系统
- 开发规范
- 常见问题
- 当前开发状态
- 版本更迭记录

不能出现这种情况：

```text
版本更迭里写了 LangChain Agent 已完成，
但项目简介、特色功能、API 文档、项目结构、数据库模型仍然是旧版本。
```

### 18.2 版本更迭分类格式

新增版本条目时，必须分清：

```markdown
## vX.X.X - YYYY-MM-DD

### 新增功能
- 新增 LangChain AI 项目智能体模式
- 新增 AI 材料问答
- 新增商业计划书体检

### 功能修改
- 将 Portal / teacher / judge 中残留的 `/ai-assistant` 入口改为打开火花 Agent 模式
- 将 `/ai-assistant` 调整为备用入口

### 功能删除或废弃
- 无
- 或：废弃某旧入口，但保留兼容路由

### Bug 修复
- 修复 Portal 中 AI 助手入口跳转 404
- 修复 teacher/judge 快捷按钮跳转 404

### 安全与稳定性
- Markdown 渲染增加 DOMPurify 安全过滤
- Agent loading 状态禁止重复提交
- 全局事件监听增加 removeEventListener 清理

### 文档更新
- 更新 API 文档
- 更新数据库模型说明
- 更新 MCP 调试说明

### 已知问题
- 如存在，明确列出
```

### 18.3 README 中必须新增或同步的内容

#### 特色功能

新增：

```markdown
### LangChain AI 项目智能体

- 通过火花助手进入，不新增第二套 AI 助手
- 支持 AI 材料问答
- 支持商业计划书体检
- 支持路演稿生成
- 支持 AI 评审辅助
- 支持智能竞赛推荐
- 基于项目材料、报名材料、项目数据和竞赛数据进行智能分析
- 支持 FAISS + Embedding，失败时降级 BM25 / 关键词检索
```

#### 技术栈

新增相关依赖：

```text
langchain
langchain-core
langchain-community
langchain-openai
langchain-text-splitters
faiss-cpu
rank-bm25
python-docx
python-pptx
pypdf 或 PyPDF2
DOMPurify
```

#### 项目结构

同步新增文件：

```text
backend/services/langchain_service.py
backend/services/document_parser.py
backend/services/vector_store.py
backend/routes/agent.py
backend/models/agent_task.py
backend/models/agent_material_index.py
frontend/src/components/HuahuoAssistant.vue
frontend/src/views/ai-assistant/AgentPanel.vue
frontend/src/api/agent.js
```

#### API 文档

新增 `/api/agent/*` 专章。

#### 数据库模型

新增：

```text
AgentTask
AgentMaterialIndex
```

#### 使用说明

写明：

1. 使用 `newyolo` 环境。
2. 安装依赖。
3. 执行迁移。
4. 上传项目材料。
5. 打开火花助手。
6. 切换 AI 智能体模式。
7. 建立材料索引。
8. 进行材料问答、BP 体检、路演稿生成、评审辅助、竞赛推荐。

#### MCP 调试说明

新增 Chrome DevTools MCP 调试章节。

---

## 十九、实施顺序

| 阶段 | 任务 | 风险 | 阶段输出要求 |
|---|---|---|---|
| Phase 1 | 后端文档解析 `document_parser.py` | 低 | 写入阶段输出 |
| Phase 2 | 后端索引服务 `vector_store.py`，含 FAISS/BM25 降级 | 中 | 写入阶段输出 |
| Phase 3 | 后端 LangChain 服务 `langchain_service.py` | 中 | 写入阶段输出 |
| Phase 4 | 数据库模型 `AgentTask` / `AgentMaterialIndex` + 迁移 | 低 | 写入阶段输出 |
| Phase 5 | 后端路由 `routes/agent.py` + 蓝图注册 | 中 | 写入阶段输出 |
| Phase 6 | 前端 API `api/agent.js` | 低 | 写入阶段输出 |
| Phase 7 | `AgentPanel.vue` 组件 | 中 | 写入阶段输出 |
| Phase 8 | `HuahuoAssistant.vue` 集成 agent 模式 | 高 | 写入阶段输出 |
| Phase 9 | 修复 Portal/teacher/judge 残留入口 | 低 | 写入阶段输出 |
| Phase 10 | `/ai-assistant` 备用页与路由处理 | 低 | 写入阶段输出 |
| Phase 11 | Chrome DevTools MCP 调试 | 中 | 写入阶段输出 |
| Phase 12 | README 全量更新 | 低 | 写入阶段输出 |
| Phase 13 | 最终回归验收 | 中 | 写入阶段输出 |

---

## 二十、最终验收标准

### 20.1 旧功能不受影响

| 功能 | 验收要求 |
|---|---|
| 火花加载 | Live2D 正常显示 |
| 火花拖拽 | 位置正常保存和恢复 |
| 对话模式 | 输入问题后 SSE 流式回复正常 |
| AI 分析模式 | 原项目简介 / 商业建议 / 风险分析正常 |
| 语音识别 | 原语音入口正常 |
| TTS 朗读 | 原朗读和口型动画正常 |
| 表情联动 | 原表情逻辑正常 |
| VoiceChat | 不受影响 |
| `/api/ai/*` | 不出现新增错误 |

### 20.2 新功能通过

| 功能 | 验收要求 |
|---|---|
| Agent 模式入口 | 火花面板可切换到 Agent 模式 |
| 材料索引 | 能索引项目材料和报名材料 |
| 材料问答 | 能基于材料回答，并显示来源 |
| BP 体检 | 能输出亮点、不足、缺失模块、建议、风险 |
| 路演稿生成 | 能生成 3/5 分钟结构化稿件 |
| 评审辅助 | 能生成摘要、风险、追问、维度参考，不给具体分数 |
| 竞赛推荐 | 能推荐竞赛和赛道，并可跳转详情 |
| 复制 | Agent 结果可复制 |
| 朗读 | Agent 结果可朗读 |
| 表情 | Agent 结果可触发表情变化 |
| 备用页 | `/ai-assistant` 可用但不是主入口 |
| Markdown 安全 | DOMPurify 等安全过滤已使用 |

### 20.3 MCP 验收通过

| 检查 | 要求 |
|---|---|
| Console | 无新增关键错误 |
| Network | `/api/agent/*` 无 404/500 |
| 权限 | 401/403 行为正确 |
| 响应格式 | `{code, message, data}` |
| 页面交互 | 可点击、loading、错误提示正常 |
| 状态隔离 | chat/analysis/agent 互不污染 |

---

## 二十一、给 AI Coder 的执行要求摘要

1. 按本最终修订方案执行，不再参考旧方案中的冲突内容。
2. 后端 Python 环境统一使用 `newyolo` conda 环境。
3. 每个 Phase 完成后，必须将阶段输出写入：

```text
E:\LEAR-CODE-NEW\软件工程\my-keshe\keshe\各自阶段输出.md
```

4. 任务完成后，必须全量更新：

```text
E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\README.md
```

5. README 更新必须覆盖全篇现有说明，不只是版本更迭。
6. 版本更迭记录必须分为：新增功能、功能修改、功能删除或废弃、Bug 修复、安全与稳定性、文档更新、已知问题。
7. 如果执行中忘记要求，随时回到本方案文档重新核对。
8. 如果 Chrome DevTools MCP 不可用，必须如实说明，不能假装完成 MCP 调试。
9. 不允许新增第二套 AI 助手。
10. 不允许破坏现有 Live2D、语音、SSE、AI 对话和 AI 分析模式。
