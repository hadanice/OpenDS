<script setup lang="ts">
import { withBase } from 'vitepress'
import CourseGrid from './CourseGrid.vue'
</script>

<template>
  <main class="term-archive">
    <a class="term-archive__back" :href="withBase('/courses/')">← 返回课程入口</a>
    <header class="term-archive__hero">
      <div>
        <p>Chronological archive</p>
        <h1>按学期查看</h1>
      </div>
      <span>按学习时间从早到晚展开。选择学期，查看当期课程、资料状态和阅读入口。</span>
    </header>
    <CourseGrid />
  </main>
</template>

<style scoped>
.term-archive {
  width: min(calc(100% - 40px), 1240px);
  margin: 0 auto;
  padding: clamp(44px, 7vw, 92px) 0 110px;
}

.term-archive__back {
  display: inline-flex;
  align-items: center;
  margin-bottom: clamp(40px, 7vw, 84px);
  color: var(--vp-c-text-2);
  font-size: 14px;
  letter-spacing: .04em;
  text-decoration: none;
  transition: color .2s ease, transform .2s ease;
}

.term-archive__back:hover {
  color: var(--vp-c-brand-1);
  transform: translateX(-3px);
}

.term-archive__hero {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(260px, .8fr);
  align-items: end;
  gap: 48px;
  margin-bottom: clamp(42px, 6vw, 74px);
  padding-bottom: 34px;
  border-bottom: 1px solid var(--vp-c-divider);
}

.term-archive__hero p {
  margin: 0 0 16px;
  color: #b66f20;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
}

.term-archive__hero h1 {
  margin: 0;
  border: 0;
  color: var(--vp-c-text-1);
  font-family: var(--opends-serif, "Noto Serif SC", serif);
  font-size: clamp(48px, 7vw, 88px);
  font-weight: 500;
  letter-spacing: -.055em;
  line-height: .98;
}

.term-archive__hero span {
  color: var(--vp-c-text-2);
  font-size: clamp(16px, 1.6vw, 20px);
  line-height: 1.8;
}

@media (max-width: 700px) {
  .term-archive {
    width: min(calc(100% - 30px), 1240px);
    padding-top: 30px;
  }

  .term-archive__back {
    margin-bottom: 44px;
  }

  .term-archive__hero {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>
