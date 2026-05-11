import innovationPoster from '@/assets/images/Off-campus_competitions/中国国际大学生创新大赛.png'
import challengePoster from '@/assets/images/Off-campus_competitions/“挑战杯”中国大学生创业计划竞赛.png'
import ecommercePoster from '@/assets/images/Off-campus_competitions/全国大学生电子商务“创新、创意及创业”挑战赛.png'

export const externalCompetitions = [
  {
    slug: 'china-international-college-student-innovation-competition',
    title: '中国国际大学生创新大赛',
    shortTitle: '中国国际大学生创新大赛',
    organizer: '教育部等部门与承办地政府',
    level: '国家级',
    category: '创新创业',
    statusText: '2026 备赛关注中',
    timeText: '2026 年 5-10 月，具体以官网通知为准',
    officialUrl: 'https://cy.ncss.cn/',
    posterImage: innovationPoster,
    coverGradient: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 50%, #db2777 100%)',
    tags: ['教育部', '创新创业', '高教主赛道', '红旅赛道', '产业赛道'],
    summary: '面向高校学生和毕业五年内校友的综合性创新创业赛事，强调新工科、新医科、新农科、新文科与产业需求结合。',
    tracks: [
      '高教主赛道：本科生组、研究生组，含创意组与创业组',
      '青年红色筑梦之旅赛道：公益组、创意组、创业组',
      '产业赛道：围绕企业命题和产业需求开展项目',
      '职教赛道、萌芽赛道等按当年通知执行'
    ],
    schedule: [
      { name: '参赛报名', date: '通常 4-7 月 / 2026 以官方通知为准', desc: '团队通过全国大学生创业服务网或学校指定系统报名' },
      { name: '校级初赛', date: '通常 4-8 月', desc: '学校组织网评、路演或排位赛，择优推荐省赛' },
      { name: '省级复赛', date: '通常 6-9 月', desc: '各省组织复赛并推荐总决赛项目' },
      { name: '全国总决赛', date: '通常 9-10 月', desc: '展示、答辩、评审并产生国家级奖项' }
    ],
    awards: [
      '高教主赛道、红旅赛道、职教赛道、产业赛道通常设置金奖、银奖、铜奖',
      '萌芽赛道通常设置创新潜力奖',
      '金奖项目指导教师可能获得优秀创新创业导师等荣誉'
    ],
    requirements: [
      '以团队为单位报名，项目只能选择一个符合要求的赛道',
      '项目须真实、健康、合法，知识产权清晰',
      '已获往年总决赛金奖、银奖的项目通常不可重复报名',
      '参赛人员年龄、学籍、毕业年限以当年通知为准'
    ],
    materials: ['项目展示 PPT', '项目计划书或申报材料', '知识产权/工商注册等佐证材料，如有']
  },
  {
    slug: 'challenge-cup-business-plan',
    title: '"挑战杯"中国大学生创业计划竞赛',
    shortTitle: '挑战杯创业计划竞赛',
    organizer: '共青团中央、中国科协、教育部、全国学联等',
    level: '国家级',
    category: '创业计划',
    statusText: '2026 第十五届备赛中',
    timeText: '两年一届，2026 赛程以官网和学校通知为准',
    officialUrl: 'https://www.tiaozhanbei.net/',
    posterImage: challengePoster,
    coverGradient: 'linear-gradient(135deg, #0891b2 0%, #0d9488 50%, #059669 100%)',
    tags: ['挑战杯', '创业计划书', '国家级', '团队赛'],
    summary: '引导大学生围绕社会需求、产业转型和商业模式创新形成创业计划书，并通过书面评审、答辩和展示评出优秀项目。',
    tracks: [
      '科技创新和未来产业',
      '乡村振兴和农业农村现代化',
      '生态文明建设和绿色低碳发展',
      '文化创意和区域交流合作',
      '社会治理和公共服务'
    ],
    schedule: [
      { name: '校级初赛', date: '通常由各高校在春季组织', desc: '学校遴选项目进入省级复赛' },
      { name: '省级复赛', date: '以各省团委/学校通知为准', desc: '省级组织资格审查、评审和推荐' },
      { name: '全国决赛', date: '以当届官网通知为准', desc: '综合评定项目社会价值、实践过程、创新意义、发展前景和团队协作' }
    ],
    awards: [
      '全国决赛通常设置金奖、银奖、铜奖',
      '学校集体奖包括"挑战杯"和"优胜杯"等',
      '部分专项赛或地方赛可能另设特等奖、一等奖、二等奖、三等奖'
    ],
    requirements: [
      '参赛项目应有较高立意，符合政策导向和法律法规',
      '普通高校和职业院校按规则分类申报',
      '以团队形式参赛，团队人数和指导教师数量按当届规则执行',
      '不得侵犯知识产权，不得借用他人项目参赛',
      '已获往届相关赛事全国金奖/银奖的项目通常不可重复报名'
    ],
    materials: ['创业计划书', '项目展示 PPT', '佐证材料', '知识产权或工商注册证明材料，如有']
  },
  {
    slug: '3chuang-ecommerce-competition',
    title: '全国大学生电子商务"创新、创意及创业"挑战赛',
    shortTitle: '三创赛',
    organizer: '全国电子商务产教融合创新联盟、西安交通大学等',
    level: '国家级',
    category: '电子商务',
    statusText: '第十六届进行中',
    timeText: '团队注册报名通常在前一年 10 月至次年 1 月，校赛通常 3-4 月',
    officialUrl: 'https://www.3chuang.net/',
    posterImage: ecommercePoster,
    coverGradient: 'linear-gradient(135deg, #dc2626 0%, #ea580c 50%, #f59e0b 100%)',
    tags: ['电子商务', '三创赛', '常规赛', '实战赛', '团队赛'],
    summary: '面向在校大学生的电子商务类创新创业赛事，强调创新意识、创意思维、创业能力和团队协同实战精神。',
    tracks: [
      '常规赛',
      '实战赛',
      '国际赛',
      '实战赛方向可包含跨境电商、商务大数据、乡村振兴、直播电商、AI 电商、文旅电商等，具体以当届指南为准'
    ],
    schedule: [
      { name: '团队注册报名', date: '通常 10 月-次年 1 月', desc: '队长在三创赛官网注册团队并通过规则测试' },
      { name: '校赛', date: '通常 3-4 月', desc: '学校组织校级选拔并推荐省赛' },
      { name: '省级赛', date: '通常 4-6 月', desc: '省级选拔赛择优推荐国赛' },
      { name: '全国总决赛', date: '通常 7-8 月', desc: '按常规赛、实战赛等类别组织国赛' }
    ],
    awards: [
      '校赛、省级赛、国赛通常设置特等奖、一等奖、二等奖',
      '常规赛国赛可另设最佳创新奖、最佳创意奖、最佳创业奖',
      '证书由三创赛竞组委系统统一生成'
    ],
    requirements: [
      '参赛学生为全日制在校大学生，专科、本科、研究生均可，专业不限',
      '团队通常由 3-5 名学生组成，其中 1 名队长',
      '可配 0-2 名高校指导老师和 0-2 名企业指导老师',
      '可跨校组队，以队长所在高校参加校赛',
      '参赛项目信息、团队组成在校赛开始后通常不可增加或修改'
    ],
    materials: ['项目报告书', '路演 PPT', '参赛团队承诺书', '指导老师承诺书', '实战赛知情书或授权协议，如有']
  }
]

export function getCompetitionBySlug(slug) {
  return externalCompetitions.find(c => c.slug === slug) || null
}

export const externalCategories = [
  { label: '全部', value: 'all' },
  { label: '创新创业', value: '创新创业' },
  { label: '创业计划', value: '创业计划' },
  { label: '电子商务', value: '电子商务' }
]