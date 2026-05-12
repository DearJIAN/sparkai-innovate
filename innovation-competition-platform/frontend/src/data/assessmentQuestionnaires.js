export const realQuestionnaires = [
  {
    id: 'entrepreneurial-spirit',
    category: '创业测评',
    title: '创业精神测评',
    description: '评估创业主动性、机会识别意识、坚韧程度与风险承担倾向，帮助你了解自己的创业精神画像。',
    duration: 10,
    totalQuestions: 10,
    isReal: true,
    resultDimensions: ['主动性', '机会意识', '抗挫力', '责任感'],
    questions: [
      {
        id: 'Q1',
        dimension: '主动性',
        stem: '当你发现一个校园或生活中的痛点时，你通常会：',
        options: [
          { key: 'A', text: '觉得和自己关系不大，很少继续关注', score: 1 },
          { key: 'B', text: '偶尔会想想原因，但通常不会行动', score: 2 },
          { key: 'C', text: '会主动查资料，判断是否有改进空间', score: 3 },
          { key: 'D', text: '会快速提出方案，并尝试找人一起验证', score: 4 }
        ]
      },
      {
        id: 'Q2',
        dimension: '主动性',
        stem: '面对一个不确定但有潜力的项目机会时，你更可能：',
        options: [
          { key: 'A', text: '因为不确定性太大而直接放弃', score: 1 },
          { key: 'B', text: '等别人先尝试后再决定是否参与', score: 2 },
          { key: 'C', text: '先做小范围调研，再决定下一步', score: 3 },
          { key: 'D', text: '主动组织资源，用低成本方式快速验证', score: 4 }
        ]
      },
      {
        id: 'Q3',
        dimension: '抗挫力',
        stem: '如果项目第一次尝试失败，你通常会：',
        options: [
          { key: 'A', text: '认为说明方向不适合自己，直接停止', score: 1 },
          { key: 'B', text: '暂时搁置，等以后有机会再说', score: 2 },
          { key: 'C', text: '复盘失败原因，并尝试调整方案', score: 3 },
          { key: 'D', text: '主动收集反馈，快速迭代并再次测试', score: 4 }
        ]
      },
      {
        id: 'Q4',
        dimension: '责任感',
        stem: '在团队中遇到没人愿意承担的关键任务时，你会：',
        options: [
          { key: 'A', text: '尽量避免接手，担心影响自己', score: 1 },
          { key: 'B', text: '等老师或负责人安排', score: 2 },
          { key: 'C', text: '如果自己能做，会主动承担一部分', score: 3 },
          { key: 'D', text: '主动协调任务分工，并推动任务完成', score: 4 }
        ]
      },
      {
        id: 'Q5',
        dimension: '机会意识',
        stem: '你对"从想法到落地"的看法更接近：',
        options: [
          { key: 'A', text: '好想法最重要，能不能落地以后再说', score: 1 },
          { key: 'B', text: '落地很难，所以通常只停留在讨论', score: 2 },
          { key: 'C', text: '想法需要通过计划和执行逐步验证', score: 3 },
          { key: 'D', text: '好项目必须快速形成原型、用户反馈和迭代闭环', score: 4 }
        ]
      },
      {
        id: 'Q6',
        dimension: '抗挫力',
        stem: '当别人质疑你的项目想法时，你通常会：',
        options: [
          { key: 'A', text: '感到被否定，不想继续表达', score: 1 },
          { key: 'B', text: '表面接受，但很少进一步分析', score: 2 },
          { key: 'C', text: '记录质疑点，并判断哪些值得改进', score: 3 },
          { key: 'D', text: '主动追问依据，把质疑转化成验证清单', score: 4 }
        ]
      },
      {
        id: 'Q7',
        dimension: '机会意识',
        stem: '面对资源不足的问题时，你更倾向于：',
        options: [
          { key: 'A', text: '没有资源就很难推进，只能等待', score: 1 },
          { key: 'B', text: '先降低目标，避免投入太多精力', score: 2 },
          { key: 'C', text: '寻找替代方案，用现有资源做简化版本', score: 3 },
          { key: 'D', text: '主动链接老师、同学、企业或平台资源推动解决', score: 4 }
        ]
      },
      {
        id: 'Q8',
        dimension: '责任感',
        stem: '你在参与竞赛或项目时，对目标通常会：',
        options: [
          { key: 'A', text: '没有明确目标，跟着团队节奏走', score: 1 },
          { key: 'B', text: '只关注完成最低要求', score: 2 },
          { key: 'C', text: '会设定阶段目标，并按节点推进', score: 3 },
          { key: 'D', text: '会拆解目标、设置指标，并定期复盘优化', score: 4 }
        ]
      },
      {
        id: 'Q9',
        dimension: '责任感',
        stem: '当项目进入重复、琐碎的执行阶段时，你通常会：',
        options: [
          { key: 'A', text: '很快失去兴趣，执行质量下降', score: 1 },
          { key: 'B', text: '需要别人频繁提醒才能继续推进', score: 2 },
          { key: 'C', text: '能保持基本执行，并按时完成任务', score: 3 },
          { key: 'D', text: '会优化流程，提高效率，并带动团队坚持', score: 4 }
        ]
      },
      {
        id: 'Q10',
        dimension: '机会意识',
        stem: '你认为创业精神最核心的是：',
        options: [
          { key: 'A', text: '有一个听起来新颖的点子', score: 1 },
          { key: 'B', text: '敢于表达自己的想法', score: 2 },
          { key: 'C', text: '能发现问题并持续推动解决', score: 3 },
          { key: 'D', text: '能承担不确定性，并用行动创造真实价值', score: 4 }
        ]
      }
    ]
  },
  {
    id: 'entrepreneurial-personality',
    category: '创业测评',
    title: '创业性格测评',
    description: '评估学生在风险承受、决策风格、沟通开放性、自我驱动和情绪稳定性方面的创业性格特征。',
    duration: 10,
    totalQuestions: 10,
    isReal: true,
    resultDimensions: ['决策风格', '适应能力', '沟通开放', '风险承受', '坚韧性'],
    questions: [
      {
        id: 'Q1',
        dimension: '决策风格',
        stem: '面对一个需要快速判断的项目机会时，你通常会：',
        options: [
          { key: 'A', text: '因为担心出错而迟迟不做决定', score: 1 },
          { key: 'B', text: '主要参考别人的选择', score: 2 },
          { key: 'C', text: '收集关键信息后做出判断', score: 3 },
          { key: 'D', text: '能在有限信息下快速决策，并承担结果', score: 4 }
        ]
      },
      {
        id: 'Q2',
        dimension: '适应能力',
        stem: '当计划被临时打乱时，你更可能：',
        options: [
          { key: 'A', text: '明显焦虑，难以继续推进', score: 1 },
          { key: 'B', text: '需要较长时间重新适应', score: 2 },
          { key: 'C', text: '调整优先级后继续处理', score: 3 },
          { key: 'D', text: '快速重组计划，并寻找新的机会点', score: 4 }
        ]
      },
      {
        id: 'Q3',
        dimension: '沟通开放',
        stem: '在公开表达项目观点时，你通常会：',
        options: [
          { key: 'A', text: '尽量避免发言', score: 1 },
          { key: 'B', text: '只有被点名时才简单表达', score: 2 },
          { key: 'C', text: '能清楚表达自己的核心观点', score: 3 },
          { key: 'D', text: '能主动表达、回应追问并影响他人', score: 4 }
        ]
      },
      {
        id: 'Q4',
        dimension: '沟通开放',
        stem: '当团队意见与你不同的时候，你会：',
        options: [
          { key: 'A', text: '直接放弃自己的意见', score: 1 },
          { key: 'B', text: '表面同意，但内心保留', score: 2 },
          { key: 'C', text: '尝试说明理由并听取对方观点', score: 3 },
          { key: 'D', text: '主动推动讨论，帮助团队形成更优方案', score: 4 }
        ]
      },
      {
        id: 'Q5',
        dimension: '风险承受',
        stem: '你对风险的态度更接近：',
        options: [
          { key: 'A', text: '只要有风险就尽量避免', score: 1 },
          { key: 'B', text: '风险较小时才愿意尝试', score: 2 },
          { key: 'C', text: '会评估风险和收益后决定是否行动', score: 3 },
          { key: 'D', text: '能接受合理风险，并提前准备应对方案', score: 4 }
        ]
      },
      {
        id: 'Q6',
        dimension: '坚韧性',
        stem: '当连续遇到多个困难时，你通常会：',
        options: [
          { key: 'A', text: '很容易怀疑自己，不想继续', score: 1 },
          { key: 'B', text: '需要别人鼓励才能坚持', score: 2 },
          { key: 'C', text: '会分解问题，一个一个解决', score: 3 },
          { key: 'D', text: '会把困难视为挑战，并主动寻找突破口', score: 4 }
        ]
      },
      {
        id: 'Q7',
        dimension: '坚韧性',
        stem: '你对长期目标的执行习惯更接近：',
        options: [
          { key: 'A', text: '容易三分钟热度', score: 1 },
          { key: 'B', text: '有目标但经常被其他事情打断', score: 2 },
          { key: 'C', text: '能按计划推进大部分任务', score: 3 },
          { key: 'D', text: '会持续跟踪目标，并根据结果优化行动', score: 4 }
        ]
      },
      {
        id: 'Q8',
        dimension: '适应能力',
        stem: '你面对陌生领域时通常会：',
        options: [
          { key: 'A', text: '因为不了解而回避', score: 1 },
          { key: 'B', text: '先观望，等别人带着做', score: 2 },
          { key: 'C', text: '主动学习基础知识', score: 3 },
          { key: 'D', text: '快速建立学习路径，并把学习转化为实践', score: 4 }
        ]
      },
      {
        id: 'Q9',
        dimension: '决策风格',
        stem: '当别人指出你的不足时，你会：',
        options: [
          { key: 'A', text: '感到不舒服，倾向于否认', score: 1 },
          { key: 'B', text: '接受但不一定改变', score: 2 },
          { key: 'C', text: '分析是否合理，并适当调整', score: 3 },
          { key: 'D', text: '主动寻求反馈，把它作为自我升级的机会', score: 4 }
        ]
      },
      {
        id: 'Q10',
        dimension: '风险承受',
        stem: '你在项目中的性格优势更接近：',
        options: [
          { key: 'A', text: '更适合完成明确、低变化的任务', score: 1 },
          { key: 'B', text: '适合在他人安排下稳定执行', score: 2 },
          { key: 'C', text: '适合承担有一定挑战的任务', score: 3 },
          { key: 'D', text: '适合在不确定环境下推动方向和团队前进', score: 4 }
        ]
      }
    ]
  },
  {
    id: 'entrepreneurial-interest',
    category: '创业测评',
    title: '创业兴趣测评',
    description: '评估学生对创新问题、产品设计、市场验证、用户研究和项目实践的兴趣倾向。',
    duration: 10,
    totalQuestions: 10,
    isReal: true,
    resultDimensions: ['问题意识', '产品兴趣', '市场兴趣', '实践意愿', '创业热情'],
    questions: [
      {
        id: 'Q1',
        dimension: '问题意识',
        stem: '你对发现生活中的未被满足需求这件事：',
        options: [
          { key: 'A', text: '很少关注', score: 1 },
          { key: 'B', text: '偶尔会注意，但不会深入', score: 2 },
          { key: 'C', text: '比较感兴趣，会思考原因', score: 3 },
          { key: 'D', text: '非常感兴趣，经常主动观察和记录', score: 4 }
        ]
      },
      {
        id: 'Q2',
        dimension: '实践意愿',
        stem: '如果有机会参与一个从 0 到 1 的项目，你会：',
        options: [
          { key: 'A', text: '不太想参与，觉得太麻烦', score: 1 },
          { key: 'B', text: '只想做简单明确的部分', score: 2 },
          { key: 'C', text: '愿意参与并学习相关知识', score: 3 },
          { key: 'D', text: '很兴奋，想参与从创意到落地的全过程', score: 4 }
        ]
      },
      {
        id: 'Q3',
        dimension: '市场兴趣',
        stem: '你对用户访谈、问卷调研等工作：',
        options: [
          { key: 'A', text: '没什么兴趣', score: 1 },
          { key: 'B', text: '可以接受，但不主动做', score: 2 },
          { key: 'C', text: '愿意参与，了解用户想法', score: 3 },
          { key: 'D', text: '很感兴趣，喜欢从真实反馈中发现机会', score: 4 }
        ]
      },
      {
        id: 'Q4',
        dimension: '产品兴趣',
        stem: '你对产品原型、功能设计或体验优化：',
        options: [
          { key: 'A', text: '基本不关注', score: 1 },
          { key: 'B', text: '只在需要完成作业时关注', score: 2 },
          { key: 'C', text: '有一定兴趣，愿意提出改进建议', score: 3 },
          { key: 'D', text: '非常感兴趣，经常分析产品为什么好用或不好用', score: 4 }
        ]
      },
      {
        id: 'Q5',
        dimension: '市场兴趣',
        stem: '你对商业模式、盈利方式、市场规模等话题：',
        options: [
          { key: 'A', text: '觉得离自己很远', score: 1 },
          { key: 'B', text: '能听懂一些，但兴趣一般', score: 2 },
          { key: 'C', text: '比较感兴趣，愿意学习', score: 3 },
          { key: 'D', text: '很感兴趣，会主动研究案例和数据', score: 4 }
        ]
      },
      {
        id: 'Q6',
        dimension: '创业热情',
        stem: '你对参加创新创业竞赛的态度是：',
        options: [
          { key: 'A', text: '没有兴趣', score: 1 },
          { key: 'B', text: '如果老师要求或同学邀请，可以参加', score: 2 },
          { key: 'C', text: '愿意参加，积累经验', score: 3 },
          { key: 'D', text: '很想参加，并希望打磨出有竞争力的项目', score: 4 }
        ]
      },
      {
        id: 'Q7',
        dimension: '创业热情',
        stem: '当你看到优秀创业案例时，你通常会：',
        options: [
          { key: 'A', text: '看过就算了', score: 1 },
          { key: 'B', text: '只关注结果是否成功', score: 2 },
          { key: 'C', text: '会思考它解决了什么问题', score: 3 },
          { key: 'D', text: '会分析其用户、产品、商业模式和成长路径', score: 4 }
        ]
      },
      {
        id: 'Q8',
        dimension: '实践意愿',
        stem: '你对把专业知识转化为实际应用：',
        options: [
          { key: 'A', text: '兴趣不大', score: 1 },
          { key: 'B', text: '觉得有意义，但不知道怎么做', score: 2 },
          { key: 'C', text: '愿意尝试做课程项目或竞赛项目', score: 3 },
          { key: 'D', text: '非常感兴趣，希望形成真实产品或服务', score: 4 }
        ]
      },
      {
        id: 'Q9',
        dimension: '产品兴趣',
        stem: '你对团队共创、头脑风暴这类活动：',
        options: [
          { key: 'A', text: '不太喜欢', score: 1 },
          { key: 'B', text: '可以参加，但不常主动发言', score: 2 },
          { key: 'C', text: '愿意参与并提出想法', score: 3 },
          { key: 'D', text: '很喜欢，能从交流中产生新灵感', score: 4 }
        ]
      },
      {
        id: 'Q10',
        dimension: '创业热情',
        stem: '未来如果有一个创业训练营机会，你会：',
        options: [
          { key: 'A', text: '大概率不会报名', score: 1 },
          { key: 'B', text: '看时间和要求再决定', score: 2 },
          { key: 'C', text: '如果内容适合，会考虑参加', score: 3 },
          { key: 'D', text: '很愿意参加，并希望获得系统训练和资源链接', score: 4 }
        ]
      }
    ]
  },
  {
    id: 'entrepreneurial-ability',
    category: '创业测评',
    title: '创业能力测评',
    description: '评估学生的问题分析、资源整合、执行推进、学习迭代和表达展示能力。',
    duration: 10,
    totalQuestions: 10,
    isReal: true,
    resultDimensions: ['问题分析', '资源整合', '执行推进', '学习迭代', '表达展示'],
    questions: [
      {
        id: 'Q1',
        dimension: '问题分析',
        stem: '当你接到一个开放式项目任务时，你通常会：',
        options: [
          { key: 'A', text: '不知道从哪里开始', score: 1 },
          { key: 'B', text: '先等别人给出方向', score: 2 },
          { key: 'C', text: '尝试拆解任务，列出关键步骤', score: 3 },
          { key: 'D', text: '快速明确目标、路径、资源和时间节点', score: 4 }
        ]
      },
      {
        id: 'Q2',
        dimension: '问题分析',
        stem: '面对复杂问题时，你的分析方式更接近：',
        options: [
          { key: 'A', text: '凭感觉判断', score: 1 },
          { key: 'B', text: '只看表面现象', score: 2 },
          { key: 'C', text: '会区分原因、影响和解决方案', score: 3 },
          { key: 'D', text: '会建立问题框架，并用数据或案例验证判断', score: 4 }
        ]
      },
      {
        id: 'Q3',
        dimension: '资源整合',
        stem: '如果需要为项目寻找资源，你会：',
        options: [
          { key: 'A', text: '不知道可以找谁', score: 1 },
          { key: 'B', text: '只问熟悉的同学', score: 2 },
          { key: 'C', text: '主动联系老师、同学或相关平台', score: 3 },
          { key: 'D', text: '系统梳理资源缺口，并多渠道获取支持', score: 4 }
        ]
      },
      {
        id: 'Q4',
        dimension: '执行推进',
        stem: '你对项目进度管理的能力是：',
        options: [
          { key: 'A', text: '经常忘记节点', score: 1 },
          { key: 'B', text: '需要别人提醒', score: 2 },
          { key: 'C', text: '能按计划完成自己的任务', score: 3 },
          { key: 'D', text: '能制定计划、跟踪进度并推动团队协同完成', score: 4 }
        ]
      },
      {
        id: 'Q5',
        dimension: '学习迭代',
        stem: '当项目需要快速学习新知识时，你会：',
        options: [
          { key: 'A', text: '觉得压力很大，容易放弃', score: 1 },
          { key: 'B', text: '零散搜索资料，效率不高', score: 2 },
          { key: 'C', text: '制定学习清单，并边学边用', score: 3 },
          { key: 'D', text: '快速搭建知识框架，并转化为项目产出', score: 4 }
        ]
      },
      {
        id: 'Q6',
        dimension: '表达展示',
        stem: '你在表达项目方案时通常：',
        options: [
          { key: 'A', text: '很难讲清楚重点', score: 1 },
          { key: 'B', text: '能讲出大概想法，但逻辑不够清晰', score: 2 },
          { key: 'C', text: '能按背景、方案、价值说明清楚', score: 3 },
          { key: 'D', text: '能根据听众调整表达，并突出项目亮点', score: 4 }
        ]
      },
      {
        id: 'Q7',
        dimension: '学习迭代',
        stem: '你对数据或用户反馈的使用方式是：',
        options: [
          { key: 'A', text: '很少使用', score: 1 },
          { key: 'B', text: '只在报告中简单引用', score: 2 },
          { key: 'C', text: '会用来判断方案是否有效', score: 3 },
          { key: 'D', text: '会持续收集、分析，并指导迭代决策', score: 4 }
        ]
      },
      {
        id: 'Q8',
        dimension: '执行推进',
        stem: '当团队出现执行效率低的问题时，你会：',
        options: [
          { key: 'A', text: '接受现状', score: 1 },
          { key: 'B', text: '抱怨但不太改变', score: 2 },
          { key: 'C', text: '提出改进建议', score: 3 },
          { key: 'D', text: '主动优化流程、分工和沟通机制', score: 4 }
        ]
      },
      {
        id: 'Q9',
        dimension: '表达展示',
        stem: '你对商业计划书或路演材料的处理能力是：',
        options: [
          { key: 'A', text: '不太了解结构', score: 1 },
          { key: 'B', text: '能完成基本内容', score: 2 },
          { key: 'C', text: '能围绕痛点、方案、市场、团队进行整理', score: 3 },
          { key: 'D', text: '能系统打磨逻辑、数据、故事线和展示效果', score: 4 }
        ]
      },
      {
        id: 'Q10',
        dimension: '资源整合',
        stem: '如果项目需要在短时间内交付成果，你通常会：',
        options: [
          { key: 'A', text: '容易慌乱，不知道先做什么', score: 1 },
          { key: 'B', text: '先做容易的部分', score: 2 },
          { key: 'C', text: '按重要程度排序，优先完成核心内容', score: 3 },
          { key: 'D', text: '快速明确最小可交付版本，并组织资源集中完成', score: 4 }
        ]
      }
    ]
  },
  {
    id: 'teamwork-ability',
    category: '能力测评',
    title: '团队合作能力测评',
    description: '评估学生在团队沟通、角色协作、冲突处理、责任承担和共同目标推进方面的能力。',
    duration: 10,
    totalQuestions: 10,
    isReal: true,
    resultDimensions: ['团队沟通', '协作意识', '冲突处理', '责任承担', '目标推进'],
    questions: [
      {
        id: 'Q1',
        dimension: '协作意识',
        stem: '当团队开始一个新任务时，你通常会：',
        options: [
          { key: 'A', text: '等别人安排自己做什么', score: 1 },
          { key: 'B', text: '只关注自己感兴趣的部分', score: 2 },
          { key: 'C', text: '主动了解目标和分工', score: 3 },
          { key: 'D', text: '帮助团队明确目标、角色和推进节奏', score: 4 }
        ]
      },
      {
        id: 'Q2',
        dimension: '团队沟通',
        stem: '在团队讨论中，你的表现更接近：',
        options: [
          { key: 'A', text: '很少发言', score: 1 },
          { key: 'B', text: '有想法但不一定表达', score: 2 },
          { key: 'C', text: '能清楚表达自己的观点', score: 3 },
          { key: 'D', text: '能表达观点，也能引导大家聚焦问题', score: 4 }
        ]
      },
      {
        id: 'Q3',
        dimension: '冲突处理',
        stem: '当队友的意见与你不同的时候，你会：',
        options: [
          { key: 'A', text: '避免争论，直接不说了', score: 1 },
          { key: 'B', text: '坚持自己的看法，不太想听解释', score: 2 },
          { key: 'C', text: '听取理由后再判断', score: 3 },
          { key: 'D', text: '帮助团队比较不同方案，形成共同决策', score: 4 }
        ]
      },
      {
        id: 'Q4',
        dimension: '责任承担',
        stem: '如果队友进度明显落后，你通常会：',
        options: [
          { key: 'A', text: '认为那是对方自己的事', score: 1 },
          { key: 'B', text: '等负责人去处理', score: 2 },
          { key: 'C', text: '主动询问是否需要帮助', score: 3 },
          { key: 'D', text: '协调资源，帮助队友解决卡点并保护整体进度', score: 4 }
        ]
      },
      {
        id: 'Q5',
        dimension: '冲突处理',
        stem: '面对团队冲突时，你更可能：',
        options: [
          { key: 'A', text: '回避冲突', score: 1 },
          { key: 'B', text: '站在自己熟悉的人一边', score: 2 },
          { key: 'C', text: '尝试客观沟通，找到问题原因', score: 3 },
          { key: 'D', text: '推动双方回到目标和事实，寻找可执行方案', score: 4 }
        ]
      },
      {
        id: 'Q6',
        dimension: '责任承担',
        stem: '你对团队任务承诺的态度是：',
        options: [
          { key: 'A', text: '如果太忙，可以先放一放', score: 1 },
          { key: 'B', text: '尽量完成，但偶尔会拖延', score: 2 },
          { key: 'C', text: '承诺后会按时完成', score: 3 },
          { key: 'D', text: '不仅完成自己的任务，还会主动同步进度和风险', score: 4 }
        ]
      },
      {
        id: 'Q7',
        dimension: '目标推进',
        stem: '当团队成果需要统一风格或质量时，你会：',
        options: [
          { key: 'A', text: '只管自己部分', score: 1 },
          { key: 'B', text: '简单合并，不太检查整体效果', score: 2 },
          { key: 'C', text: '会检查自己部分是否和整体一致', score: 3 },
          { key: 'D', text: '主动推动统一标准，提升整体质量', score: 4 }
        ]
      },
      {
        id: 'Q8',
        dimension: '协作意识',
        stem: '你在团队中的角色通常是：',
        options: [
          { key: 'A', text: '被动执行者', score: 1 },
          { key: 'B', text: '完成分配任务的人', score: 2 },
          { key: 'C', text: '稳定贡献者', score: 3 },
          { key: 'D', text: '协调推动者或关键问题解决者', score: 4 }
        ]
      },
      {
        id: 'Q9',
        dimension: '目标推进',
        stem: '当团队需要做出取舍时，你会：',
        options: [
          { key: 'A', text: '不太参与决策', score: 1 },
          { key: 'B', text: '只考虑自己的工作量', score: 2 },
          { key: 'C', text: '根据目标和资源提出建议', score: 3 },
          { key: 'D', text: '综合目标、风险、时间和成员状态，推动合理取舍', score: 4 }
        ]
      },
      {
        id: 'Q10',
        dimension: '团队沟通',
        stem: '你认为好的团队合作最重要的是：',
        options: [
          { key: 'A', text: '每个人只完成自己的任务', score: 1 },
          { key: 'B', text: '队长安排清楚，其他人执行', score: 2 },
          { key: 'C', text: '成员之间及时沟通、互相配合', score: 3 },
          { key: 'D', text: '共同目标清晰、责任透明、反馈及时、相互成就', score: 4 }
        ]
      }
    ]
  }
]

export function getQuestionnaireById(id) {
  return realQuestionnaires.find(q => q.id === id) || null
}

export function getQuestionnaireIds() {
  return realQuestionnaires.map(q => q.id)
}

export function validateQuestionnaire(questionnaire) {
  if (!questionnaire) return false
  if (!questionnaire.isReal) return true
  if (!Array.isArray(questionnaire.questions)) return false
  if (questionnaire.questions.length !== 10) return false
  return questionnaire.questions.every((q) => {
    if (!q.options || !Array.isArray(q.options)) return false
    if (q.options.length !== 4) return false
    const keys = q.options.map(item => item.key).join('')
    return keys === 'ABCD'
  })
}

export function validateAllQuestionnaires() {
  const results = []
  const allReal = realQuestionnaires.filter(q => q.isReal)
  if (allReal.length !== 5) {
    results.push(`期望 5 个真实问卷，实际找到 ${allReal.length} 个`)
  }
  allReal.forEach(q => {
    if (q.questions.length !== 10) {
      results.push(`${q.title}: 题目数量为 ${q.questions.length}，期望 10`)
    }
    q.questions.forEach((question) => {
      if (!question.options || question.options.length !== 4) {
        results.push(`${q.title} / ${question.id}: 选项数量为 ${question.options?.length || 0}，期望 4`)
      } else {
        const keys = question.options.map(o => o.key).join('')
        if (keys !== 'ABCD') {
          results.push(`${q.title} / ${question.id}: 选项 key 为 "${keys}"，期望 "ABCD"`)
        }
        question.options.forEach((opt) => {
          if (typeof opt.score !== 'number') {
            results.push(`${q.title} / ${question.id} / 选项 ${opt.key}: score 不是数字类型`)
          }
        })
      }
    })
  })
  return results
}