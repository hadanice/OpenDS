<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

interface PathCourse {
  title: string
  code: string
  href?: string
}

interface PathStage {
  number: string
  title: string
  caption: string
  courses: PathCourse[]
}

interface ModuleCourse {
  title: string
  code: string
  credits: number
  term: string
  href?: string
  group?: '理医工' | '社会科学'
}

interface ModuleGroup {
  id: string
  number: string
  title: string
  kicker: string
  summary: string
  courses: ModuleCourse[]
}

const pathwayStages: PathStage[] = [
  {
    number: '01',
    title: '数理与编程基础',
    caption: '先建立描述问题、表达算法与理解不确定性的共同语言。',
    courses: [
      { title: '高等数学', code: 'MATH120009' },
      { title: '程序设计', code: 'COMP110042' },
      { title: '线性代数', code: 'MATH120010' },
      { title: '数据科学导论', code: 'DATA130001' }
    ]
  },
  {
    number: '02',
    title: '第 3 学期 · 核心工具',
    caption: '从数学基础进入算法、系统与概率三条互相支撑的主线。',
    courses: [
      { title: '高等线性代数', code: 'MATH10003', href: '/notes/advanced-linear-algebra/' },
      { title: '数值算法 I', code: 'MATH20007', href: '/notes/numerical-algorithms/' },
      { title: '数据结构', code: 'CS20017', href: '/notes/algorithms/' },
      { title: '概率论基础', code: 'STAT20011', href: '/notes/probability/' },
      { title: '计算机原理', code: 'CS20018', href: '/notes/computer-systems/' }
    ]
  },
  {
    number: '03',
    title: '第 4 学期 · 建模与系统',
    caption: '把工具组织成模型、数据系统与可复现的计算过程。',
    courses: [
      { title: '最优化方法', code: 'MATH20008', href: '/notes/optimization/' },
      { title: '数据库及实现', code: 'CS20019', href: '/notes/database/' },
      { title: '统计学基础 I', code: 'STAT20010', href: '/notes/mathematical-statistics/' },
      { title: '生物统计学', code: 'STAT50025', href: '/notes/biostatistics/' }
    ]
  },
  {
    number: '04',
    title: '第 5—6 学期 · 智能进阶',
    caption: '沿统计学习、人工智能与数据挖掘进入专业方向。',
    courses: [
      { title: '统计（机器）学习', code: 'STAT30015' },
      { title: '人工智能', code: 'CS50020' },
      { title: '自然语言处理与大语言模型', code: 'CS40008', href: '/notes/nlp-llms/' },
      { title: '图数据管理与挖掘', code: 'CS50027' },
      { title: '神经网络与深度学习', code: 'CS30064' }
    ]
  },
  {
    number: '05',
    title: '实践与研究',
    caption: '用真实问题把知识连接起来，最终形成自己的研究路径。',
    courses: [
      { title: '课程项目', code: 'PROJECTS' },
      { title: '生产实习', code: 'STAT40004' },
      { title: '毕业论文', code: 'STAT40005' }
    ]
  }
]

const modules: ModuleGroup[] = [
  {
    id: 'core',
    number: '01',
    title: '专业核心',
    kicker: 'Common foundation',
    summary: '共同底座覆盖数值计算、统计建模、算法、系统与智能方法。',
    courses: [
      { title: '统计计算', code: 'STAT30016', credits: 3, term: '第 1 学期' },
      { title: '数值算法与案例分析 I', code: 'MATH20007', credits: 3, term: '第 3 学期', href: '/notes/numerical-algorithms/' },
      { title: '统计（机器）学习概论', code: 'STAT30015', credits: 3, term: '第 5 学期' },
      { title: '人工智能', code: 'CS50020', credits: 3, term: '第 5 学期' },
      { title: '神经网络与深度学习', code: 'CS30064', credits: 3, term: '第 6 学期' },
      { title: '生产实习', code: 'STAT40004', credits: 1, term: '第 7 学期' },
      { title: '毕业论文', code: 'STAT40005', credits: 6, term: '第 8 学期' },
      { title: '数据结构', code: 'CS20017', credits: 4, term: '第 3 学期', href: '/notes/algorithms/' },
      { title: '概率论基础', code: 'STAT20011', credits: 3, term: '第 3 学期', href: '/notes/probability/' },
      { title: '计算机原理', code: 'CS20018', credits: 3, term: '第 3 学期', href: '/notes/computer-systems/' },
      { title: '最优化方法', code: 'MATH20008', credits: 3, term: '第 4 学期', href: '/notes/optimization/' },
      { title: '数据库及实现', code: 'CS20019', credits: 3, term: '第 4 学期', href: '/notes/database/' },
      { title: '高等线性代数', code: 'MATH10003', credits: 3, term: '第 3 学期', href: '/notes/advanced-linear-algebra/' },
      { title: '图像处理与可视化', code: 'CS30065', credits: 3, term: '第 5 学期' },
      { title: '统计学基础：原理、方法及 R 应用 (I)', code: 'STAT20010', credits: 3, term: '第 4 学期', href: '/notes/mathematical-statistics/' }
    ]
  },
  {
    id: 'statistics',
    number: '02',
    title: '统计与分析',
    kicker: 'Statistics & analysis',
    summary: '从随机性、回归与时间序列，延伸到数据同化和稀疏方法。',
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
    summary: '把算法放进大规模系统，处理文本、图、图像与复杂决策。',
    courses: [
      { title: '大规模分布式系统', code: 'CS50022', credits: 3, term: '第 4 / 6 学期' },
      { title: '高级大数据解析', code: 'CS50021', credits: 3, term: '第 3 / 5 学期' },
      { title: '自然语言处理 / 大语言模型', code: 'CS50023 · 已修读 CS40008', credits: 3, term: '第 4 / 6 学期', href: '/notes/nlp-llms/' },
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
    summary: '两类应用方向合并成一个探索区，各选一门，把方法带进真实领域。',
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
const activeModuleId = ref('core')
const story = ref<HTMLElement | null>(null)
const activeModule = computed(() => modules.find((item) => item.id === activeModuleId.value) ?? modules[0])

const courseHref = (href?: string) => href ? withBase(href) : undefined

const goToScene = (index: number) => {
  const target = story.value
  if (!target) return
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  target.scrollTo({ top: index * target.clientHeight, behavior: reduced ? 'auto' : 'smooth' })
  activeScene.value = index
}

const syncScene = (event: Event) => {
  const target = event.currentTarget as HTMLElement
  const nextScene = Math.min(1, Math.max(0, Math.round(target.scrollTop / target.clientHeight)))
  if (nextScene !== activeScene.value) activeScene.value = nextScene
}
</script>

<template>
  <main class="course-map-deck">
    <nav class="map-progress" aria-label="课程地图页面">
      <button
        v-for="(_, index) in 2"
        :key="index"
        type="button"
        :class="{ 'is-active': activeScene === index }"
        :aria-label="`前往第 ${index + 1} 幕`"
        :aria-current="activeScene === index ? 'step' : undefined"
        @click="goToScene(index)"
      >
        <span>0{{ index + 1 }}</span>
        <i />
      </button>
    </nav>

    <div ref="story" class="map-story" @scroll.passive="syncScene">
      <section id="map-pathway" class="map-scene map-scene--pathway" :class="{ 'is-active': activeScene === 0 }">
        <div class="map-scene__content">
          <a class="map-back" :href="withBase('/courses/')">← 返回课程入口</a>
          <header class="map-heading">
            <p>Knowledge pathway · 01</p>
            <div>
              <h1>从基础，到专业核心</h1>
              <span>课程不是一张清单。它们沿着数学、统计、算法与系统四条主线彼此承接，最终汇入真实问题。</span>
            </div>
          </header>

          <div class="pathway-shell" aria-label="按学习阶段组织的课程路径">
            <div class="pathway-flow" aria-hidden="true"><i /></div>
            <div class="pathway-grid">
              <article
                v-for="(stage, index) in pathwayStages"
                :key="stage.number"
                class="path-stage"
                :style="{ '--delay': `${index * 70}ms` }"
              >
                <div class="path-stage__node"><span>{{ stage.number }}</span></div>
                <p>{{ stage.title }}</p>
                <h2>{{ stage.caption }}</h2>
                <div class="path-stage__courses">
                  <component
                    :is="course.href ? 'a' : 'span'"
                    v-for="course in stage.courses"
                    :key="course.code"
                    :href="courseHref(course.href)"
                    :class="{ 'has-notes': course.href }"
                  >
                    <b>{{ course.title }}</b>
                    <small>{{ course.code }}</small>
                  </component>
                </div>
              </article>
            </div>
          </div>

          <button class="scene-cue" type="button" @click="goToScene(1)">
            <span>继续看方向模块</span>
            <i>↓</i>
          </button>
        </div>
      </section>

      <section id="map-modules" class="map-scene map-scene--modules" :class="{ 'is-active': activeScene === 1 }">
        <div class="map-scene__content">
          <header class="map-heading map-heading--modules">
            <p>Professional pathways · 02</p>
            <div>
              <h2>核心课程之后，网络向四组方向展开</h2>
              <span>专业核心是共同底座。统计、系统与应用方向不是彼此割裂的终点，而是可以交叉选择的观察角度。</span>
            </div>
          </header>

          <div class="module-workspace">
            <div class="module-selector" role="tablist" aria-label="选择课程模块">
              <button
                v-for="module in modules"
                :key="module.id"
                type="button"
                role="tab"
                :aria-selected="activeModuleId === module.id"
                :aria-controls="`module-${module.id}`"
                :class="{ 'is-active': activeModuleId === module.id }"
                @click="activeModuleId = module.id"
              >
                <span>{{ module.number }}</span>
                <div>
                  <b>{{ module.title }}</b>
                  <small>{{ module.summary }}</small>
                </div>
                <i>{{ module.courses.length }}</i>
              </button>
            </div>

            <section class="module-detail" aria-live="polite">
              <Transition name="module-swap" mode="out-in">
                <div :id="`module-${activeModule.id}`" :key="activeModule.id" role="tabpanel">
                  <header>
                    <div>
                      <p>{{ activeModule.kicker }}</p>
                      <h3>{{ activeModule.title }}</h3>
                    </div>
                    <span>{{ activeModule.courses.length }} 门课程</span>
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
                        <small>{{ course.code }}</small>
                        <i v-if="course.href">↗</i>
                      </div>
                      <h4>{{ course.title }}</h4>
                      <p>{{ course.credits }} 学分 · {{ course.term }}</p>
                    </component>
                  </div>
                </div>
              </Transition>
            </section>
          </div>

          <button class="scene-cue scene-cue--up" type="button" @click="goToScene(0)">
            <i>↑</i>
            <span>回到学习主线</span>
          </button>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.course-map-deck {
  position: relative;
  height: calc(100svh - var(--vp-nav-height));
  min-height: 620px;
  overflow: hidden;
  color: var(--vp-c-text-1);
  background: var(--vp-c-bg);
}

.map-story {
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  scroll-behavior: smooth;
  scroll-snap-type: y mandatory;
  scrollbar-color: color-mix(in srgb, var(--vp-c-brand-1) 38%, transparent) transparent;
  scrollbar-width: thin;
}

.map-scene {
  position: relative;
  height: 100%;
  min-height: 620px;
  overflow-y: auto;
  scroll-snap-align: start;
  scroll-snap-stop: always;
}

.map-scene::before,
.map-scene::after {
  position: absolute;
  border-radius: 50%;
  content: "";
  pointer-events: none;
}

.map-scene--pathway {
  background:
    linear-gradient(color-mix(in srgb, var(--vp-c-divider) 28%, transparent) 1px, transparent 1px),
    radial-gradient(circle at 10% 18%, color-mix(in srgb, var(--vp-c-brand-1) 13%, transparent), transparent 30%),
    radial-gradient(circle at 88% 70%, rgba(184, 113, 32, .09), transparent 29%),
    var(--vp-c-bg);
  background-size: 100% 45px, auto, auto, auto;
}

.map-scene--pathway::before {
  top: -24vw;
  right: -12vw;
  width: 52vw;
  height: 52vw;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 16%, transparent);
}

.map-scene--pathway::after {
  top: -11vw;
  right: 1vw;
  width: 26vw;
  height: 26vw;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent);
}

.map-scene--modules {
  background:
    radial-gradient(circle at 88% 14%, color-mix(in srgb, var(--vp-c-brand-1) 12%, transparent), transparent 25%),
    radial-gradient(circle at 5% 88%, rgba(184, 113, 32, .09), transparent 24%),
    var(--vp-c-bg-alt);
}

.map-scene__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  width: min(calc(100% - 72px), 1500px);
  min-height: 100%;
  margin: 0 auto;
  padding: clamp(28px, 4vh, 52px) 0 24px;
}

.map-back {
  align-self: flex-start;
  margin-bottom: clamp(24px, 4vh, 46px);
  color: var(--vp-c-text-2);
  font-size: 13px;
  letter-spacing: .05em;
  text-decoration: none;
  transition: color .2s ease, transform .2s ease;
}

.map-back:hover {
  color: var(--vp-c-brand-1);
  transform: translateX(-3px);
}

.map-heading {
  display: grid;
  grid-template-columns: minmax(180px, .35fr) minmax(0, 1.65fr);
  gap: clamp(28px, 5vw, 80px);
  align-items: start;
  margin-bottom: clamp(24px, 4vh, 44px);
}

.map-heading > p {
  margin: 9px 0 0;
  color: #b66f20;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
}

.map-heading h1,
.map-heading h2 {
  margin: 0;
  border: 0;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, "Noto Serif SC", serif);
  font-size: clamp(42px, 5vw, 74px);
  font-weight: 500;
  letter-spacing: -.055em;
  line-height: 1.05;
}

.map-heading span {
  display: block;
  max-width: 860px;
  margin-top: 18px;
  color: var(--vp-c-text-2);
  font-size: clamp(15px, 1.35vw, 19px);
  line-height: 1.75;
}

.pathway-shell {
  position: relative;
  flex: 1;
  min-height: 360px;
  overflow-x: auto;
  overflow-y: hidden;
  border: 1px solid var(--vp-c-divider);
  border-radius: 28px;
  background: color-mix(in srgb, var(--vp-c-bg) 88%, transparent);
  box-shadow: 0 22px 70px rgba(16, 54, 49, .07);
  scrollbar-color: color-mix(in srgb, var(--vp-c-brand-1) 30%, transparent) transparent;
  scrollbar-width: thin;
}

.pathway-flow {
  position: absolute;
  top: 50px;
  left: 9.5%;
  width: 81%;
  height: 2px;
  overflow: hidden;
  background: color-mix(in srgb, var(--vp-c-brand-1) 18%, var(--vp-c-divider));
}

.pathway-flow i {
  position: absolute;
  inset: 0 auto 0 -28%;
  width: 28%;
  background: linear-gradient(90deg, transparent, var(--vp-c-brand-1), transparent);
  animation: pathway-pulse 5.8s ease-in-out infinite;
}

.pathway-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(220px, 1fr));
  gap: 0;
  min-width: 1180px;
  height: 100%;
  padding: 30px 22px 22px;
}

.path-stage {
  position: relative;
  padding: 0 16px;
  opacity: 0;
  transform: translateY(18px);
}

.map-scene.is-active .path-stage {
  animation: stage-arrive .65s var(--delay) ease forwards;
}

.path-stage:not(:last-child)::after {
  position: absolute;
  top: 17px;
  right: -5px;
  color: var(--vp-c-brand-1);
  content: "→";
  font-size: 16px;
}

.path-stage__node {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  margin: 0 auto 22px;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 38%, var(--vp-c-divider));
  border-radius: 50%;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
  box-shadow: 0 0 0 9px color-mix(in srgb, var(--vp-c-brand-1) 8%, transparent);
  font-family: var(--opends-serif, serif);
  font-size: 13px;
}

.path-stage > p {
  margin: 0 0 8px;
  color: var(--vp-c-text-1);
  font-size: 15px;
  font-weight: 700;
  text-align: center;
}

.path-stage > h2 {
  min-height: 55px;
  margin: 0 0 18px;
  border: 0;
  color: var(--vp-c-text-3);
  font-size: 12px;
  font-weight: 400;
  line-height: 1.55;
  text-align: center;
}

.path-stage__courses {
  display: grid;
  gap: 8px;
}

.path-stage__courses > * {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  min-height: 42px;
  padding: 9px 11px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 11px;
  color: var(--vp-c-text-2);
  background: color-mix(in srgb, var(--vp-c-bg-soft) 70%, transparent);
  text-decoration: none;
  transition: border-color .2s ease, color .2s ease, transform .2s ease, background .2s ease;
}

.path-stage__courses > *.has-notes {
  border-color: color-mix(in srgb, var(--vp-c-brand-1) 28%, var(--vp-c-divider));
  color: var(--vp-c-text-1);
}

.path-stage__courses > a:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 8%, var(--vp-c-bg));
  transform: translateY(-2px);
}

.path-stage__courses b {
  font-size: 12px;
  font-weight: 600;
  line-height: 1.35;
}

.path-stage__courses small {
  flex: none;
  color: var(--vp-c-text-3);
  font-family: ui-monospace, monospace;
  font-size: 9px;
}

.scene-cue {
  display: inline-flex;
  align-items: center;
  align-self: center;
  gap: 12px;
  margin-top: 18px;
  border: 0;
  color: var(--vp-c-text-2);
  background: transparent;
  cursor: pointer;
  font-size: 12px;
  letter-spacing: .08em;
}

.scene-cue i {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  color: var(--vp-c-brand-1);
  font-style: normal;
  animation: cue-drift 2s ease-in-out infinite;
}

.map-heading--modules {
  margin-top: clamp(5px, 2vh, 20px);
}

.map-heading--modules h2 {
  font-size: clamp(38px, 4.4vw, 66px);
}

.module-workspace {
  display: grid;
  grid-template-columns: minmax(280px, .72fr) minmax(0, 1.58fr);
  gap: clamp(22px, 3vw, 48px);
  flex: 1;
  min-height: 0;
}

.module-selector {
  position: relative;
  display: grid;
  align-content: center;
  gap: 8px;
}

.module-selector::before {
  position: absolute;
  top: 12%;
  bottom: 12%;
  left: 20px;
  width: 1px;
  background: linear-gradient(transparent, var(--vp-c-divider) 15%, var(--vp-c-divider) 85%, transparent);
  content: "";
}

.module-selector button {
  position: relative;
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  gap: 14px;
  align-items: center;
  width: 100%;
  padding: 16px 15px 16px 0;
  border: 1px solid transparent;
  border-radius: 16px;
  color: var(--vp-c-text-2);
  background: transparent;
  cursor: pointer;
  text-align: left;
  transition: color .25s ease, background .25s ease, border-color .25s ease, transform .25s ease;
}

.module-selector button > span {
  position: relative;
  z-index: 1;
  display: grid;
  place-items: center;
  width: 41px;
  height: 41px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  color: var(--vp-c-text-3);
  background: var(--vp-c-bg-alt);
  font-family: var(--opends-serif, serif);
  font-size: 12px;
  transition: inherit;
}

.module-selector button b,
.module-selector button small {
  display: block;
}

.module-selector button b {
  margin-bottom: 5px;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, serif);
  font-size: 18px;
  font-weight: 600;
}

.module-selector button small {
  overflow: hidden;
  font-size: 11px;
  line-height: 1.45;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.module-selector button > i {
  color: var(--vp-c-text-3);
  font-size: 11px;
  font-style: normal;
}

.module-selector button:hover {
  color: var(--vp-c-text-1);
  transform: translateX(4px);
}

.module-selector button.is-active {
  border-color: color-mix(in srgb, var(--vp-c-brand-1) 20%, var(--vp-c-divider));
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--vp-c-bg) 78%, transparent);
  box-shadow: 0 12px 36px rgba(18, 61, 56, .06);
}

.module-selector button.is-active > span {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-bg);
  background: var(--vp-c-brand-1);
  box-shadow: 0 0 0 7px color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent);
}

.module-detail {
  min-height: 0;
  padding: clamp(20px, 2.4vw, 34px);
  overflow-y: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 26px;
  background: color-mix(in srgb, var(--vp-c-bg) 91%, transparent);
  box-shadow: 0 22px 70px rgba(16, 54, 49, .08);
  scrollbar-color: color-mix(in srgb, var(--vp-c-brand-1) 32%, transparent) transparent;
  scrollbar-width: thin;
}

.module-detail header {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.module-detail header p {
  margin: 0 0 5px;
  color: #b66f20;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: .15em;
  text-transform: uppercase;
}

.module-detail header h3 {
  margin: 0;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, serif);
  font-size: clamp(27px, 2.6vw, 39px);
  font-weight: 500;
  letter-spacing: -.035em;
}

.module-detail header > span {
  flex: none;
  color: var(--vp-c-text-3);
  font-size: 12px;
}

.module-course-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}

.module-course {
  display: block;
  min-height: 105px;
  padding: 13px 15px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 13px;
  color: var(--vp-c-text-1);
  background: color-mix(in srgb, var(--vp-c-bg-soft) 68%, transparent);
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
  gap: 7px;
}

.module-course small {
  overflow: hidden;
  color: var(--vp-c-text-3);
  font-family: ui-monospace, monospace;
  font-size: 9px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.module-course em {
  flex: none;
  padding: 2px 6px;
  border-radius: 999px;
  color: var(--vp-c-brand-1);
  background: color-mix(in srgb, var(--vp-c-brand-1) 10%, transparent);
  font-size: 9px;
  font-style: normal;
}

.module-course i {
  margin-left: auto;
  color: var(--vp-c-brand-1);
  font-size: 11px;
  font-style: normal;
}

.module-course h4 {
  margin: 11px 0 8px;
  color: var(--vp-c-text-1);
  font-size: 14px;
  font-weight: 650;
  line-height: 1.35;
}

.module-course p {
  margin: 0;
  color: var(--vp-c-text-3);
  font-size: 10px;
}

.scene-cue--up {
  flex-direction: row;
  margin-top: 14px;
}

.module-swap-enter-active,
.module-swap-leave-active {
  transition: opacity .22s ease, transform .22s ease;
}

.module-swap-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.module-swap-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.map-progress {
  position: absolute;
  z-index: 5;
  top: 50%;
  right: clamp(12px, 2vw, 34px);
  display: grid;
  gap: 18px;
  transform: translateY(-50%);
}

.map-progress button {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 9px;
  padding: 0;
  border: 0;
  color: var(--vp-c-text-3);
  background: transparent;
  cursor: pointer;
  font-size: 10px;
}

.map-progress i {
  display: block;
  width: 17px;
  height: 2px;
  background: var(--vp-c-divider);
  transition: width .25s ease, background .25s ease;
}

.map-progress button.is-active {
  color: var(--vp-c-text-1);
}

.map-progress button.is-active i {
  width: 32px;
  background: var(--vp-c-brand-1);
}

@keyframes pathway-pulse {
  0% { transform: translateX(0); }
  55%, 100% { transform: translateX(460%); }
}

@keyframes stage-arrive {
  to { opacity: 1; transform: translateY(0); }
}

@keyframes cue-drift {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(3px); }
}

@media (max-width: 960px) {
  .map-heading {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .map-heading > p {
    margin: 0;
  }

  .map-heading span {
    margin-top: 12px;
  }

  .module-workspace {
    grid-template-columns: 1fr;
    grid-template-rows: auto minmax(0, 1fr);
    gap: 14px;
  }

  .module-selector {
    grid-auto-flow: column;
    grid-auto-columns: minmax(220px, 1fr);
    grid-template-columns: none;
    align-content: normal;
    gap: 9px;
    overflow-x: auto;
    padding-bottom: 5px;
    scrollbar-width: thin;
  }

  .module-selector::before {
    display: none;
  }

  .module-selector button {
    grid-template-columns: 32px minmax(0, 1fr) auto;
    padding: 10px;
    border-color: var(--vp-c-divider);
    background: color-mix(in srgb, var(--vp-c-bg) 66%, transparent);
  }

  .module-selector button > span {
    width: 32px;
    height: 32px;
  }

  .module-selector button small {
    display: none;
  }
}

@media (max-width: 700px) {
  .course-map-deck,
  .map-scene {
    min-height: 570px;
  }

  .map-scene__content {
    width: min(calc(100% - 30px), 1500px);
    padding-top: 24px;
  }

  .map-back {
    margin-bottom: 22px;
  }

  .map-heading {
    margin-bottom: 20px;
  }

  .map-heading h1,
  .map-heading h2 {
    font-size: clamp(34px, 10vw, 47px);
  }

  .map-heading span {
    font-size: 14px;
    line-height: 1.6;
  }

  .pathway-shell {
    min-height: 340px;
    border-radius: 20px;
  }

  .pathway-grid {
    min-width: 1120px;
  }

  .map-progress {
    top: 18px;
    right: 16px;
    grid-auto-flow: column;
    transform: none;
  }

  .map-progress button span {
    display: none;
  }

  .map-progress button.is-active i {
    width: 24px;
  }

  .map-heading--modules {
    margin-top: 22px;
  }

  .module-detail {
    padding: 18px;
    border-radius: 20px;
  }

  .module-detail header {
    margin-bottom: 14px;
    padding-bottom: 13px;
  }

  .module-course-grid {
    grid-template-columns: 1fr;
  }

  .module-course {
    min-height: 98px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .map-story {
    scroll-behavior: auto;
  }

  .pathway-flow i,
  .scene-cue i {
    animation: none;
  }

  .map-scene.is-active .path-stage {
    opacity: 1;
    transform: none;
    animation: none;
  }
}
</style>
