# SparkAI 产业命题详情页补全设计思路（含 skill-router 路由与本地 Skills 指令版）

> 任务目标：为当前「产业命题」模块补齐详情页，让它像「校外竞赛详情」「校内竞赛详情」「训练营详情」「课程详情」一样，拥有独立、完整、可跳转、可承接的详情展示页。  
> 当前问题：`IndustryTopics.vue` 只有列表页与「承接命题」跳转，缺少产业命题详情页，导致用户无法先完整了解命题背景、需求、交付物、奖励、周期、企业信息后再决定是否承接。

---

## 0. 本次任务的核心结论

请新增一个产业命题详情页：

```txt
frontend/src/views/portal/IndustryTopicDetail.vue
```

并新增路由：

```txt
/industry-topics/:id
```

保留已有承接路由：

```txt
/accept-topic/:id
```

最终用户路径应该是：

```txt
产业命题列表页
  ↓ 点击「查看详情」或点击卡片
产业命题详情页
  ↓ 点击「承接命题」
承接命题填写页
  ↓ 确认后
创建项目页
```

不要让「承接命题」按钮直接替代详情页。

---

## 1. 必须优先调用 skill-router

本次任务涉及“该用哪些 Skills”判断，因此请先调用本地 Skill：

```txt
skill-router
```

调用目的：

1. 先检查当前 available skills list。
2. 只选择当前可用 Skills。
3. 防止 AI 假装调用不存在的 Skill。
4. 给出本次任务的 Skill 使用计划。
5. 在任务结束时给出 Skill 使用总结和验证方式。
6. 如果需要浏览器页面 QA，只能调用顶层 `gstack`，并说明使用它的 browser testing / QA 内部能力。

调用后，最终回复必须包含：

```txt
SKILL_ROUTER_APPLIED: ROUTER_20260512_CN_GSTACK
```

如果 `skill-router` 不在 available skills list 中，请明确说明不可用，并退回到手动 Skill 使用计划，不要假装调用。

---

## 2. 本次推荐使用的 Skills

请不要一次性乱用所有 Skills。建议按阶段使用：

| 阶段 | 必须 / 推荐 Skill | 用途 |
|---|---|---|
| Skill 路由 | `skill-router` | 先判断本次任务该使用哪些 available skills，防止假调用 |
| 现状审计 | `redesign-existing-projects` | 审计 `IndustryTopics.vue`、`AcceptTopic.vue`、router 配置和已有详情页写法 |
| 页面结构 | `frontend-design` | 规划产业命题详情页的信息架构、Hero、内容区、侧栏操作卡 |
| 设计系统对齐 | `design-md` | 对齐 SparkAI 现有详情页、Banner、卡片、按钮、圆角、渐变规范 |
| UI 抛光 | `impeccable` | 检查间距、视觉层级、按钮状态、响应式、可读性 |
| 图标统一 | `better-icons` | 为企业、周期、预算、交付物、难度、承接按钮等选择统一图标 |
| 体验判断 | `ui-ux-pro-max` | 确保用户从了解命题到承接命题的路径顺畅 |
| 完整输出 | `full-output-enforcement` | 防止漏路由、漏文件、漏按钮、undefined、TODO、半成品 |
| 页面 QA | `gstack` | 如可用，使用顶层 `gstack` 的 browser testing / QA 能力检查页面跳转和展示 |

可选但不强制：

| Skill | 用途 |
|---|---|
| `diagnose` | 如果出现路由跳转失败、数据找不到、刷新 404、按钮失效等 bug，再调用 |
| `gpt-taste` | 如果页面视觉仍然模板感强，可用于增强审美 |
| `high-end-visual-design` | 如果详情页 Hero 和内容卡片需要更高级的视觉质感，可调用 |

不要使用：

| Skill | 原因 |
|---|---|
| `industrial-brutalist-ui` | SparkAI 当前不是粗野主义风格 |
| `image-to-code` | 本次不是按截图还原 |
| `imagegen-frontend-web` | 本次不生成参考图 |
| `imagegen-frontend-mobile` | 本次不生成移动端参考图 |
| `brandkit` | 本次不重做品牌系统 |

---

## 3. 必须生成 Skill 使用日志

为了验证 AI 是否真的调用了 Skills，请在项目根目录创建或更新：

```txt
SKILL_USAGE_LOG_INDUSTRY_TOPIC_DETAIL.md
```

同时在终端追加运行轨迹：

```txt
SKILL_RUNTIME_TRACE.log
```

### 3.1 Markdown 日志格式

每次使用 Skill 都追加一条：

```md
### 记录 N
- 时间：YYYY-MM-DD HH:mm:ss
- 当前任务：正在处理什么
- 调用 Skill：skill-router / frontend-design / impeccable / ...
- 该 Skill 给出的帮助：必须具体说明，不允许套话
- 应用到的文件：例如 router/index.js、IndustryTopics.vue、IndustryTopicDetail.vue
- 可验证结果：用户如何在页面或代码中看到这个 Skill 生效
```

### 3.2 终端日志格式

请使用系统真实时间，不要手写固定时间。PowerShell 格式参考：

```powershell
$log = "E:\LEAR-CODE-NEW\软件工程\my-keshe\SKILL_RUNTIME_TRACE.log"
$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[SKILL-START] $now | skill-router | 产业命题详情页任务 Skill 路由" | Add-Content -Path $log -Encoding utf8
```

每个 Skill 至少写：

```txt
[SKILL-START] 时间 | skill-name | 当前任务
[SKILL-END] 时间 | skill-name | 具体帮助 | 产出文件
```

如果无法调用某个 Skill，必须写：

```txt
[SKILL-FAILED] 时间 | skill-name | 无法调用原因
```

---

## 4. 当前项目事实依据

根据当前 README，平台页中已有：

```txt
/industry-topics    => portal/IndustryTopics.vue    产业命题
/accept-topic/:id   => portal/AcceptTopic.vue       承接命题（填写承接信息）
```

同时，校外竞赛、校内竞赛、训练营和课程都已经有对应详情页：

```txt
/external-competitions/:slug  => ExternalCompetitionDetail.vue
/competitions/:id             => CompetitionDetail.vue
/training-camps/:id           => TrainingCampDetail.vue
/courses/:id                  => CourseDetail.vue
```

所以产业命题也应该补齐：

```txt
/industry-topics/:id          => IndustryTopicDetail.vue
```

这是一次“模块一致性补齐”，不是新业务乱加。

---

## 5. 页面体验目标

### 5.1 产业命题列表页

当前 `IndustryTopics.vue` 中每张卡片应该有两个动作：

```txt
查看详情
承接命题
```

建议交互：

- 点击卡片主体或「查看详情」：进入 `/industry-topics/:id`
- 点击「承接命题」：进入 `/accept-topic/:id`
- 不要让卡片只有「承接命题」一个动作
- 卡片中的「承接命题」按钮保留，但详情页才是更完整的决策入口

### 5.2 产业命题详情页

详情页必须像校内竞赛 / 校外竞赛 / 训练营 / 课程详情一样完整，而不是简单弹窗。

建议页面结构：

```txt
Hero 大横幅
  - 命题标题
  - 企业 / 实验室 / 发布单位
  - 难度 / 周期 / 预算 / 领域标签
  - 主按钮：承接命题
  - 次按钮：返回列表

主体内容
  - 命题背景
  - 需求说明
  - 技术方向
  - 交付物要求
  - 周期安排
  - 评分 / 验收标准
  - 企业信息
  - 适合团队

右侧吸附操作卡
  - 命题状态
  - 难度
  - 周期
  - 奖金 / 经费
  - 发布单位
  - 承接命题按钮
```

---

## 6. 详情页内容板块建议

### 6.1 Hero 区

产业命题没有真实海报也没关系，可以使用高质量渐变 Hero，但要和平台详情页保持一致。

Hero 风格建议：

```txt
深青蓝 / 产业科技渐变
柔和光球
数据网格
企业协作感
轻科技线条
```

Hero 中展示：

- 命题标题
- 发布单位 / 企业名 / 实验室名
- 标签：产业命题、企业真实需求、难度、周期
- 摘要介绍
- 承接命题按钮

### 6.2 命题背景

解释企业为什么提出这个命题：行业痛点、业务场景、当前问题、希望学生团队解决什么。

### 6.3 需求说明

用清晰列表写：核心目标、功能需求、技术需求、数据需求、用户角色、约束条件。

### 6.4 技术方向

适合展示：前端 / 后端 / AI / 数据分析 / 物联网 / 小程序 / 算法、推荐技术栈、是否需要原型、部署、文档。

### 6.5 交付物要求

必须明确学生要交什么：方案设计书、系统原型、源代码、部署说明、测试报告、路演 PPT、演示视频。

### 6.6 周期安排

可以做成时间线：需求理解、方案设计、原型开发、中期检查、最终交付、验收展示。

### 6.7 奖励与支持

展示：奖金 / 经费、企业导师指导、数据或场景支持、实习 / 孵化机会、证书或推荐机会。

### 6.8 适合团队

告诉学生什么团队适合承接：团队人数建议、技术能力要求、角色构成、适合专业、是否需要指导老师。

### 6.9 右侧操作卡

建议固定在右侧或随滚动吸附：

```txt
命题信息
- 发布单位
- 难度
- 周期
- 奖励
- 领域
- 状态

[承接命题]
[返回列表]
```

---

## 7. 数据结构建议

如果当前产业命题数据是写在 `IndustryTopics.vue` 里，建议抽到单独文件：

```txt
frontend/src/data/industryTopics.js
```

数据结构建议：

```js
export const industryTopics = [
  {
    id: 1,
    title: '智慧校园服务创新命题',
    company: '智慧校园实验室',
    difficulty: '中等',
    duration: '3 个月',
    reward: '优秀团队可获得实习机会',
    budget: '3000 元',
    status: '开放承接',
    category: '智慧校园',
    tags: ['智慧校园', '教育科技', '系统开发'],
    summary: '围绕校园服务体验，设计并实现一个面向学生的智能服务原型。',
    background: '...',
    requirements: ['...', '...'],
    techDirections: ['Vue 3', 'Flask', '数据可视化'],
    deliverables: ['方案设计书', '系统原型', '源代码仓库', '演示视频'],
    schedule: [
      { name: '需求理解', time: '第 1 周', desc: '完成场景调研和需求拆解' },
      { name: '方案设计', time: '第 2-3 周', desc: '形成系统设计和交互原型' }
    ],
    evaluation: ['创新性', '可行性', '完成度', '展示效果'],
    suitableTeam: ['前端开发', '后端开发', '产品设计', '项目管理']
  }
]
```

如果当前数据已经在组件里，也可以先不抽离，但强烈建议抽离，方便列表页和详情页共享同一份数据，避免重复维护。

---

## 8. 路由设计

在 `frontend/src/router/index.js` 中新增平台路由：

```js
{
  path: '/industry-topics/:id',
  name: 'IndustryTopicDetail',
  component: () => import('@/views/portal/IndustryTopicDetail.vue'),
  meta: {
    title: '产业命题详情',
    platformPage: true
  }
}
```

注意：

- `meta` 字段要对齐项目现有路由写法。
- 如果项目使用的是 `platform: true`，就沿用 `platform: true`。
- 不要随意改现有路由守卫。
- `/accept-topic/:id` 保持学生专属路由或现有权限逻辑。
- 详情页如果所有角色都能看，建议放在平台页面分组。
- 承接按钮是否需要登录或学生身份，沿用 `AcceptTopic.vue` 的现有逻辑。

---

## 9. 列表页修改

在 `IndustryTopics.vue` 中：

1. 卡片主体点击跳转详情页。
2. 新增「查看详情」按钮。
3. 保留「承接命题」按钮。
4. 不要让点击承接按钮冒泡触发详情跳转。
5. 保持顶部 Banner 和卡片风格与其它平台页一致。

示例逻辑方向：

```js
const goDetail = (topic) => {
  router.push(`/industry-topics/${topic.id}`)
}

const acceptTopic = (topic) => {
  router.push(`/accept-topic/${topic.id}`)
}
```

按钮事件注意：

```vue
@click.stop="acceptTopic(topic)"
```

---

## 10. 详情页空状态与异常处理

详情页通过 `route.params.id` 找数据：

- 找到数据：正常展示。
- 找不到数据：展示友好的空状态。
- 空状态提供「返回产业命题」按钮。
- 不要出现 undefined。
- 不要白屏。
- 控制台不要报错。

---

## 11. 视觉统一要求

详情页视觉应参考：

- `ExternalCompetitionDetail.vue`
- `CompetitionDetail.vue`
- `TrainingCampDetail.vue`
- `CourseDetail.vue`

统一点：

1. 顶部大 Hero。
2. 主体白色内容卡片。
3. 右侧信息 / 操作卡。
4. 大圆角。
5. 柔和阴影。
6. 青蓝 / 深青蓝 / 产业科技渐变。
7. 响应式布局。
8. 移动端右侧卡片下移到正文下方。

不要做成：简单弹窗、只有一屏文字、后台详情页、纯表格页、没有承接 CTA 的说明页。

---

## 12. 分步骤 Prompt

### Prompt 1：使用 skill-router 制定 Skill 计划

请先调用本地 Skill：`skill-router`，检查当前 available skills list，并为“产业命题详情页补齐任务”选择合适 Skills。不要假装调用不存在的 Skill。输出 Skill 使用计划，并把调用情况写入 `SKILL_USAGE_LOG_INDUSTRY_TOPIC_DETAIL.md` 和 `SKILL_RUNTIME_TRACE.log`。

### Prompt 2：审计现有产业命题模块

请审计 `IndustryTopics.vue`、`AcceptTopic.vue`、router 配置，以及校外竞赛、校内竞赛、训练营、课程的详情页实现方式。确认产业命题目前缺少详情页，只存在列表和承接填写页。保留现有承接逻辑，不要破坏 `/accept-topic/:id`。

建议调用 Skills：`redesign-existing-projects`、`frontend-design`、`full-output-enforcement`。

### Prompt 3：新增产业命题详情页

请新增 `IndustryTopicDetail.vue`，页面结构参考现有详情页：顶部 Hero、正文内容卡片、右侧命题信息卡、承接 CTA。详情页需要展示命题背景、需求说明、技术方向、交付物、周期安排、奖励支持、适合团队和验收标准。

建议调用 Skills：`frontend-design`、`design-md`、`impeccable`、`ui-ux-pro-max`。

### Prompt 4：新增路由并连接列表页

请在 router 中新增 `/industry-topics/:id` 路由。修改 `IndustryTopics.vue`，让卡片主体和「查看详情」按钮跳转详情页，「承接命题」按钮继续跳转 `/accept-topic/:id`。注意阻止按钮事件冒泡，避免点击承接时进入详情页。

建议调用 Skills：`redesign-existing-projects`、`frontend-design`、`full-output-enforcement`。

### Prompt 5：整理产业命题数据

请检查产业命题数据是否写死在组件内。如果是，建议抽离到 `frontend/src/data/industryTopics.js`，让列表页、详情页、承接页共享数据。不要重复维护多份数据。保证没有 undefined。

建议调用 Skills：`frontend-design`、`full-output-enforcement`。

### Prompt 6：视觉抛光和响应式

请统一产业命题详情页与校外竞赛、校内竞赛、训练营、课程详情页的视觉语言：大 Hero、白色内容卡、右侧吸附操作卡、大圆角、柔和阴影、产业科技渐变。移动端改为单列布局。

建议调用 Skills：`impeccable`、`high-end-visual-design`、`ui-ux-pro-max`、`better-icons`。

### Prompt 7：QA 与验收

请运行构建和页面检查。验证 `/industry-topics` 列表可进入 `/industry-topics/:id` 详情页；详情页「承接命题」可进入 `/accept-topic/:id`；刷新详情页不白屏；无 undefined；控制台无报错；移动端布局正常。

建议调用 Skills：`gstack`（使用 browser testing / QA 内部能力）、`full-output-enforcement`。如果 `gstack` 不可用，则手动浏览器验证并记录。

---

## 13. 验收标准

### 13.1 路由与页面

- 已新增 `IndustryTopicDetail.vue`。
- 已新增 `/industry-topics/:id` 路由。
- `/industry-topics` 列表页卡片可进入详情页。
- 详情页刷新后正常显示。
- 不存在命题时有友好空状态。
- `/accept-topic/:id` 原有承接流程不被破坏。

### 13.2 视觉与体验

- 产业命题详情页像完整的平台详情页，不是弹窗。
- 顶部有产业科技感 Hero。
- 正文内容结构清晰。
- 右侧有命题信息与承接 CTA。
- 和校外竞赛、校内竞赛、训练营、课程详情页保持一致的设计语言。
- 移动端单列展示正常。

### 13.3 数据与功能

- 列表页、详情页、承接页尽量共享同一份产业命题数据。
- 不出现 undefined。
- 不出现 TODO。
- 不出现控制台报错。
- 承接按钮正常跳转。
- 返回列表正常。

### 13.4 Skill 验证

- 最终回复包含 `SKILL_ROUTER_APPLIED: ROUTER_20260512_CN_GSTACK`，前提是实际调用了 `skill-router`。
- 根目录有 `SKILL_USAGE_LOG_INDUSTRY_TOPIC_DETAIL.md`。
- 根目录 `SKILL_RUNTIME_TRACE.log` 有真实时间的 `[SKILL-START]` / `[SKILL-END]` 记录。
- 每个 Skill 的记录都说明了具体帮助和应用文件。
- 不允许写“模拟 Skill 调用”。
- 不允许手写错误日期。
- 如果某个 Skill 不可用，必须明确写 `[SKILL-FAILED]`，不能假装使用。

---

## 14. 给 AI Coder 的一句话重点

```txt
产业命题现在只有列表页和承接页，缺少详情页；请先调用 skill-router 规划可用 Skills，然后新增 /industry-topics/:id 详情页，让产业命题模块像校外竞赛、校内竞赛、训练营、课程一样完整，并保留 /accept-topic/:id 承接流程。
```
