<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'

type CourseState = '已整理' | '持续更新' | '计划中'

interface Course {
  term: string
  title: string
  code: string
  teacher: string
  materials: string[]
  state: CourseState
  href?: string
  external?: boolean
}

const props = withDefaults(defineProps<{ featured?: boolean }>(), {
  featured: false
})

const courses: Course[] = [
  {
    term: '25秋',
    title: '高等线性代数',
    code: 'MATH10003',
    teacher: '邵美悦',
    materials: ['笔记', '作业'],
    state: '已整理',
    href: '/notes/advanced-linear-algebra/'
  },
  {
    term: '25秋',
    title: '数值算法与案例分析Ⅰ',
    code: 'MATH20007',
    teacher: '邵美悦',
    materials: ['笔记', '作业', '项目'],
    state: '已整理',
    href: '/notes/numerical-algorithms/'
  },
  {
    term: '25秋',
    title: '算法与数据结构',
    code: 'CS20017h',
    teacher: '黄增峰',
    materials: ['笔记', '课件', '作业'],
    state: '已整理',
    href: '/notes/algorithms/'
  },
  {
    term: '25秋',
    title: '计算机原理',
    code: 'CS20018',
    teacher: '梁家卿',
    materials: ['笔记', '课件', 'Lab'],
    state: '已整理',
    href: '/notes/computer-systems/'
  },
  {
    term: '25秋',
    title: '概率论基础',
    code: 'STAT20011',
    teacher: '吴波',
    materials: ['笔记', '作业'],
    state: '已整理',
    href: '/notes/probability/'
  },
  {
    term: '26春',
    title: '最优化方法',
    code: 'MATH20008',
    teacher: '江如俊',
    materials: ['笔记', '作业'],
    state: '已整理',
    href: '/notes/optimization/'
  },
  {
    term: '26春',
    title: '数据库及实现',
    code: 'CS20019',
    teacher: '郑卫国',
    materials: ['笔记', '项目'],
    state: '已整理',
    href: '/notes/database/'
  },
  {
    term: '26春',
    title: '自然语言处理与大语言模型',
    code: 'CS40008',
    teacher: '周宝健',
    materials: ['笔记', 'Readings', '实验', '项目'],
    state: '已整理',
    href: '/notes/nlp-llms/'
  },
  {
    term: '26春',
    title: '统计学基础Ⅰ：数理统计',
    code: 'STAT20010h',
    teacher: '孙鑫伟',
    materials: ['笔记', '项目', '考试'],
    state: '已整理',
    href: '/notes/mathematical-statistics/'
  },
  {
    term: '26春',
    title: '生物统计学',
    code: 'STAT50025',
    teacher: '张静茹',
    materials: ['笔记', '项目', '展示'],
    state: '已整理',
    href: '/notes/biostatistics/'
  },
  {
    term: '26秋',
    title: '多模态数据同化',
    code: 'AIS410010',
    teacher: '陈钊',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '26秋',
    title: '图像处理与数据可视化',
    code: 'CS30065h',
    teacher: '庄吓海、陈思明',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '26秋',
    title: '人工智能',
    code: 'CS50020',
    teacher: '魏忠钰',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '26秋',
    title: '图数据管理与挖掘',
    code: 'CS50027',
    teacher: '郑卫国',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '26秋',
    title: '统计（机器）学习概论',
    code: 'STAT30015',
    teacher: '王天宇',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '26秋',
    title: '统计计算',
    code: 'STAT30016h',
    teacher: '张楠、周渊',
    materials: ['待整理'],
    state: '计划中'
  },
  {
    term: '27春',
    title: '神经网络与深度学习',
    code: 'CS30064',
    teacher: '付彦伟',
    materials: ['待整理'],
    state: '计划中'
  }
]

const terms = ['全部', '25秋', '26春', '26秋', '27春']
const activeTerm = ref('全部')
const termOrder = new Map([
  ['25秋', 1],
  ['26春', 2],
  ['26秋', 3],
  ['27春', 4]
])

const visibleCourses = computed(() => {
  if (props.featured) {
    return courses
      .filter((course) => Boolean(course.href))
      .sort((left, right) => (termOrder.get(right.term) ?? -1) - (termOrder.get(left.term) ?? -1))
  }

  if (activeTerm.value === '全部') {
    return [...courses]
      .sort((left, right) => (termOrder.get(left.term) ?? -1) - (termOrder.get(right.term) ?? -1))
  }
  return courses.filter((course) => course.term === activeTerm.value)
})

const courseHref = (course: Course) => {
  if (!course.href) return undefined
  return course.external ? course.href : withBase(course.href)
}
</script>

<template>
  <div class="course-browser">
    <div v-if="!featured" class="course-filters" aria-label="按学期筛选课程">
      <button
        v-for="term in terms"
        :key="term"
        class="course-filter"
        :class="{ 'is-active': activeTerm === term }"
        :aria-pressed="activeTerm === term"
        type="button"
        @click="activeTerm = term"
      >
        {{ term }}
      </button>
    </div>

    <div class="course-grid">
      <component
        :is="course.href ? 'a' : 'article'"
        v-for="course in visibleCourses"
        :key="`${course.term}-${course.code}`"
        class="course-card"
        :class="{ 'is-planned': !course.href }"
        :href="courseHref(course)"
        :target="course.external ? '_blank' : undefined"
        :rel="course.external ? 'noreferrer' : undefined"
      >
        <div class="course-card__topline">
          <span class="course-term">{{ course.term }}</span>
          <span class="course-state" :data-state="course.state">{{ course.state }}</span>
        </div>
        <h3>{{ course.title }}</h3>
        <div class="course-meta">
          <span>{{ course.code }}</span>
          <span>{{ course.teacher }}</span>
        </div>
        <div class="course-materials">
          <span v-for="material in course.materials" :key="material">{{ material }}</span>
        </div>
        <span v-if="course.href" class="course-card__link">
          {{ course.external ? '查看资料' : '阅读课程' }}
          <span aria-hidden="true">{{ course.external ? '↗' : '→' }}</span>
        </span>
        <span v-else class="course-card__link">等待开课</span>
      </component>
    </div>
  </div>
</template>

<style scoped>
.course-browser {
  margin: 22px 0 0;
}

.course-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  margin: 0 0 24px;
}

.course-filter {
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 8px 15px;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-2);
  cursor: pointer;
  font: inherit;
  font-size: 0.86rem;
  font-weight: 650;
  transition: 150ms ease;
}

.course-filter:hover,
.course-filter:focus-visible {
  border-color: var(--vp-c-brand-2);
  color: var(--vp-c-brand-1);
}

.course-filter.is-active {
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-1);
  color: white;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.course-card {
  position: relative;
  display: flex;
  min-height: 240px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  padding: 22px;
  overflow: hidden;
  background: color-mix(in srgb, var(--vp-c-bg) 93%, transparent);
  box-shadow: 0 12px 34px rgba(28, 41, 39, 0.05);
  color: var(--vp-c-text-1) !important;
  flex-direction: column;
  text-decoration: none !important;
  transition: border-color 160ms ease, box-shadow 160ms ease, transform 160ms ease;
}

.course-card::after {
  position: absolute;
  right: -34px;
  bottom: -44px;
  width: 118px;
  height: 118px;
  border: 1px solid var(--vp-c-brand-soft);
  border-radius: 50%;
  content: "";
}

a.course-card:hover {
  border-color: var(--vp-c-brand-2);
  box-shadow: 0 18px 44px rgba(23, 95, 90, 0.11);
  transform: translateY(-4px);
}

.course-card.is-planned {
  background: color-mix(in srgb, var(--vp-c-bg-soft) 85%, transparent);
}

.course-card__topline,
.course-meta,
.course-materials {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.course-card__topline {
  justify-content: space-between;
  gap: 10px;
}

.course-term {
  color: var(--opends-gold);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}

.course-state {
  border-radius: 999px;
  padding: 4px 9px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 0.7rem;
  font-weight: 700;
}

.course-state[data-state="计划中"] {
  background: color-mix(in srgb, var(--vp-c-text-2) 10%, transparent);
  color: var(--vp-c-text-2);
}

.course-card h3 {
  margin: 23px 0 10px;
  border: 0;
  font-family: var(--opends-serif);
  font-size: 1.15rem;
  letter-spacing: -0.02em;
  line-height: 1.45;
}

.course-meta {
  gap: 7px 13px;
  color: var(--vp-c-text-2);
  font-size: 0.82rem;
}

.course-materials {
  gap: 6px;
  margin-top: 18px;
}

.course-materials span {
  border: 1px solid var(--vp-c-divider);
  border-radius: 6px;
  padding: 3px 7px;
  color: var(--vp-c-text-2);
  font-size: 0.72rem;
}

.course-card__link {
  z-index: 1;
  margin-top: auto;
  padding-top: 24px;
  color: var(--vp-c-brand-1);
  font-size: 0.82rem;
  font-weight: 750;
}

.is-planned .course-card__link {
  color: var(--vp-c-text-2);
}

@media (max-width: 960px) {
  .course-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .course-grid {
    grid-template-columns: 1fr;
  }

  .course-card {
    min-height: 218px;
  }
}
</style>
