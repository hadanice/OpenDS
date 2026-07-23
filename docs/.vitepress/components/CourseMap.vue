<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'

type PathId = 'math' | 'statistics' | 'systems' | 'intelligence' | 'application'

interface KnowledgePath {
  id: PathId
  number: string
  title: string
  color: string
}

interface KnowledgeNode {
  id: string
  title: string
  code: string
  x: number
  y: number
  paths: PathId[]
  href?: string
}

interface KnowledgeEdge {
  from: string
  to: string
  paths: PathId[]
}

interface ModuleCourse {
  title: string
  code: string
  credits: number
  term: string
  href?: string
  siteCode?: string
  group?: '理医工' | '社会科学'
}

interface ModuleGroup {
  id: string
  number: string
  title: string
  kicker: string
  courses: ModuleCourse[]
}

const knowledgePaths: KnowledgePath[] = [
  { id: 'math', number: '01', title: '数理基础', color: '#b27432' },
  { id: 'statistics', number: '02', title: '统计推断', color: '#18756f' },
  { id: 'systems', number: '03', title: '算法系统', color: '#4d7198' },
  { id: 'intelligence', number: '04', title: '智能方法', color: '#765a9b' },
  { id: 'application', number: '05', title: '领域应用', color: '#9a5e61' }
]

const knowledgeNodes: KnowledgeNode[] = [
  { id: 'analysis', title: '数学分析 B I—II', code: 'MATH10012 · 10013', x: 8, y: 19, paths: ['math', 'statistics'] },
  { id: 'linear', title: '线性代数', code: 'CS10003', x: 8, y: 50, paths: ['math', 'intelligence'] },
  { id: 'programming', title: '程序设计', code: 'CS10004', x: 8, y: 81, paths: ['systems', 'intelligence'] },

  { id: 'advanced-linear', title: '高等线性代数', code: 'MATH10003', x: 29, y: 19, paths: ['math', 'intelligence'], href: '/notes/advanced-linear-algebra/' },
  { id: 'probability', title: '概率论基础', code: 'STAT20011', x: 29, y: 50, paths: ['statistics', 'intelligence', 'application'], href: '/notes/probability/' },
  { id: 'algorithms', title: '算法与数据结构', code: 'CS20017h', x: 29, y: 81, paths: ['systems', 'intelligence'], href: '/notes/algorithms/' },

  { id: 'numerical', title: '数值算法 I', code: 'MATH20007', x: 50, y: 11, paths: ['math', 'intelligence', 'application'], href: '/notes/numerical-algorithms/' },
  { id: 'math-statistics', title: '统计学基础 I', code: 'STAT20010h', x: 50, y: 36, paths: ['statistics', 'intelligence', 'application'], href: '/notes/mathematical-statistics/' },
  { id: 'computer-systems', title: '计算机原理', code: 'CS20018', x: 50, y: 64, paths: ['systems', 'intelligence'], href: '/notes/computer-systems/' },
  { id: 'database', title: '数据库及实现', code: 'CS20019', x: 50, y: 88, paths: ['systems', 'application'], href: '/notes/database/' },

  { id: 'optimization', title: '最优化方法', code: 'MATH20008', x: 71, y: 10, paths: ['math', 'statistics', 'intelligence'], href: '/notes/optimization/' },
  { id: 'stat-computing', title: '统计计算', code: 'STAT30016h', x: 71, y: 29, paths: ['statistics', 'intelligence'] },
  { id: 'stat-learning', title: '统计（机器）学习', code: 'STAT30015', x: 71, y: 48, paths: ['math', 'statistics', 'intelligence', 'application'] },
  { id: 'artificial-intelligence', title: '人工智能', code: 'CS50020', x: 71, y: 68, paths: ['systems', 'intelligence'] },
  { id: 'nlp', title: 'NLP 与大语言模型', code: 'CS40008', x: 71, y: 88, paths: ['systems', 'intelligence', 'application'], href: '/notes/nlp-llms/' },

  { id: 'image', title: '图像处理与可视化', code: 'CS30065', x: 92, y: 10, paths: ['intelligence', 'application'] },
  { id: 'biostatistics', title: '生物统计学', code: 'STAT50025', x: 92, y: 29, paths: ['statistics', 'application'], href: '/notes/biostatistics/' },
  { id: 'graph-mining', title: '图数据管理与挖掘', code: 'CS50027', x: 92, y: 48, paths: ['systems', 'application'] },
  { id: 'deep-learning', title: '神经网络与深度学习', code: 'CS30064', x: 92, y: 68, paths: ['intelligence', 'application'] },
  { id: 'research', title: '项目 · 实习 · 毕业论文', code: 'PRACTICE', x: 92, y: 88, paths: ['math', 'statistics', 'systems', 'intelligence', 'application'] }
]

const knowledgeEdges: KnowledgeEdge[] = [
  { from: 'analysis', to: 'advanced-linear', paths: ['math'] },
  { from: 'linear', to: 'advanced-linear', paths: ['math', 'intelligence'] },
  { from: 'advanced-linear', to: 'numerical', paths: ['math', 'intelligence'] },
  { from: 'numerical', to: 'optimization', paths: ['math', 'intelligence'] },
  { from: 'optimization', to: 'stat-learning', paths: ['math', 'statistics', 'intelligence'] },
  { from: 'stat-learning', to: 'research', paths: ['math', 'statistics', 'application'] },

  { from: 'analysis', to: 'probability', paths: ['statistics'] },
  { from: 'probability', to: 'math-statistics', paths: ['statistics', 'intelligence', 'application'] },
  { from: 'math-statistics', to: 'stat-computing', paths: ['statistics', 'intelligence'] },
  { from: 'stat-computing', to: 'stat-learning', paths: ['statistics', 'intelligence'] },
  { from: 'math-statistics', to: 'biostatistics', paths: ['statistics', 'application'] },
  { from: 'biostatistics', to: 'research', paths: ['statistics', 'application'] },

  { from: 'programming', to: 'algorithms', paths: ['systems', 'intelligence'] },
  { from: 'algorithms', to: 'computer-systems', paths: ['systems', 'intelligence'] },
  { from: 'algorithms', to: 'database', paths: ['systems'] },
  { from: 'computer-systems', to: 'artificial-intelligence', paths: ['systems', 'intelligence'] },
  { from: 'database', to: 'graph-mining', paths: ['systems', 'application'] },
  { from: 'database', to: 'nlp', paths: ['systems', 'application'] },
  { from: 'artificial-intelligence', to: 'nlp', paths: ['systems', 'intelligence'] },
  { from: 'graph-mining', to: 'research', paths: ['systems', 'application'] },
  { from: 'nlp', to: 'research', paths: ['systems', 'intelligence', 'application'] },

  { from: 'advanced-linear', to: 'optimization', paths: ['intelligence'] },
  { from: 'math-statistics', to: 'stat-learning', paths: ['intelligence'] },
  { from: 'algorithms', to: 'artificial-intelligence', paths: ['intelligence'] },
  { from: 'stat-learning', to: 'nlp', paths: ['intelligence', 'application'] },
  { from: 'stat-learning', to: 'deep-learning', paths: ['intelligence', 'application'] },
  { from: 'artificial-intelligence', to: 'deep-learning', paths: ['intelligence'] },
  { from: 'numerical', to: 'image', paths: ['intelligence', 'application'] },
  { from: 'image', to: 'research', paths: ['intelligence', 'application'] },
  { from: 'deep-learning', to: 'research', paths: ['intelligence', 'application'] }
]

const modules: ModuleGroup[] = [
  {
    id: 'core',
    number: '01',
    title: '专业核心',
    kicker: 'Common foundation',
    courses: [
      { title: '统计计算', code: 'STAT30016', siteCode: '修读 STAT30016h', credits: 3, term: '第 5 学期' },
      { title: '数值算法与案例分析 I', code: 'MATH20007', credits: 3, term: '第 3 学期', href: '/notes/numerical-algorithms/' },
      { title: '统计（机器）学习概论', code: 'STAT30015', credits: 3, term: '第 5 学期' },
      { title: '人工智能', code: 'CS50020', credits: 3, term: '第 5 学期' },
      { title: '神经网络与深度学习', code: 'CS30064', credits: 3, term: '第 6 学期' },
      { title: '生产实习', code: 'STAT40004', credits: 1, term: '第 7 学期' },
      { title: '毕业论文', code: 'STAT40005', credits: 6, term: '第 8 学期' },
      { title: '数据结构', code: 'CS20017', siteCode: '站内 CS20017h', credits: 4, term: '第 3 学期', href: '/notes/algorithms/' },
      { title: '概率论基础', code: 'STAT20011', credits: 3, term: '第 3 学期', href: '/notes/probability/' },
      { title: '计算机原理', code: 'CS20018', credits: 3, term: '第 3 学期', href: '/notes/computer-systems/' },
      { title: '最优化方法', code: 'MATH20008', credits: 3, term: '第 4 学期', href: '/notes/optimization/' },
      { title: '数据库及实现', code: 'CS20019', credits: 3, term: '第 4 学期', href: '/notes/database/' },
      { title: '高等线性代数', code: 'MATH10003', credits: 3, term: '第 3 学期', href: '/notes/advanced-linear-algebra/' },
      { title: '图像处理与可视化', code: 'CS30065', credits: 3, term: '第 5 学期' },
      { title: '统计学基础：原理、方法及 R 应用 (I)', code: 'STAT20010', siteCode: '站内 STAT20010h', credits: 3, term: '第 4 学期', href: '/notes/mathematical-statistics/' }
    ]
  },
  {
    id: 'statistics',
    number: '02',
    title: '统计与分析',
    kicker: 'Statistics & analysis',
    courses: [
      { title: '数值算法与案例分析 II', code: 'MATH50009', credits: 3, term: '第 4 / 6 学期' },
      { title: '随机过程导论', code: 'STAT50017', credits: 3, term: '第 4 / 6 学期' },
      { title: '统计学基础 II：回归分析', code: 'STAT50024', credits: 3, term: '第 3 / 5 学期' },
      { title: '时间序列与空间统计', code: 'STAT50016', credits: 3, term: '第 4 / 6 学期' },
      { title: '数据融合与同化', code: 'STAT50019', credits: 3, term: '第 4 / 6 学期' },
      { title: '数学模型', code: 'MATH20009', credits: 3, term: '第 4 / 6 学期' },
      { title: '随机分析', code: 'MATH60033', credits: 3, term: '第 3—6 学期' },
      { title: '运筹学 A', code: 'MATH130019', credits: 3, term: '第 4 / 6 学期' },
      { title: '多元统计分析', code: 'STAT50023', credits: 3, term: '第 4 / 6 学期' },
      { title: '计算方法', code: 'MATH30008', credits: 3, term: '第 3 / 5 学期' },
      { title: '应用泛函分析', code: 'MATH50011', credits: 3, term: '第 3 / 5 学期' },
      { title: '线性规划', code: 'MATH50012', credits: 3, term: '第 4 / 6 学期' },
      { title: '多模态数据同化', code: 'AIS410010', credits: 3, term: '第 4 / 6 学期' },
      { title: '人工智能中的稀疏理论与应用', code: 'AIS631010', credits: 3, term: '第 3 / 5 学期' },
      { title: '高等微积分', code: 'MATH50014', credits: 3, term: '秋季' }
    ]
  },
  {
    id: 'systems',
    number: '03',
    title: '系统与数据挖掘',
    kicker: 'Systems & data mining',
    courses: [
      { title: '大规模分布式系统', code: 'CS50022', credits: 3, term: '第 4 / 6 学期' },
      { title: '高级大数据解析', code: 'CS50021', credits: 3, term: '第 3 / 5 学期' },
      { title: '自然语言处理', code: 'CS50023', siteCode: '站内 CS40008', credits: 3, term: '第 4 / 6 学期', href: '/notes/nlp-llms/' },
      { title: '计算理论', code: 'CS50024', credits: 3, term: '第 3 / 5 学期' },
      { title: '数字图像处理', code: 'DATA130032', credits: 3, term: '第 3—6 学期' },
      { title: '图数据管理与挖掘', code: 'CS50027', credits: 3, term: '第 3 / 5 学期' },
      { title: '强化学习算法与理论基础', code: 'MATH50013', credits: 3, term: '第 3 / 5 学期' },
      { title: '算法设计与分析', code: 'CS30016', credits: 3, term: '第 4 / 6 学期' },
      { title: '计算机视觉', code: 'CS50028', credits: 3, term: '第 4 / 6 学期' },
      { title: '认知智能前沿技术与实践', code: 'AIT531023', credits: 3, term: '第 3 / 5 学期' }
    ]
  },
  {
    id: 'applied',
    number: '04',
    title: '理医工 × 社会科学',
    kicker: 'Applied data science',
    courses: [
      { title: '卫生统计学 A', code: 'PHPM40014', credits: 3, term: '第 3 / 5 学期', group: '理医工' },
      { title: '医疗大数据统计学', code: 'STAT50020', credits: 3, term: '第 4 / 6 学期', group: '理医工' },
      { title: '医学图像处理', code: 'CS50026', credits: 3, term: '第 4 / 6 学期', group: '理医工' },
      { title: '生物统计学', code: 'STAT50025', credits: 3, term: '第 4 / 6 学期', group: '理医工', href: '/notes/biostatistics/' },
      { title: '组学数据的统计分析和挖掘', code: 'BIOL130112', credits: 2, term: '第 3 / 5 学期', group: '理医工' },
      { title: '心理统计学（一）', code: 'PSYC30017', credits: 3, term: '第 3 / 5 学期', group: '理医工' },
      { title: '心理统计学（二）', code: 'PSYC30018', credits: 2, term: '第 4 / 6 学期', group: '理医工' },
      { title: '生物医学工程学基础', code: 'BME30003', credits: 3, term: '第 4 / 6 学期', group: '理医工' },
      { title: '社交网络挖掘', code: 'CS50019', credits: 3, term: '第 3 / 5 学期', group: '社会科学' },
      { title: '金融计量学', code: 'STAT50018', credits: 3, term: '第 3 / 5 学期', group: '社会科学' },
      { title: '商务分析', code: 'DATA130035', credits: 3, term: '第 3 / 5 学期', group: '社会科学' },
      { title: '社会数据管理与分析', code: 'DATA130037', credits: 3, term: '第 3—6 学期', group: '社会科学' },
      { title: '决策理论', code: 'DATA130038', credits: 3, term: '第 3 / 5 学期', group: '社会科学' },
      { title: '金融工程', code: 'STAT50022', credits: 3, term: '第 3 / 5 学期', group: '社会科学' },
      { title: '社会科学方法论', code: 'SOCI130062', credits: 2, term: '春 / 秋', group: '社会科学' },
      { title: '社会科学数据挖掘', code: 'STAT50021', credits: 3, term: '第 4 / 6 学期', group: '社会科学' },
      { title: '大数据传播与新媒体分析', code: 'CS50025', credits: 3, term: '第 4 / 6 学期', group: '社会科学' },
      { title: '金融风险管理与金融工程', code: 'ECON40019', credits: 3, term: '第 6 学期', group: '社会科学' }
    ]
  }
]

const activeScene = ref(0)
const activePathId = ref<PathId>('statistics')
const activeModuleId = ref('core')
const graph = ref<HTMLElement | null>(null)
const graphSize = ref({ width: 1400, height: 540 })
const touchStartY = ref(0)

const nodeMap = new Map(knowledgeNodes.map((node) => [node.id, node]))
const activePath = computed(() => knowledgePaths.find((path) => path.id === activePathId.value) ?? knowledgePaths[0])
const activeNodes = computed(() => knowledgeNodes.filter((node) => node.paths.includes(activePathId.value)))
const activeEdges = computed(() => knowledgeEdges.filter((edge) => edge.paths.includes(activePathId.value)))
const activeModule = computed(() => modules.find((module) => module.id === activeModuleId.value) ?? modules[0])

const courseHref = (href?: string) => href ? withBase(href) : undefined
const nodeStyle = (node: KnowledgeNode) => ({ left: `${node.x}%`, top: `${node.y}%` })
const edgeStyle = (edge: KnowledgeEdge) => {
  const from = nodeMap.get(edge.from)!
  const to = nodeMap.get(edge.to)!
  const x1 = graphSize.value.width * from.x / 100
  const y1 = graphSize.value.height * from.y / 100
  const x2 = graphSize.value.width * to.x / 100
  const y2 = graphSize.value.height * to.y / 100
  const distance = Math.hypot(x2 - x1, y2 - y1)
  const angle = Math.atan2(y2 - y1, x2 - x1)

  return {
    left: `${x1}px`,
    top: `${y1}px`,
    width: `${distance}px`,
    transform: `rotate(${angle}rad)`
  }
}

let wheelLocked = false
let wheelTimer: ReturnType<typeof setTimeout> | undefined
let pathTimer: ReturnType<typeof setInterval> | undefined
let pathResumeTimer: ReturnType<typeof setTimeout> | undefined
let resizeObserver: ResizeObserver | undefined

const goToScene = (index: number) => {
  const next = Math.min(1, Math.max(0, index))
  if (next === activeScene.value) return
  activeScene.value = next
  wheelLocked = true
  if (wheelTimer) clearTimeout(wheelTimer)
  wheelTimer = setTimeout(() => { wheelLocked = false }, 780)
}

const handleWheel = (event: WheelEvent) => {
  if (wheelLocked || Math.abs(event.deltaY) < 16) return
  goToScene(event.deltaY > 0 ? activeScene.value + 1 : activeScene.value - 1)
}

const handleKey = (event: KeyboardEvent) => {
  if (['ArrowDown', 'PageDown', ' '].includes(event.key)) {
    event.preventDefault()
    goToScene(activeScene.value + 1)
  }
  if (['ArrowUp', 'PageUp'].includes(event.key)) {
    event.preventDefault()
    goToScene(activeScene.value - 1)
  }
}

const handleTouchStart = (event: TouchEvent) => {
  touchStartY.value = event.changedTouches[0]?.clientY ?? 0
}

const handleTouchEnd = (event: TouchEvent) => {
  const delta = touchStartY.value - (event.changedTouches[0]?.clientY ?? touchStartY.value)
  if (Math.abs(delta) < 44) return
  goToScene(delta > 0 ? activeScene.value + 1 : activeScene.value - 1)
}

const startPathCycle = () => {
  if (pathTimer || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  pathTimer = setInterval(() => {
    if (activeScene.value !== 0) return
    const current = knowledgePaths.findIndex((path) => path.id === activePathId.value)
    activePathId.value = knowledgePaths[(current + 1) % knowledgePaths.length].id
  }, 5200)
}

const selectPath = (id: PathId) => {
  activePathId.value = id
  if (pathTimer) clearInterval(pathTimer)
  if (pathResumeTimer) clearTimeout(pathResumeTimer)
  pathTimer = undefined
  pathResumeTimer = setTimeout(startPathCycle, 12000)
}

onMounted(() => {
  if (graph.value) {
    resizeObserver = new ResizeObserver(([entry]) => {
      graphSize.value = {
        width: entry.contentRect.width,
        height: entry.contentRect.height
      }
    })
    resizeObserver.observe(graph.value)
  }
  startPathCycle()
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  if (wheelTimer) clearTimeout(wheelTimer)
  if (pathTimer) clearInterval(pathTimer)
  if (pathResumeTimer) clearTimeout(pathResumeTimer)
})
</script>

<template>
  <main
    class="course-map-deck"
    tabindex="0"
    aria-label="两幕课程地图"
    @wheel.prevent="handleWheel"
    @keydown="handleKey"
    @touchstart.passive="handleTouchStart"
    @touchend.passive="handleTouchEnd"
  >
    <nav class="scene-progress" aria-label="课程地图页面">
      <button
        v-for="index in 2"
        :key="index"
        type="button"
        :class="{ 'is-active': activeScene === index - 1 }"
        :aria-label="`前往第 ${index} 幕`"
        :aria-current="activeScene === index - 1 ? 'step' : undefined"
        @click="goToScene(index - 1)"
      >
        <span>0{{ index }}</span><i />
      </button>
    </nav>

    <div
      class="map-story__track"
      :style="{ transform: `translateY(-${activeScene * 50}%)` }"
    >
      <section class="map-scene map-scene--knowledge">
        <div class="scene-frame">
          <header class="compact-header">
            <div class="compact-header__identity">
              <a :href="withBase('/courses/')">← 课程入口</a>
              <div><small>Knowledge pathways · 01</small><h1>知识承接图</h1></div>
            </div>
            <div class="path-switcher" role="tablist" aria-label="选择知识路径">
              <button
                v-for="path in knowledgePaths"
                :key="path.id"
                type="button"
                role="tab"
                :aria-selected="activePathId === path.id"
                :class="{ 'is-active': activePathId === path.id }"
                :style="{ '--path-color': path.color }"
                @click="selectPath(path.id)"
              >
                <span>{{ path.number }}</span>{{ path.title }}
              </button>
            </div>
          </header>

          <div
            ref="graph"
            class="knowledge-graph"
            :style="{ '--path-color': activePath.color }"
            role="tabpanel"
            :aria-label="`${activePath.title}知识路径`"
          >
            <div class="graph-columns" aria-hidden="true">
              <span v-for="label in ['基础语言', '核心工具', '建模与系统', '专业方法', '应用与研究']" :key="label">
                {{ label }}
              </span>
            </div>

            <TransitionGroup name="edge-fade" tag="div" class="edge-layer">
              <span
                v-for="edge in activeEdges"
                :key="`${activePathId}-${edge.from}-${edge.to}`"
                class="knowledge-edge"
                :style="edgeStyle(edge)"
                aria-hidden="true"
              ><i /></span>
            </TransitionGroup>

            <TransitionGroup name="node-fade" tag="div" class="node-layer">
              <component
                :is="node.href ? 'a' : 'article'"
                v-for="(node, index) in activeNodes"
                :key="`${activePathId}-${node.id}`"
                class="knowledge-node"
                :class="{ 'has-notes': node.href }"
                :href="courseHref(node.href)"
                :style="{ ...nodeStyle(node), '--node-delay': `${index * 34}ms` }"
              >
                <strong>{{ node.title }}</strong>
                <small>{{ node.code }}</small>
                <i v-if="node.href">↗</i>
              </component>
            </TransitionGroup>

            <div class="path-status" aria-hidden="true">
              <span :style="{ background: activePath.color }" />
              {{ activePath.title }}路线
            </div>
          </div>

          <button class="scene-hint" type="button" @click="goToScene(1)">
            滚轮 / 下滑查看方向模块 <span>↓</span>
          </button>
        </div>
      </section>

      <section class="map-scene map-scene--modules">
        <div class="scene-frame">
          <header class="compact-header compact-header--modules">
            <div class="compact-header__identity">
              <div><small>Professional pathways · 02</small><h2>方向模块</h2></div>
            </div>
            <div class="module-switcher" role="tablist" aria-label="选择课程模块">
              <button
                v-for="module in modules"
                :key="module.id"
                type="button"
                role="tab"
                :aria-selected="activeModuleId === module.id"
                :class="{ 'is-active': activeModuleId === module.id }"
                @click="activeModuleId = module.id"
              >
                <span>{{ module.number }}</span>{{ module.title }}
                <i>{{ module.courses.length }}</i>
              </button>
            </div>
          </header>

          <section class="module-panel" aria-live="polite">
            <Transition name="module-swap" mode="out-in">
              <div :key="activeModule.id" class="module-panel__body" role="tabpanel">
                <header>
                  <div><small>{{ activeModule.kicker }}</small><h3>{{ activeModule.title }}</h3></div>
                  <span>{{ activeModule.courses.length }} 门</span>
                </header>
                <div class="module-course-grid">
                  <component
                    :is="course.href ? 'a' : 'article'"
                    v-for="course in activeModule.courses"
                    :key="`${activeModule.id}-${course.code}`"
                    class="module-course"
                    :href="courseHref(course.href)"
                  >
                    <div>
                      <em v-if="course.group">{{ course.group }}</em>
                      <code>{{ course.code }}</code>
                      <i v-if="course.href">↗</i>
                    </div>
                    <strong>{{ course.title }}</strong>
                    <small>
                      {{ course.credits }} 学分 · {{ course.term }}
                      <b v-if="course.siteCode">{{ course.siteCode }}</b>
                    </small>
                  </component>
                </div>
              </div>
            </Transition>
          </section>

          <button class="scene-hint" type="button" @click="goToScene(0)">
            <span>↑</span> 上滑返回知识路径
          </button>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
:global(body:has(.course-map-deck)) {
  overflow: hidden;
}

.course-map-deck {
  position: relative;
  height: calc(100dvh - var(--vp-nav-height));
  min-height: 560px;
  overflow: hidden;
  color: var(--vp-c-text-1);
  background: var(--vp-c-bg);
  outline: none;
  overscroll-behavior: none;
  touch-action: pan-x;
}

.map-story__track {
  display: grid;
  grid-template-rows: repeat(2, 50%);
  height: 200%;
  transition: transform .72s cubic-bezier(.22, .78, .22, 1);
  will-change: transform;
}

.map-scene {
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.map-scene--knowledge {
  background:
    linear-gradient(color-mix(in srgb, var(--vp-c-divider) 22%, transparent) 1px, transparent 1px),
    radial-gradient(circle at 9% 15%, color-mix(in srgb, var(--vp-c-brand-1) 12%, transparent), transparent 27%),
    radial-gradient(circle at 91% 78%, rgba(178, 116, 50, .08), transparent 25%),
    var(--vp-c-bg);
  background-size: 100% 45px, auto, auto, auto;
}

.map-scene--modules {
  background:
    radial-gradient(circle at 84% 12%, color-mix(in srgb, var(--vp-c-brand-1) 11%, transparent), transparent 25%),
    radial-gradient(circle at 5% 90%, rgba(178, 116, 50, .08), transparent 24%),
    var(--vp-c-bg-alt);
}

.scene-frame {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  width: min(calc(100% - 76px), 1580px);
  height: 100%;
  margin: 0 auto;
  padding: clamp(18px, 2.4vh, 28px) 0 12px;
}

.compact-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  min-height: 64px;
  margin-bottom: clamp(12px, 1.8vh, 20px);
}

.compact-header__identity {
  display: flex;
  align-items: center;
  flex: none;
  gap: 24px;
}

.compact-header__identity > a {
  color: var(--vp-c-text-2);
  font-size: 12px;
  text-decoration: none;
  transition: color .2s ease, transform .2s ease;
}

.compact-header__identity > a:hover {
  color: var(--vp-c-brand-1);
  transform: translateX(-3px);
}

.compact-header small {
  display: block;
  margin-bottom: 3px;
  color: #b66f20;
  font-size: 9px;
  font-weight: 750;
  letter-spacing: .16em;
  text-transform: uppercase;
}

.compact-header h1,
.compact-header h2 {
  margin: 0;
  border: 0;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, "Noto Serif SC", serif);
  font-size: clamp(24px, 2.4vw, 36px);
  font-weight: 520;
  letter-spacing: -.04em;
  line-height: 1;
}

.path-switcher,
.module-switcher {
  display: flex;
  min-width: 0;
  padding: 4px;
  overflow-x: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  background: color-mix(in srgb, var(--vp-c-bg) 80%, transparent);
  scrollbar-width: none;
}

.path-switcher::-webkit-scrollbar,
.module-switcher::-webkit-scrollbar {
  display: none;
}

.path-switcher button,
.module-switcher button {
  display: inline-flex;
  align-items: center;
  flex: none;
  gap: 7px;
  min-height: 34px;
  padding: 6px 12px;
  border: 0;
  border-radius: 999px;
  color: var(--vp-c-text-2);
  background: transparent;
  cursor: pointer;
  font-size: 11px;
  white-space: nowrap;
  transition: color .2s ease, background .2s ease, box-shadow .2s ease;
}

.path-switcher button span,
.module-switcher button span {
  color: var(--vp-c-text-3);
  font-family: var(--opends-serif, serif);
  font-size: 9px;
}

.path-switcher button.is-active {
  color: white;
  background: var(--path-color);
  box-shadow: 0 7px 18px color-mix(in srgb, var(--path-color) 23%, transparent);
}

.path-switcher button.is-active span {
  color: rgba(255, 255, 255, .72);
}

.knowledge-graph {
  position: relative;
  min-height: 0;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 24px;
  background:
    radial-gradient(circle at center, color-mix(in srgb, var(--path-color) 6%, transparent), transparent 62%),
    color-mix(in srgb, var(--vp-c-bg) 91%, transparent);
  box-shadow: 0 20px 64px rgba(20, 56, 52, .07);
  isolation: isolate;
  transition: background .35s ease;
}

.graph-columns {
  position: absolute;
  inset: 0;
  z-index: -1;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  pointer-events: none;
}

.graph-columns span {
  position: relative;
  padding-top: 13px;
  border-right: 1px solid color-mix(in srgb, var(--vp-c-divider) 62%, transparent);
  color: var(--vp-c-text-3);
  font-size: 9px;
  letter-spacing: .1em;
  text-align: center;
}

.graph-columns span:last-child {
  border-right: 0;
}

.edge-layer,
.node-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.knowledge-edge {
  position: absolute;
  z-index: 1;
  display: block;
  height: 2px;
  transform-origin: 0 50%;
  pointer-events: none;
}

.knowledge-edge::before {
  position: absolute;
  inset: 0;
  border-radius: 999px;
  background: color-mix(in srgb, var(--path-color) 42%, var(--vp-c-divider));
  content: "";
}

.knowledge-edge::after {
  position: absolute;
  top: -2px;
  right: -1px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--path-color);
  box-shadow: 0 0 0 5px color-mix(in srgb, var(--path-color) 10%, transparent);
  content: "";
}

.knowledge-edge i {
  position: absolute;
  z-index: 1;
  inset: 0;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, color-mix(in srgb, var(--path-color) 90%, white), transparent);
  transform: scaleX(0);
  transform-origin: left;
  animation: edge-draw .9s .08s ease forwards, edge-shimmer 3.8s 1s ease-in-out infinite;
}

.knowledge-node {
  position: absolute;
  z-index: 2;
  display: grid;
  place-content: center;
  width: clamp(112px, 9.8vw, 158px);
  min-height: clamp(48px, 6.5vh, 66px);
  padding: 8px 10px;
  border: 1px solid color-mix(in srgb, var(--path-color) 22%, var(--vp-c-divider));
  border-radius: 13px;
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--vp-c-bg) 95%, transparent);
  box-shadow: 0 9px 25px rgba(24, 50, 47, .07);
  pointer-events: auto;
  text-align: center;
  text-decoration: none;
  transform: translate(-50%, -50%);
  transition: border-color .2s ease, color .2s ease, transform .2s ease, box-shadow .2s ease;
}

.knowledge-node.has-notes {
  border-color: color-mix(in srgb, var(--path-color) 56%, var(--vp-c-divider));
}

a.knowledge-node:hover {
  z-index: 3;
  border-color: var(--path-color);
  color: var(--path-color);
  box-shadow: 0 13px 34px color-mix(in srgb, var(--path-color) 15%, transparent);
  transform: translate(-50%, -53%);
}

.knowledge-node strong,
.knowledge-node small {
  display: block;
}

.knowledge-node strong {
  font-size: clamp(10px, .75vw, 12px);
  font-weight: 680;
  line-height: 1.3;
}

.knowledge-node small {
  margin-top: 4px;
  overflow: hidden;
  color: var(--vp-c-text-3);
  font-family: ui-monospace, monospace;
  font-size: clamp(7px, .55vw, 9px);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.knowledge-node > i {
  position: absolute;
  top: 5px;
  right: 7px;
  color: var(--path-color);
  font-size: 9px;
  font-style: normal;
}

.path-status {
  position: absolute;
  z-index: 3;
  right: 14px;
  bottom: 11px;
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--vp-c-text-3);
  font-size: 9px;
  letter-spacing: .08em;
}

.path-status span {
  width: 24px;
  height: 2px;
}

.scene-hint {
  display: inline-flex;
  align-items: center;
  justify-self: center;
  gap: 9px;
  min-height: 28px;
  margin-top: 5px;
  border: 0;
  color: var(--vp-c-text-3);
  background: transparent;
  cursor: pointer;
  font-size: 9px;
  letter-spacing: .08em;
}

.scene-hint span {
  color: var(--vp-c-brand-1);
  font-size: 14px;
  animation: hint-drift 1.8s ease-in-out infinite;
}

.module-switcher button {
  position: relative;
  padding-right: 10px;
}

.module-switcher button > i {
  display: grid;
  place-items: center;
  min-width: 20px;
  height: 20px;
  padding: 0 5px;
  border-radius: 999px;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg-soft);
  font-size: 8px;
  font-style: normal;
}

.module-switcher button.is-active {
  color: white;
  background: var(--vp-c-brand-1);
  box-shadow: 0 7px 18px color-mix(in srgb, var(--vp-c-brand-1) 22%, transparent);
}

.module-switcher button.is-active span,
.module-switcher button.is-active > i {
  color: rgba(255, 255, 255, .76);
}

.module-switcher button.is-active > i {
  background: rgba(255, 255, 255, .13);
}

.module-panel {
  position: relative;
  min-height: 0;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 24px;
  background: color-mix(in srgb, var(--vp-c-bg) 92%, transparent);
  box-shadow: 0 20px 64px rgba(20, 56, 52, .07);
}

.module-panel__body {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  height: 100%;
  padding: clamp(15px, 2vh, 22px);
}

.module-panel__body > header {
  display: flex;
  align-items: end;
  justify-content: space-between;
  min-height: 46px;
  margin-bottom: 10px;
  padding-bottom: 9px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.module-panel__body > header small {
  display: block;
  margin-bottom: 2px;
  color: #b66f20;
  font-size: 8px;
  font-weight: 750;
  letter-spacing: .15em;
  text-transform: uppercase;
}

.module-panel__body > header h3 {
  margin: 0;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, serif);
  font-size: clamp(22px, 2.2vw, 32px);
  font-weight: 520;
  letter-spacing: -.035em;
  line-height: 1;
}

.module-panel__body > header > span {
  color: var(--vp-c-text-3);
  font-size: 10px;
}

.module-course-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  grid-auto-rows: minmax(0, 1fr);
  gap: clamp(5px, .7vh, 8px);
  min-height: 0;
}

.module-course {
  display: grid;
  grid-template-rows: auto auto auto;
  align-content: center;
  min-width: 0;
  min-height: 0;
  padding: clamp(7px, 1vh, 11px) 12px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 11px;
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--vp-c-bg-soft) 66%, transparent);
  text-decoration: none;
  transition: border-color .2s ease, background .2s ease, transform .2s ease;
}

a.module-course:hover {
  border-color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 7%, var(--vp-c-bg));
  transform: translateY(-2px);
}

.module-course > div {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 6px;
}

.module-course code {
  overflow: hidden;
  color: var(--vp-c-text-3);
  font-size: clamp(7px, .55vw, 9px);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.module-course em {
  flex: none;
  padding: 1px 5px;
  border-radius: 999px;
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent);
  font-size: 7px;
  font-style: normal;
}

.module-course > div > i {
  margin-left: auto;
  color: var(--vp-c-brand-1);
  font-size: 9px;
  font-style: normal;
}

.module-course strong {
  display: -webkit-box;
  margin: 4px 0 3px;
  overflow: hidden;
  font-size: clamp(10px, .75vw, 12px);
  font-weight: 680;
  line-height: 1.25;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.module-course > small {
  overflow: hidden;
  color: var(--vp-c-text-3);
  font-size: clamp(7px, .52vw, 9px);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.module-course > small b {
  margin-left: 5px;
  color: var(--vp-c-brand-1);
  font-weight: 520;
}

.scene-progress {
  position: absolute;
  z-index: 10;
  top: 50%;
  right: clamp(9px, 1.4vw, 24px);
  display: grid;
  gap: 14px;
  transform: translateY(-50%);
}

.scene-progress button {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 7px;
  padding: 0;
  border: 0;
  color: var(--vp-c-text-3);
  background: transparent;
  cursor: pointer;
  font-size: 9px;
}

.scene-progress i {
  width: 15px;
  height: 2px;
  background: var(--vp-c-divider);
  transition: width .25s ease, background .25s ease;
}

.scene-progress button.is-active {
  color: var(--vp-c-text-1);
}

.scene-progress button.is-active i {
  width: 29px;
  background: var(--vp-c-brand-1);
}

.node-fade-enter-active {
  animation: node-arrive .45s var(--node-delay) both ease-out;
}

.node-fade-leave-active {
  position: absolute;
  transition: opacity .16s ease, transform .16s ease;
}

.node-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(.94);
}

.edge-fade-enter-active {
  animation: edge-arrive .35s both ease;
}

.edge-fade-leave-active {
  transition: opacity .14s ease;
}

.edge-fade-leave-to {
  opacity: 0;
}

.module-swap-enter-active,
.module-swap-leave-active {
  transition: opacity .2s ease, transform .2s ease;
}

.module-swap-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.module-swap-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@keyframes node-arrive {
  from { opacity: 0; transform: translate(-50%, -50%) scale(.9); }
  to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

@keyframes edge-arrive {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes edge-draw {
  to { transform: scaleX(1); }
}

@keyframes edge-shimmer {
  0%, 100% { opacity: .25; }
  50% { opacity: 1; }
}

@keyframes hint-drift {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(2px); }
}

@media (max-width: 1120px) {
  .scene-frame {
    width: min(calc(100% - 52px), 1580px);
  }

  .compact-header {
    gap: 16px;
  }

  .compact-header__identity {
    gap: 12px;
  }

  .path-switcher button,
  .module-switcher button {
    padding: 5px 8px;
    font-size: 10px;
  }

  .module-course-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .course-map-deck {
    min-height: 520px;
  }

  .scene-frame {
    width: min(calc(100% - 24px), 1580px);
    padding-top: 12px;
  }

  .compact-header {
    display: grid;
    align-content: start;
    gap: 8px;
    min-height: 95px;
    margin-bottom: 8px;
  }

  .compact-header__identity {
    justify-content: space-between;
  }

  .compact-header h1,
  .compact-header h2 {
    font-size: 23px;
  }

  .path-switcher,
  .module-switcher {
    width: 100%;
  }

  .path-switcher button,
  .module-switcher button {
    flex: 1 0 auto;
    min-height: 30px;
    padding: 4px 7px;
    font-size: 9px;
  }

  .knowledge-graph,
  .module-panel {
    border-radius: 17px;
  }

  .graph-columns span {
    padding-top: 8px;
    font-size: 7px;
    letter-spacing: 0;
  }

  .knowledge-node {
    width: clamp(68px, 20vw, 82px);
    min-height: 42px;
    padding: 5px;
    border-radius: 9px;
  }

  .knowledge-node strong {
    display: -webkit-box;
    overflow: hidden;
    font-size: 8px;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
  }

  .knowledge-node small {
    font-size: 6px;
  }

  .path-status {
    display: none;
  }

  .module-panel__body {
    padding: 9px;
  }

  .module-panel__body > header {
    min-height: 36px;
    margin-bottom: 6px;
    padding-bottom: 5px;
  }

  .module-panel__body > header h3 {
    font-size: 19px;
  }

  .module-course-grid {
    gap: 4px;
  }

  .module-course {
    padding: 4px 6px;
    border-radius: 8px;
  }

  .module-course strong {
    margin: 2px 0;
    font-size: 8px;
  }

  .module-course code,
  .module-course > small {
    font-size: 6px;
  }

  .module-course em {
    display: none;
  }

  .scene-progress {
    top: 11px;
    right: 11px;
    grid-auto-flow: column;
    transform: none;
  }

  .scene-progress button span {
    display: none;
  }

  .scene-progress button.is-active i {
    width: 22px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .map-story__track {
    transition: none;
  }

  .knowledge-edge i,
  .scene-hint span,
  .node-fade-enter-active,
  .edge-fade-enter-active {
    animation: none;
  }
}
</style>
