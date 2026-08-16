<script setup lang="ts">
import { computed } from 'vue'
import { withBase } from 'vitepress'
import { courses, directionOrder, termOrder, type Course } from '../course-data'

const props = defineProps<{ mode: 'term' | 'direction' }>()

const heading = computed(() => props.mode === 'term' ? '按学期' : '按方向模块')
const order = computed(() => props.mode === 'term' ? termOrder : directionOrder)
const keyOf = (course: Course) => props.mode === 'term' ? course.term : course.direction
const groups = computed(() => order.value.map((label) => ({
  label,
  courses: courses.filter((course) => keyOf(course) === label)
})))
</script>

<template>
  <main class="course-archive">
    <header>
      <h1>{{ heading }}</h1>
      <a :href="withBase('/')">返回</a>
    </header>

    <section v-for="group in groups" :key="group.label" class="course-group">
      <h2>{{ group.label }}</h2>
      <div class="course-list">
        <component
          :is="course.slug ? 'a' : 'div'"
          v-for="course in group.courses"
          :key="course.code"
          class="course-row"
          :class="{ 'has-notes': course.slug }"
          :href="course.slug ? withBase(`/notes/${course.slug}/`) : undefined"
        >
          <code>{{ course.code }}</code>
          <strong>{{ course.title }}</strong>
          <span aria-hidden="true">{{ course.slug ? '→' : '—' }}</span>
        </component>
      </div>
    </section>
  </main>
</template>

<style scoped>
.course-archive {
  width: min(calc(100% - 48px), 960px);
  margin: 0 auto;
  padding: 72px 0 112px;
}

.course-archive > header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 72px;
}

.course-archive h1 {
  margin: 0;
  border: 0;
  font-size: clamp(36px, 6vw, 64px);
  font-weight: 500;
  letter-spacing: -0.055em;
}

.course-archive > header a {
  color: var(--vp-c-text-2);
  font-size: 14px;
  text-decoration: none;
}

.course-archive > header a:hover,
.course-archive > header a:focus-visible {
  color: var(--vp-c-text-1);
}

.course-group + .course-group {
  margin-top: 68px;
}

.course-group h2 {
  margin: 0 0 16px;
  border: 0;
  padding: 0;
  color: var(--vp-c-text-2);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
}

.course-list {
  border-top: 1px solid var(--vp-c-divider);
}

.course-row {
  display: grid;
  grid-template-columns: 132px minmax(0, 1fr) auto;
  align-items: center;
  gap: 20px;
  min-height: 76px;
  border-bottom: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-1);
  text-decoration: none;
}

a.course-row {
  transition: padding 140ms ease;
}

a.course-row:hover,
a.course-row:focus-visible {
  padding: 0 12px;
  outline: none;
}

.course-row code {
  padding: 0;
  color: var(--vp-c-text-3);
  background: none;
  font-size: 12px;
}

.course-row strong {
  overflow: hidden;
  font-size: 17px;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-row span {
  font-size: 18px;
}

@media (max-width: 560px) {
  .course-archive {
    width: min(calc(100% - 32px), 960px);
    padding-top: 48px;
  }

  .course-archive > header {
    margin-bottom: 52px;
  }

  .course-group + .course-group {
    margin-top: 52px;
  }

  .course-row {
    grid-template-columns: 1fr auto;
    gap: 8px 14px;
    padding: 14px 0;
  }

  a.course-row:hover,
  a.course-row:focus-visible {
    padding: 14px 8px;
  }

  .course-row code { grid-column: 1; grid-row: 1; }
  .course-row strong { grid-column: 1; grid-row: 2; }
  .course-row span { grid-column: 2; grid-row: 1 / 3; }
}

@media (prefers-reduced-motion: reduce) {
  a.course-row { transition: none; }
}
</style>
