# TRAE CN Skill 调用真实性测试任务

> 测试目的：验证 TRAE CN 是否真的会读取、调用并应用本地 Skills，而不是只在总结里口头声称“已使用 Skill”。  
> 测试目录：`E:\LEAR-CODE-NEW\软件工程\my-keshe\TEST`  
> 任务类型：创建一个独立的一页式网页，不依赖 SparkAI 主项目，不改动主项目代码。  
> 重要要求：本任务的核心不是做复杂功能，而是验证 Skill 是否真实生效、是否能留下可检查证据。

---

## 0. 绝对禁止

1. 不要修改 SparkAI 主项目任何文件。
2. 不要修改 `frontend`、`backend`、数据库、路由、登录、Live2D、AI 助手等主项目代码。
3. 不要只写总结，不写实际文件。
4. 不要只说“已调用 Skill”，必须在 TEST 目录生成可验证的文件。
5. 不要使用 2025 年或错误时间。必须使用执行任务时的系统真实时间。

---

## 1. 必须使用的本地 Skills

开始前必须主动使用以下本地 Skills，Skill 名必须严格按本地文件夹名：

| 本地 Skill 文件夹名 | 本次测试用途 |
|---|---|
| `frontend-design` | 设计一页式网页的信息架构、页面布局、响应式结构 |
| `design-md` | 生成页面设计规范，确保设计语言明确 |
| `impeccable` | 检查视觉层级、间距、圆角、阴影、按钮状态、可访问性 |
| `better-icons` | 为页面选择统一风格图标 |
| `design-taste-frontend` | 提升页面审美，避免默认模板感 |
| `high-end-visual-design` | 增强高级感、留白、渐变、卡片质感 |
| `ui-ux-pro-max` | 检查交互体验、CTA、响应式和可用性 |
| `full-output-enforcement` | 确保文件完整、没有 TODO、没有占位符、没有 undefined |

可选使用：

| 本地 Skill 文件夹名 | 用途 |
|---|---|
| `redesign-existing-projects` | 如果你认为需要审计已有 TEST 文件，可使用；如果 TEST 是空文件夹，可不使用 |

不要使用：

| 本地 Skill 文件夹名 | 原因 |
|---|---|
| `industrial-brutalist-ui` | 本次不做粗野主义 |
| `image-to-code` | 本次不按图片还原 |
| `imagegen-frontend-web` | 本次不生成参考图 |
| `imagegen-frontend-mobile` | 本次不生成移动端参考图 |
| `brandkit` | 本次不做品牌重塑 |

---

## 2. 必须生成的文件

请在 `E:\LEAR-CODE-NEW\软件工程\my-keshe\TEST` 目录下创建以下文件：

```txt
TEST/
├── index.html
├── styles.css
├── script.js
├── DESIGN.md
└── SKILL_USAGE_LOG_TEST.md
```

说明：

- `index.html`：测试网页主体。
- `styles.css`：网页样式。
- `script.js`：简单交互。
- `DESIGN.md`：本次网页的设计说明。
- `SKILL_USAGE_LOG_TEST.md`：Skill 调用证据日志，最重要。

---

## 3. 网页主题

请创建一个独立的一页式网页，主题为：

```txt
SparkAI Skill Test Landing Page
```

中文标题可以写：

```txt
火花智创 · Skill 调用测试页
```

页面内容必须包括：

1. 顶部 Hero 区域  
   - 标题：`火花智创 · Skill 调用测试页`
   - 副标题：`用于验证 TRAE CN 是否真实调用本地 Skills`
   - 两个按钮：`查看测试结果`、`查看 Skill 日志`

2. Skill 检查卡片区  
   展示至少 8 张卡片，分别对应：
   - frontend-design
   - design-md
   - impeccable
   - better-icons
   - design-taste-frontend
   - high-end-visual-design
   - ui-ux-pro-max
   - full-output-enforcement

3. 可视化测试结果区  
   用简单 UI 展示：
   - 页面已创建
   - 样式已加载
   - JS 已运行
   - Skill 日志已生成
   - 响应式布局已处理

4. 简单交互  
   至少实现一个交互，例如：
   - 点击按钮滚动到 Skill 日志说明区
   - 点击卡片切换选中状态
   - 点击按钮切换浅色 / 深色预览模式  
   注意：交互必须写在 `script.js` 中，不要只用 HTML 假装。

---

## 4. 视觉方向

不要写成普通默认网页。请让页面明显体现 Skills 的设计效果。

方向：

```txt
亮色科技感
青蓝 / 蓝紫渐变
大圆角卡片
柔和阴影
清晰留白
现代按钮
统一图标
响应式布局
```

要求：

1. 整体亮色，不要大面积暗色。
2. Hero 有高级渐变背景。
3. 卡片有 hover 效果。
4. 按钮有明确主次关系。
5. 图标风格统一。
6. 字体层级清晰。
7. 移动端一列展示，PC 多列展示。
8. 不要出现廉价模板感。

---

## 5. DESIGN.md 要求

在 `DESIGN.md` 中写清楚：

1. 页面设计目标。
2. 色彩策略。
3. 组件结构。
4. 响应式策略。
5. 每个主要区域参考了哪些 Skills。
6. 哪些设计决策来自哪个 Skill。

示例格式：

```md
# DESIGN.md

## 设计目标
...

## 使用的 Skills 与影响
- frontend-design：用于确定页面结构和响应式布局
- impeccable：用于检查卡片间距、按钮状态和视觉层级
...
```

---

## 6. SKILL_USAGE_LOG_TEST.md 要求

这是本任务最重要的文件。

必须在 `SKILL_USAGE_LOG_TEST.md` 中逐条记录每次 Skill 调用。

### 必须包含的字段

每条记录必须包含：

```md
### 记录 N
- 时间：YYYY-MM-DD HH:mm:ss
- 当前任务：正在处理什么
- 调用 Skill：具体本地 Skill 文件夹名
- 该 Skill 给出的帮助：必须写具体，不允许泛泛而谈
- 应用到的文件：例如 index.html / styles.css / script.js / DESIGN.md
- 可验证结果：用户如何在页面或代码中看出这个 Skill 生效了
```

### 时间要求

1. 时间必须是执行任务时的真实系统时间。
2. 不允许写固定日期。
3. 不允许写 2025 年旧日期。
4. 如果无法读取系统时间，请先说明原因，并通过命令或环境获取当前时间后再写入。
5. 所有记录时间必须精确到秒。

### 至少记录这些 Skills

必须至少有以下 8 条记录：

```txt
frontend-design
design-md
impeccable
better-icons
design-taste-frontend
high-end-visual-design
ui-ux-pro-max
full-output-enforcement
```

如果实际没有调用某个 Skill，不要虚假记录；应停止任务并说明无法调用原因。

---

## 7. 如何验证你真的使用了 Skill

请在 `SKILL_USAGE_LOG_TEST.md` 最后添加一个「验证清单」：

```md
## 验证清单

- [ ] index.html 已创建
- [ ] styles.css 已创建
- [ ] script.js 已创建
- [ ] DESIGN.md 已创建
- [ ] 每个要求的 Skill 都有单独记录
- [ ] 每条 Skill 记录都有真实时间
- [ ] 每条 Skill 记录都说明了具体帮助
- [ ] 页面视觉不是默认模板
- [ ] 页面有响应式布局
- [ ] 页面有 JS 交互
- [ ] 无 TODO
- [ ] 无 undefined
```

完成后必须全部勾选。

---

## 8. 文件完整性要求

`full-output-enforcement` 必须用于最终检查：

1. 不允许出现 `TODO`。
2. 不允许出现 `undefined`。
3. 不允许出现空文件。
4. 不允许只写注释不写实现。
5. 不允许只生成 HTML 不生成 CSS / JS。
6. 不允许只写日志不做网页。
7. 不允许文件路径写错。
8. 不允许遗漏 `DESIGN.md` 或 `SKILL_USAGE_LOG_TEST.md`。

---

## 9. 最终回复要求

任务完成后，请回复：

```txt
TEST Skill 调用测试页已完成。

生成文件：
- index.html
- styles.css
- script.js
- DESIGN.md
- SKILL_USAGE_LOG_TEST.md

本次实际调用 Skills：
- ...
- ...

请打开 TEST/index.html 查看页面效果。
请查看 TEST/SKILL_USAGE_LOG_TEST.md 核对 Skill 调用记录。
```

不要只回复“完成了”。

---

## 10. 一句话重点

```txt
本任务不是为了做复杂网页，而是为了验证 TRAE CN 是否真的调用本地 Skills：必须创建网页，必须生成 DESIGN.md，必须生成 SKILL_USAGE_LOG_TEST.md，必须记录真实时间、具体 Skill、具体帮助和可验证结果。
```
