<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { withBase } from 'vitepress'

type Track = 'math' | 'statistics' | 'systems' | 'intelligence' | 'application'
type CourseState = '站内可读' | '仓库资料' | '培养方案'

interface CourseNode {
  id: string
  title: string
  code: string
  term: string
  column: number
  row: number
  tracks: Track[]
  state: CourseState
  href?: string
  external?: boolean
}

interface CourseEdge {
  from: string
  to: string
}

interface EdgePath extends CourseEdge {
  d: string
  active: boolean
}

const repository = 'https://github.com/hadanice/OpenDS/tree/main/'
const repositoryPath = (value: string) => `${repository}${encodeURIComponent(value)}`

const stages = [
  { number: '01—02', title: '数理与编程基础', subtitle: '建立共同语言' },
  { number: '03', title: '核心工具箱', subtitle: '形成计算与推断能力' },
  { number: '04', title: '建模与数据系统', subtitle: '把方法连接到问题' },
  { number: '05—06', title: '智能与专业分流', subtitle: '进入进阶模块' },
  { number: '07—08', title: '实践与研究', subtitle: '把知识变成产出' }
]

const courses: CourseNode[] = [
  { id: 'analysis', title: '数学分析 BⅠ—Ⅱ', code: 'MATH10012 / 13', term: '第 1—2 学期', column: 1, row: 1, tracks: ['math', 'statistics', 'intelligence'], state: '培养方案' },
  { id: 'linear', title: '线性代数', code: 'CS10003', term: '第 1 学期', column: 1, row: 3, tracks: ['math', 'statistics', 'intelligence'], state: '培养方案' },
  { id: 'programming', title: '程序设计', code: 'CS10004', term: '第 1 学期', column: 1, row: 5, tracks: ['systems', 'intelligence'], state: '培养方案' },
  { id: 'physics', title: '大学物理 BⅠ—Ⅱ', code: 'PHYS10003 / 04', term: '第 1—2 学期', column: 1, row: 7, tracks: ['math', 'application'], state: '培养方案' },

  { id: 'advanced-linear', title: '高等线性代数', code: 'MATH10003', term: '25 秋 · 第 3 学期', column: 2, row: 1, tracks: ['math', 'statistics', 'intelligence'], state: '仓库资料', href: repositoryPath('高等线性代数'), external: true },
  { id: 'numerical', title: '数值算法与案例分析Ⅰ', code: 'MATH20007', term: '25 秋 · 第 3 学期', column: 2, row: 2, tracks: ['math', 'statistics', 'application'], state: '仓库资料', href: repositoryPath('数值算法与案例分析Ⅰ'), external: true },
  { id: 'probability', title: '概率论基础', code: 'STAT20011', term: '25 秋 · 第 3 学期', column: 2, row: 3, tracks: ['statistics', 'intelligence', 'application'], state: '站内可读', href: '/notes/probability/' },
  { id: 'algorithms', title: '算法与数据结构', code: 'CS20017h', term: '25 秋 · 第 3 学期', column: 2, row: 5, tracks: ['systems', 'intelligence'], state: '站内可读', href: '/notes/algorithms/' },
  { id: 'computer-systems', title: '计算机原理', code: 'CS20018', term: '25 秋 · 第 3 学期', column: 2, row: 7, tracks: ['systems', 'intelligence'], state: '站内可读', href: '/notes/computer-systems/' },

  { id: 'math-statistics', title: '统计学基础Ⅰ：数理统计', code: 'STAT20010h', term: '26 春 · 第 4 学期', column: 3, row: 1, tracks: ['statistics', 'application'], state: '站内可读', href: '/notes/mathematical-statistics/' },
  { id: 'optimization', title: '最优化方法', code: 'MATH20008', term: '26 春 · 第 4 学期', column: 3, row: 3, tracks: ['math', 'statistics', 'intelligence'], state: '站内可读', href: '/notes/optimization/' },
  { id: 'biostatistics', title: '生物统计学', code: 'STAT50025', term: '26 春 · 第 4/6 学期', column: 3, row: 5, tracks: ['statistics', 'application', 'intelligence'], state: '站内可读', href: '/notes/biostatistics/' },
  { id: 'database', title: '数据库及实现', code: 'CS20019', term: '26 春 · 第 4 学期', column: 3, row: 7, tracks: ['systems', 'intelligence'], state: '站内可读', href: '/notes/database/' },

  { id: 'stat-computing', title: '统计计算', code: 'STAT30016h', term: '26 秋 · 核心课程', column: 4, row: 1, tracks: ['statistics'], state: '培养方案' },
  { id: 'stat-learning', title: '统计（机器）学习概论', code: 'STAT30015', term: '26 秋 · 第 5 学期', column: 4, row: 2, tracks: ['statistics', 'intelligence'], state: '培养方案' },
  { id: 'multimodal', title: '多模态数据同化', code: 'AIS410010', term: '26 秋 · 进阶模块', column: 4, row: 3, tracks: ['statistics', 'application', 'intelligence'], state: '培养方案' },
  { id: 'ai', title: '人工智能', code: 'CS50020', term: '26 秋 · 第 5 学期', column: 4, row: 4, tracks: ['systems', 'intelligence'], state: '培养方案' },
  { id: 'image', title: '图像处理与数据可视化', code: 'CS30065h', term: '26 秋 · 第 5/6 学期', column: 4, row: 5, tracks: ['systems', 'intelligence', 'application'], state: '培养方案' },
  { id: 'graph-mining', title: '图数据管理与挖掘', code: 'CS50027', term: '26 秋 · 系统模块', column: 4, row: 6, tracks: ['systems', 'intelligence'], state: '培养方案' },
  { id: 'nlp', title: '自然语言处理与大语言模型', code: 'CS40008', term: '26 春 · 系统/类脑模块', column: 4, row: 7, tracks: ['systems', 'intelligence'], state: '仓库资料', href: 'https://baojian.github.io/llm-26/', external: true },
  { id: 'deep-learning', title: '神经网络与深度学习', code: 'CS30064', term: '27 春 · 第 6 学期', column: 4, row: 8, tracks: ['intelligence', 'application'], state: '培养方案' },

  { id: 'internship', title: '生产实习', code: 'STAT40004', term: '第 7 学期', column: 5, row: 3, tracks: ['math', 'statistics', 'systems', 'intelligence', 'application'], state: '培养方案' },
  { id: 'thesis', title: '毕业论文', code: 'STAT40005', term: '第 8 学期', column: 5, row: 6, tracks: ['math', 'statistics', 'systems', 'intelligence', 'application'], state: '培养方案' }
]

const edges: CourseEdge[] = [
  { from: 'analysis', to: 'advanced-linear' },
  { from: 'analysis', to: 'numerical' },
  { from: 'analysis', to: 'probability' },
  { from: 'linear', to: 'advanced-linear' },
  { from: 'linear', to: 'numerical' },
  { from: 'programming', to: 'algorithms' },
  { from: 'programming', to: 'computer-systems' },
  { from: 'physics', to: 'numerical' },
  { from: 'advanced-linear', to: 'math-statistics' },
  { from: 'advanced-linear', to: 'optimization' },
  { from: 'numerical', to: 'optimization' },
  { from: 'numerical', to: 'image' },
  { from: 'probability', to: 'math-statistics' },
  { from: 'probability', to: 'biostatistics' },
  { from: 'algorithms', to: 'database' },
  { from: 'algorithms', to: 'ai' },
  { from: 'computer-systems', to: 'database' },
  { from: 'math-statistics', to: 'stat-computing' },
  { from: 'math-statistics', to: 'stat-learning' },
  { from: 'math-statistics', to: 'multimodal' },
  { from: 'optimization', to: 'stat-learning' },
  { from: 'optimization', to: 'ai' },
  { from: 'optimization', to: 'deep-learning' },
  { from: 'biostatistics', to: 'multimodal' },
  { from: 'database', to: 'graph-mining' },
  { from: 'database', to: 'nlp' },
  { from: 'ai', to: 'deep-learning' },
  { from: 'image', to: 'deep-learning' },
  { from: 'stat-learning', to: 'internship' },
  { from: 'multimodal', to: 'internship' },
  { from: 'graph-mining', to: 'internship' },
  { from: 'nlp', to: 'internship' },
  { from: 'deep-learning', to: 'internship' },
  { from: 'internship', to: 'thesis' }
]

const trackOptions: Array<{ value: 'all' | Track; label: string }> = [
  { value: 'all', label: '全景' },
  { value: 'math', label: '数学与优化' },
  { value: 'statistics', label: '统计与分析' },
  { value: 'systems', label: '系统与挖掘' },
  { value: 'application', label: '理医工应用' },
  { value: 'intelligence', label: '类脑与智能' }
]

const moduleExits = [
  { title: '统计与分析', detail: '回归分析、时间序列、多元统计、随机过程、数据同化' },
  { title: '系统与数据挖掘', detail: '分布式系统、自然语言处理、图数据挖掘、算法设计、计算机视觉' },
  { title: '理医工大数据', detail: '卫生统计、医疗大数据、医学图像、生物统计、组学数据分析' },
  { title: '社会科学大数据', detail: '社交网络、金融计量、商务分析、社会数据挖掘、新媒体分析' },
  { title: '类脑计算', detail: '非线性系统、复杂系统、多模态同化、认知智能、神经网络' }
]

const activeTrack = ref<'all' | Track>('all')
const canvas = ref<HTMLElement | null>(null)
const nodeElements = new Map<string, HTMLElement>()
const edgePaths = ref<EdgePath[]>([])
let resizeObserver: ResizeObserver | undefined

const courseById = new Map(courses.map((course) => [course.id, course]))

const courseIsActive = (course: CourseNode) =>
  activeTrack.value === 'all' || course.tracks.includes(activeTrack.value)

const hrefFor = (course: CourseNode) => {
  if (!course.href) return undefined
  return course.external ? course.href : withBase(course.href)
}

const setNodeRef = (id: string, element: unknown) => {
  if (element instanceof HTMLElement) nodeElements.set(id, element)
  else nodeElements.delete(id)
}

const updateEdges = () => {
  if (!canvas.value) return
  const canvasRect = canvas.value.getBoundingClientRect()
  edgePaths.value = edges.flatMap((edge) => {
    const source = nodeElements.get(edge.from)
    const target = nodeElements.get(edge.to)
    const sourceCourse = courseById.get(edge.from)
    const targetCourse = courseById.get(edge.to)
    if (!source || !target || !sourceCourse || !targetCourse) return []

    const sourceRect = source.getBoundingClientRect()
    const targetRect = target.getBoundingClientRect()
    const startX = sourceRect.right - canvasRect.left
    const startY = sourceRect.top + sourceRect.height / 2 - canvasRect.top
    const endX = targetRect.left - canvasRect.left
    const endY = targetRect.top + targetRect.height / 2 - canvasRect.top
    const bend = Math.max(34, Math.abs(endX - startX) * 0.48)
    const d = `M ${startX} ${startY} C ${startX + bend} ${startY}, ${endX - bend} ${endY}, ${endX} ${endY}`
    return [{
      ...edge,
      d,
      active: courseIsActive(sourceCourse) && courseIsActive(targetCourse)
    }]
  })
}

const activeCourseCount = computed(() =>
  courses.filter((course) => courseIsActive(course)).length
)

onMounted(async () => {
  await nextTick()
  updateEdges()
  resizeObserver = new ResizeObserver(updateEdges)
  if (canvas.value) resizeObserver.observe(canvas.value)
  nodeElements.forEach((element) => resizeObserver?.observe(element))
  document.fonts?.ready.then(updateEdges)
  window.addEventListener('resize', updateEdges)
})

watch(activeTrack, () => nextTick(updateEdges))

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  window.removeEventListener('resize', updateEdges)
})
</script>

<template>
  <main class="course-atlas">
    <header class="course-atlas__hero">
      <p class="page-eyebrow">Learning network · 2024 培养方案</p>
      <div>
        <h1>课程地图</h1>
        <p>
          从数理与编程基础出发，经过统计、计算机与优化核心，分流到智能系统和应用领域，
          最终汇入实习与毕业研究。连线表示建议的知识承接关系，不等同于学校正式先修规定。
        </p>
      </div>
    </header>

    <section class="course-map" aria-labelledby="course-map-title">
      <div class="course-map__toolbar">
        <div>
          <span class="course-map__toolbar-label" id="course-map-title">聚焦一条路径</span>
          <span class="course-map__count">当前显示 {{ activeCourseCount }} 个节点</span>
        </div>
        <div class="course-map__filters" role="group" aria-label="筛选专业方向">
          <button
            v-for="option in trackOptions"
            :key="option.value"
            type="button"
            :class="{ 'is-active': activeTrack === option.value }"
            :aria-pressed="activeTrack === option.value"
            @click="activeTrack = option.value"
          >
            {{ option.label }}
          </button>
        </div>
      </div>

      <div class="course-map__scroll" tabindex="0" aria-label="可横向滚动的课程学习路径">
        <div ref="canvas" class="course-map__canvas">
          <div class="course-map__stages" aria-hidden="true">
            <div v-for="stage in stages" :key="stage.number" class="course-map__stage">
              <span>{{ stage.number }}</span>
              <strong>{{ stage.title }}</strong>
              <small>{{ stage.subtitle }}</small>
            </div>
          </div>

          <svg class="course-map__edges" aria-hidden="true">
            <path
              v-for="edge in edgePaths"
              :key="`${edge.from}-${edge.to}`"
              :d="edge.d"
              :class="{ 'is-muted': activeTrack !== 'all' && !edge.active }"
            />
          </svg>

          <div class="course-map__grid">
            <component
              :is="course.href ? 'a' : 'article'"
              v-for="course in courses"
              :key="course.id"
              :ref="(element: unknown) => setNodeRef(course.id, element)"
              class="course-node"
              :class="[
                `course-node--${course.tracks[0]}`,
                { 'is-muted': activeTrack !== 'all' && !courseIsActive(course) }
              ]"
              :style="{ gridColumn: course.column, gridRow: course.row }"
              :href="hrefFor(course)"
              :target="course.external ? '_blank' : undefined"
              :rel="course.external ? 'noreferrer' : undefined"
            >
              <div class="course-node__meta">
                <span>{{ course.term }}</span>
                <span class="course-node__state" :data-state="course.state">{{ course.state }}</span>
              </div>
              <h2>{{ course.title }}</h2>
              <p>{{ course.code }}</p>
              <span v-if="course.href" class="course-node__arrow" aria-hidden="true">
                {{ course.external ? '↗' : '→' }}
              </span>
            </component>
          </div>
        </div>
      </div>

      <div class="course-map__legend" aria-label="课程节点状态说明">
        <span><i data-state="站内可读" />站内可读</span>
        <span><i data-state="仓库资料" />仓库或外部资料</span>
        <span><i data-state="培养方案" />培养方案中的前置或计划课程</span>
      </div>
    </section>

    <section class="module-network" aria-labelledby="module-network-title">
      <div class="module-network__head">
        <p class="page-eyebrow">Professional pathways</p>
        <h2 id="module-network-title">核心课程之后，网络向五个模块展开</h2>
        <p>培养方案允许在专业导师指导下选择发展路径；大数据技术与应用方向要求每个模块至少选一门，类脑计算则形成另一条完整进阶路线。</p>
      </div>
      <div class="module-network__hub" aria-hidden="true">专业核心</div>
      <div class="module-network__branches">
        <article v-for="(module, index) in moduleExits" :key="module.title">
          <span>0{{ index + 1 }}</span>
          <h3>{{ module.title }}</h3>
          <p>{{ module.detail }}</p>
        </article>
      </div>
    </section>
  </main>
</template>

<style scoped>
.course-atlas {
  padding: clamp(58px, 8vw, 112px) 0 120px;
  overflow: hidden;
}

.course-atlas__hero,
.course-map,
.module-network {
  width: min(100% - 40px, 1560px);
  margin-inline: auto;
}

.course-atlas__hero {
  display: grid;
  grid-template-columns: minmax(180px, 0.55fr) minmax(0, 1.45fr);
  gap: 48px;
  align-items: end;
  margin-bottom: 46px;
}

.course-atlas__hero h1 {
  margin: 0;
  font-family: var(--opends-serif);
  font-size: clamp(3.2rem, 8vw, 7rem);
  letter-spacing: -0.07em;
  line-height: 0.95;
}

.course-atlas__hero p:not(.page-eyebrow) {
  max-width: 780px;
  margin: 24px 0 0;
  color: var(--vp-c-text-2);
  font-size: 1.04rem;
  line-height: 1.85;
}

.course-map {
  border: 1px solid var(--vp-c-divider);
  border-radius: 28px;
  overflow: hidden;
  background: color-mix(in srgb, var(--vp-c-bg) 94%, transparent);
  box-shadow: 0 26px 80px rgba(28, 41, 39, 0.08);
}

.course-map__toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  border-bottom: 1px solid var(--vp-c-divider);
  padding: 18px 22px;
  background: color-mix(in srgb, var(--vp-c-bg-soft) 86%, transparent);
}

.course-map__toolbar-label {
  display: block;
  color: var(--vp-c-text-1);
  font-size: 0.82rem;
  font-weight: 760;
}

.course-map__count {
  display: block;
  margin-top: 3px;
  color: var(--vp-c-text-2);
  font-size: 0.72rem;
}

.course-map__filters {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 7px;
}

.course-map__filters button {
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 7px 11px;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  font: inherit;
  font-size: 0.74rem;
  font-weight: 680;
  cursor: pointer;
}

.course-map__filters button:hover,
.course-map__filters button:focus-visible,
.course-map__filters button.is-active {
  border-color: var(--vp-c-brand-1);
  color: white;
  background: var(--vp-c-brand-1);
  outline: none;
}

.course-map__scroll {
  overflow-x: auto;
  overscroll-behavior-inline: contain;
  scrollbar-color: var(--vp-c-divider) transparent;
}

.course-map__scroll:focus-visible {
  outline: 2px solid var(--vp-c-brand-2);
  outline-offset: -2px;
}

.course-map__canvas {
  position: relative;
  min-width: 1500px;
  padding: 34px 44px 52px;
  background-image:
    radial-gradient(circle at 18% 18%, rgba(23, 95, 90, 0.06), transparent 20rem),
    linear-gradient(rgba(23, 95, 90, 0.035) 1px, transparent 1px);
  background-size: auto, 100% 34px;
}

.course-map__stages,
.course-map__grid {
  display: grid;
  grid-template-columns: repeat(5, 220px);
  column-gap: 76px;
}

.course-map__stages {
  margin-bottom: 26px;
}

.course-map__stage {
  display: flex;
  flex-direction: column;
  border-top: 2px solid var(--vp-c-brand-2);
  padding-top: 10px;
}

.course-map__stage span {
  color: var(--opends-gold);
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

.course-map__stage strong {
  margin-top: 3px;
  font-family: var(--opends-serif);
  font-size: 1rem;
}

.course-map__stage small {
  margin-top: 2px;
  color: var(--vp-c-text-2);
  font-size: 0.68rem;
}

.course-map__grid {
  position: relative;
  z-index: 2;
  grid-template-rows: repeat(8, minmax(84px, auto));
  row-gap: 20px;
}

.course-map__edges {
  position: absolute;
  inset: 0;
  z-index: 1;
  width: 100%;
  height: 100%;
  overflow: visible;
  pointer-events: none;
}

.course-map__edges path {
  fill: none;
  stroke: color-mix(in srgb, var(--vp-c-brand-2) 52%, var(--vp-c-divider));
  stroke-width: 1.5;
  transition: opacity 220ms ease, stroke-width 220ms ease;
}

.course-map__edges path:not(.is-muted) {
  stroke-width: 2;
}

.course-map__edges path.is-muted {
  opacity: 0.08;
}

.course-node {
  position: relative;
  align-self: center;
  display: block;
  border: 1px solid var(--vp-c-divider);
  border-left: 4px solid var(--node-accent, var(--vp-c-brand-2));
  border-radius: 14px;
  padding: 14px 15px 13px;
  min-height: 82px;
  color: var(--vp-c-text-1) !important;
  background: color-mix(in srgb, var(--vp-c-bg) 94%, transparent);
  box-shadow: 0 8px 22px rgba(28, 41, 39, 0.07);
  text-decoration: none !important;
  transition: opacity 220ms ease, transform 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

a.course-node:hover,
a.course-node:focus-visible {
  border-color: var(--node-accent, var(--vp-c-brand-2));
  box-shadow: 0 14px 34px rgba(23, 95, 90, 0.14);
  outline: none;
  transform: translateY(-3px);
}

.course-node.is-muted {
  opacity: 0.18;
}

.course-node--math { --node-accent: #b27432; }
.course-node--statistics { --node-accent: #24756f; }
.course-node--systems { --node-accent: #496f9d; }
.course-node--intelligence { --node-accent: #7b5ca8; }
.course-node--application { --node-accent: #9b5f64; }

.course-node__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  color: var(--vp-c-text-2);
  font-size: 0.62rem;
}

.course-node__state {
  color: var(--vp-c-brand-1);
  font-weight: 760;
}

.course-node__state[data-state='仓库资料'] { color: var(--opends-gold); }
.course-node__state[data-state='培养方案'] { color: var(--vp-c-text-2); }

.course-node h2 {
  margin: 8px 20px 2px 0;
  border: 0;
  padding: 0;
  font-family: var(--opends-serif);
  font-size: 0.88rem;
  line-height: 1.35;
}

.course-node p {
  margin: 0;
  color: var(--vp-c-text-2);
  font-size: 0.65rem;
}

.course-node__arrow {
  position: absolute;
  right: 12px;
  bottom: 11px;
  color: var(--node-accent, var(--vp-c-brand-2));
  font-weight: 800;
}

.course-map__legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 22px;
  border-top: 1px solid var(--vp-c-divider);
  padding: 14px 22px;
  color: var(--vp-c-text-2);
  font-size: 0.72rem;
}

.course-map__legend span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}

.course-map__legend i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--vp-c-brand-2);
}

.course-map__legend i[data-state='仓库资料'] { background: var(--opends-gold); }
.course-map__legend i[data-state='培养方案'] { background: var(--vp-c-text-2); }

.module-network {
  position: relative;
  margin-top: 100px;
  padding: 54px 0 0;
}

.module-network__head {
  max-width: 790px;
}

.module-network__head h2 {
  margin: 8px 0 14px;
  font-family: var(--opends-serif);
  font-size: clamp(2rem, 4vw, 3.2rem);
  letter-spacing: -0.045em;
  line-height: 1.15;
}

.module-network__head > p:last-child {
  color: var(--vp-c-text-2);
  line-height: 1.75;
}

.module-network__hub {
  width: max-content;
  margin: 46px auto 32px;
  border: 1px solid var(--vp-c-brand-2);
  border-radius: 999px;
  padding: 10px 18px;
  color: white;
  background: var(--vp-c-brand-1);
  font-size: 0.78rem;
  font-weight: 760;
  box-shadow: 0 10px 28px rgba(23, 95, 90, 0.18);
}

.module-network__branches {
  position: relative;
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
}

.module-network__branches::before {
  position: absolute;
  top: -33px;
  right: 10%;
  left: 10%;
  height: 33px;
  border-top: 1px solid var(--vp-c-divider);
  border-right: 1px solid var(--vp-c-divider);
  border-left: 1px solid var(--vp-c-divider);
  content: '';
}

.module-network__branches article {
  position: relative;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  padding: 20px;
  background: color-mix(in srgb, var(--vp-c-bg) 94%, transparent);
}

.module-network__branches article::before {
  position: absolute;
  top: -34px;
  left: 50%;
  width: 1px;
  height: 34px;
  background: var(--vp-c-divider);
  content: '';
}

.module-network__branches span {
  color: var(--opends-gold);
  font-family: var(--opends-serif);
  font-size: 1.25rem;
}

.module-network__branches h3 {
  margin: 14px 0 8px;
  font-size: 0.98rem;
}

.module-network__branches p {
  margin: 0;
  color: var(--vp-c-text-2);
  font-size: 0.8rem;
  line-height: 1.7;
}

@media (max-width: 900px) {
  .course-atlas__hero {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .course-map__toolbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .course-map__filters {
    justify-content: flex-start;
  }

  .module-network__branches {
    grid-template-columns: 1fr;
  }

  .module-network__branches::before,
  .module-network__branches article::before,
  .module-network__hub {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .course-node,
  .course-map__edges path {
    transition: none;
  }
}
</style>
