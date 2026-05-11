# DESIGN.md — SparkAI Skill Test Landing Page

## 1. 设计目标

本页面是 **SparkAI Skill 调用真实性测试** 的一页式落地页，核心目标：

1. **验证 Skill 真实生效**：通过页面视觉质量证明 8 个本地 Skills 确实被读取并应用
2. **展示 Skill 能力边界**：每个视觉决策都可追溯到具体 Skill 的指导
3. **独立可运行**：不依赖主项目，单文件夹内可完整预览
4. **科技感与高级感并存**：亮色主题、青蓝渐变、精致卡片、流畅交互

---

## 2. 色彩策略

### 主色调

| Token | Hex | 用途 |
|---|---|---|
| `--color-bg` | `#f8fafc` | 页面背景，极浅灰蓝 |
| `--color-surface` | `#ffffff` | 卡片、按钮表面 |
| `--color-hero-start` | `#e0f2fe` | Hero 渐变起点（天蓝） |
| `--color-hero-mid` | `#dbeafe` | Hero 渐变中点（浅蓝） |
| `--color-hero-end` | `#ede9fe` | Hero 渐变终点（淡紫） |
| `--color-accent` | `#0ea5e9` | 主强调色（天空蓝） |
| `--color-accent-deep` | `#0284c7` | 深强调色，用于 hover |

### 文字色阶

| Token | Hex | 用途 |
|---|---|---|
| `--text-primary` | `#0f172a` | 主标题、重要文字 |
| `--text-secondary` | `#475569` | 副标题、描述文字 |
| `--text-muted` | `#94a3b8` | 辅助信息、禁用态 |

### 色彩决策来源

- **frontend-design**：建议使用青蓝/蓝紫渐变方向，避免通用紫色渐变模板
- **design-taste-frontend**：禁止过度饱和强调色，使用单一高对比度强调色（天空蓝）
- **high-end-visual-design**：使用 tinted neutrals，禁止纯黑纯白，背景使用 `#f8fafc` 而非 `#fff`
- **impeccable**：检查对比度，确保文字与背景对比度 ≥ 4.5:1

---

## 3. 字体策略

| 用途 | 字体 | 权重 | 来源 |
|---|---|---|---|
| Display / 标题 | Outfit | 700-800 | high-end-visual-design 推荐，避免 Inter |
| 正文 / 中文 | Noto Sans SC | 400-500 | frontend-design 建议，确保中文显示品质 |

### 字号层级

| 层级 | 尺寸 | 字重 | 用途 |
|---|---|---|---|
| H1 (Hero) | `clamp(2.5rem, 6vw, 4.5rem)` | 800 | 主标题 |
| H2 (Section) | `clamp(1.75rem, 4vw, 2.5rem)` | 700 | 区块标题 |
| H3 (Card) | `1.05rem` | 700 | 卡片标题 |
| Body | `1rem` | 400 | 正文描述 |
| Caption | `0.8rem` | 500 | 标签、状态文字 |
| Eyebrow | `0.75rem` | 600 | 顶部标签 |

### 字体决策来源

- **high-end-visual-design**：明确禁止 Inter、Roboto 等通用字体，推荐使用 Outfit、Geist 等高端字体
- **design-taste-frontend**：Display 字体使用 `tracking-tighter`，正文使用 `leading-relaxed`
- **impeccable**：确保中文字体回退栈完整，避免字体闪烁

---

## 4. 组件结构

### 4.1 Hero 区域

```
hero (min-height: 100dvh)
├── hero-bg (渐变背景 + 径向光晕 + 纹理图案)
├── hero-content (居中内容)
│   ├── eyebrow (小标签: SparkAI Skill Verification)
│   ├── hero-title (主标题)
│   ├── hero-subtitle (副标题)
│   └── hero-actions (两个按钮)
│       ├── btn-primary (查看测试结果)
│       └── btn-secondary (查看 Skill 日志)
└── hero-scroll-hint (滚动提示动画)
```

**设计决策**：
- **high-end-visual-design**：Hero 使用全屏高度 `min-h-[100dvh]`，避免 iOS Safari 视口跳动问题
- **frontend-design**：背景使用多层叠加（渐变 + 径向光晕 + SVG 纹理），创造深度感
- **design-taste-frontend**：Eyebrow 标签使用 uppercase + tracking，建立视觉层级

### 4.2 Skill 卡片区域

```
skill-cards-section
├── section-header
│   ├── section-tag
│   ├── section-title
│   └── section-desc
└── cards-grid (4列网格)
    └── skill-card × 8
        ├── card-shell (外层包裹 - Double-Bezel)
        │   └── card-core (内层内容)
        │       ├── card-icon
        │       ├── card-title
        │       ├── card-desc
        │       └── card-status
        │           ├── status-dot
        │           └── status-text
```

**设计决策**：
- **high-end-visual-design**：使用 "Double-Bezel" 嵌套架构（外层 shell + 内层 core），模拟物理硬件质感
- **high-end-visual-design**：卡片圆角 `rounded-[2rem]`，大圆角创造柔和现代感
- **design-taste-frontend**：卡片 hover 时 `translateY(-6px)` + 阴影增强，提供触觉反馈
- **impeccable**：卡片间距统一 `gap: 1.5rem`，避免视觉拥挤

### 4.3 验证区域

```
verify-section
├── section-header
└── verify-grid (3列网格)
    └── verify-item × 6
        ├── verify-icon (成功图标)
        └── verify-info
            ├── h4 (标题)
            └── p (描述)
```

### 4.4 按钮组件

| 类型 | 背景 | 文字 | 阴影 | Hover |
|---|---|---|---|---|
| Primary | 渐变 `#0ea5e9` → `#0284c7` | `#fff` | 蓝色发光阴影 | `translateY(-2px)` + 阴影增强 |
| Secondary | `#ffffff` | `#0f172a` | 轻微阴影 | 背景变灰 + 阴影增强 |

**设计决策**：
- **high-end-visual-design**：按钮使用 `rounded-full` 全圆角，内部图标嵌套在圆形 wrapper 中
- **design-taste-frontend**：Active 状态使用 `scale(0.98)` 模拟物理按压感
- **ui-ux-pro-max**：确保按钮有明确的 hover 反馈和 focus 状态

---

## 5. 响应式策略

| 断点 | 布局变化 |
|---|---|
| `> 1024px` | 卡片 4 列，验证项 3 列 |
| `768px - 1024px` | 卡片 2 列，验证项 2 列 |
| `< 768px` | 卡片 1 列，验证项 1 列，按钮全宽 |
| `< 480px` | 字号进一步缩小，内边距压缩 |

**设计决策**：
- **ui-ux-pro-max**：移动端优先确保内容可读，避免水平滚动
- **design-taste-frontend**：使用 CSS Grid 而非复杂 flex 百分比计算
- **high-end-visual-design**：非对称布局在移动端必须回退到严格单列

---

## 6. 动画与交互

| 动画 | 实现方式 | 来源 Skill |
|---|---|---|
| Hero 内容淡入上浮 | CSS `@keyframes fadeInUp` | frontend-design |
| 滚动提示动画 | CSS `@keyframes scrollWheel` | design-taste-frontend |
| 卡片 hover 上浮 | `transform: translateY(-6px)` | high-end-visual-design |
| 按钮点击涟漪 | JS 动态创建 ripple span | ui-ux-pro-max |
| 滚动视差 | `requestAnimationFrame` + `translateY` | design-taste-frontend |
| 滚动 reveal | `IntersectionObserver` | frontend-design |
| 卡片点击选中 | `classList.toggle('active')` | ui-ux-pro-max |
| 按钮 hover 图标位移 | `transform: translateX(2px)` | high-end-visual-design |

**缓动函数**：
- 主要过渡：`cubic-bezier(0.4, 0, 0.2, 1)`
- 慢速过渡：`cubic-bezier(0.16, 1, 0.3, 1)`

---

## 7. 使用的 Skills 与影响

| Skill | 影响领域 | 具体设计决策 |
|---|---|---|
| **frontend-design** | 整体架构、布局、响应式 | 页面采用单页结构，Hero + Cards + Verify 三区布局；使用 CSS Grid 实现卡片网格；添加滚动 reveal 动画 |
| **design-md** | 设计文档规范 | 生成本 DESIGN.md 文件，确保设计决策可追溯；建立色彩、字体、组件的 token 体系 |
| **impeccable** | 视觉层级、间距、可访问性 | 检查卡片间距统一为 1.5rem；确保文字对比度达标；添加 `prefers-reduced-motion` 支持；按钮添加 focus 状态 |
| **better-icons** | 图标系统 | 所有图标使用统一风格的 SVG（stroke-width: 1.5-2，24x24 viewBox）；避免使用 emoji |
| **design-taste-frontend** | 审美提升、动画细节 | 禁止 Inter 字体，改用 Outfit；按钮 active 状态使用 scale(0.98)；使用 `min-h-[100dvh]` 替代 `h-screen` |
| **high-end-visual-design** | 高级感、材质、阴影 | 采用 Double-Bezel 卡片架构；使用 `shadow-diffuse` 柔和阴影；Hero 背景多层叠加；大圆角 `rounded-[2rem]` |
| **ui-ux-pro-max** | 交互体验、可用性 | 按钮添加涟漪效果；卡片可点击切换选中状态；平滑滚动到锚点；确保所有交互元素有 hover 反馈 |
| **full-output-enforcement** | 文件完整性 | 确保 5 个文件全部生成且无占位符；无 TODO；无 undefined；代码完整可运行 |

---

## 8. 阴影系统

| 名称 | 值 | 用途 |
|---|---|---|
| `--shadow-sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | 轻微 elevation |
| `--shadow-md` | `0 4px 6px -1px ...` | 卡片 hover |
| `--shadow-lg` | `0 10px 15px -3px ...` | 下拉菜单、浮层 |
| `--shadow-xl` | `0 20px 25px -5px ...` | 卡片 hover 增强 |
| `--shadow-diffuse` | `0 20px 40px -15px rgba(0,0,0,0.05)` | 卡片默认状态 |

---

## 9. 圆角系统

| Token | 值 | 用途 |
|---|---|---|
| `--radius-sm` | `0.75rem` | 小元素 |
| `--radius-md` | `1rem` | 图标容器 |
| `--radius-lg` | `1.5rem` | 验证项 |
| `--radius-xl` | `2rem` | 卡片外壳 |
| `--radius-full` | `9999px` | 按钮、标签 |

---

## 10. 设计原则总结

1. **亮色优先**：整体使用亮色主题，Hero 使用青蓝/蓝紫渐变，避免大面积暗色
2. **大圆角现代感**：所有主要容器使用 `2rem` 圆角，按钮使用全圆角
3. **柔和阴影**：使用低透明度、大扩散范围的阴影，避免生硬投影
4. **清晰留白**：区块间距 `6rem`，内容最大宽度 `1200px`，呼吸感充足
5. **统一图标**：所有图标采用一致的 stroke 风格，无 emoji
6. **响应式优雅**：移动端单列，平板双列，桌面四列，过渡自然
7. **交互反馈**：每个可交互元素都有明确的 hover/active/focus 状态
8. **性能优先**：动画仅使用 `transform` 和 `opacity`，使用 `IntersectionObserver` 而非 scroll 事件
