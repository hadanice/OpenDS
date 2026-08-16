<script setup lang="ts">
import { withBase } from 'vitepress'
</script>

<template>
  <main class="course-portal">
    <h1 class="visually-hidden">课程笔记</h1>
    <nav aria-label="课程笔记浏览方式">
      <a :href="withBase('/courses/terms')">
        <span>01</span>
        <strong>按学期</strong>
        <i aria-hidden="true">→</i>
      </a>
      <a :href="withBase('/courses/map')">
        <span>02</span>
        <strong>按方向模块</strong>
        <i aria-hidden="true">→</i>
      </a>
    </nav>
  </main>
</template>

<style scoped>
.course-portal {
  display: grid;
  min-height: calc(100dvh - var(--vp-nav-height));
  place-items: center;
  padding: 48px 24px;
}

.course-portal nav {
  width: min(100%, 860px);
  border-top: 1px solid var(--vp-c-divider);
}

.course-portal a {
  display: grid;
  grid-template-columns: 52px 1fr auto;
  align-items: center;
  gap: 18px;
  min-height: 132px;
  border-bottom: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-1);
  text-decoration: none;
  transition: color 140ms ease, background-color 140ms ease;
}

.course-portal a:hover,
.course-portal a:focus-visible {
  color: var(--vp-c-bg);
  background: var(--vp-c-text-1);
  outline: none;
}

.course-portal span {
  padding-left: 18px;
  color: var(--vp-c-text-3);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.course-portal a:hover span,
.course-portal a:focus-visible span {
  color: currentColor;
}

.course-portal strong {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 500;
  letter-spacing: -0.04em;
}

.course-portal i {
  padding-right: 20px;
  font-size: 22px;
  font-style: normal;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 560px) {
  .course-portal {
    align-items: start;
    padding-top: 18vh;
  }

  .course-portal a {
    grid-template-columns: 36px 1fr auto;
    min-height: 104px;
    gap: 10px;
  }

  .course-portal span { padding-left: 8px; }
  .course-portal i { padding-right: 8px; }
}

@media (prefers-reduced-motion: reduce) {
  .course-portal a { transition: none; }
}
</style>
