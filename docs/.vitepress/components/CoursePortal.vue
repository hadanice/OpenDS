<script setup lang="ts">
import { withBase } from 'vitepress'
</script>

<template>
  <main class="course-portal">
    <div class="course-portal__glow" aria-hidden="true" />
    <header class="course-portal__hero">
      <p class="course-portal__eyebrow">Course archive · two views</p>
      <h1>用两种方式，进入同一张知识网络</h1>
      <p>按时间回看每个学期的学习现场，或沿知识承接关系理解课程为什么彼此相连。</p>
    </header>

    <section class="course-portal__choices" aria-label="选择课程浏览方式">
      <a class="course-choice course-choice--term" :href="withBase('/courses/terms')">
        <div class="course-choice__meta"><span>01</span><small>Chronological</small></div>
        <div class="course-choice__copy">
          <h2>按学期查看</h2>
          <p>从最近学期向前浏览课程，快速进入笔记、作业、项目和相关资源。</p>
        </div>
        <div class="term-preview" aria-hidden="true">
          <span>27 春</span><span>26 秋</span><span>26 春</span><span>25 秋</span>
        </div>
        <strong class="course-choice__action">打开学期档案 <i>→</i></strong>
      </a>

      <a class="course-choice course-choice--map" :href="withBase('/courses/map')">
        <div class="course-choice__meta"><span>02</span><small>Relational</small></div>
        <div class="course-choice__copy">
          <h2>按课程地图查看</h2>
          <p>从基础走向专业核心，再展开统计、系统与跨领域应用的进阶方向。</p>
        </div>
        <div class="network-preview" aria-hidden="true">
          <i class="network-preview__line network-preview__line--one" />
          <i class="network-preview__line network-preview__line--two" />
          <i class="network-preview__line network-preview__line--three" />
          <span class="network-preview__node network-preview__node--one" />
          <span class="network-preview__node network-preview__node--two" />
          <span class="network-preview__node network-preview__node--three" />
          <span class="network-preview__node network-preview__node--four" />
          <span class="network-preview__node network-preview__node--five" />
        </div>
        <strong class="course-choice__action">进入学习路径 <i>↓</i></strong>
      </a>
    </section>
  </main>
</template>

<style scoped>
.course-portal {
  position: relative;
  min-height: calc(100svh - var(--vp-nav-height));
  padding: clamp(62px, 8vw, 112px) max(24px, calc((100vw - 1320px) / 2)) 72px;
  overflow: hidden;
  background:
    linear-gradient(rgba(23, 95, 90, 0.032) 1px, transparent 1px),
    var(--vp-c-bg);
  background-size: 100% 34px;
}

.course-portal__glow {
  position: absolute;
  top: -22%;
  right: -8%;
  width: min(58vw, 820px);
  aspect-ratio: 1;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  box-shadow: 0 0 0 70px rgba(23, 95, 90, 0.025), 0 0 0 140px rgba(178, 116, 50, 0.018);
  pointer-events: none;
}

.course-portal__hero {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
  gap: clamp(36px, 7vw, 110px);
  align-items: end;
  margin-bottom: clamp(46px, 7vh, 76px);
}

.course-portal__eyebrow {
  grid-column: 1 / -1;
  margin: 0 0 -20px;
  color: var(--opends-gold);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.course-portal__hero h1 {
  max-width: 850px;
  margin: 0;
  font-family: var(--opends-serif);
  font-size: clamp(3.3rem, 6.8vw, 6.8rem);
  letter-spacing: -0.065em;
  line-height: 0.98;
}

.course-portal__hero > p:last-child {
  margin: 0 0 8px;
  color: var(--vp-c-text-2);
  font-size: 1rem;
  line-height: 1.85;
}

.course-portal__choices {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.course-choice {
  position: relative;
  display: grid;
  min-height: 370px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 26px;
  padding: clamp(24px, 3vw, 38px);
  overflow: hidden;
  color: var(--vp-c-text-1) !important;
  background: color-mix(in srgb, var(--vp-c-bg) 92%, transparent);
  box-shadow: 0 22px 58px rgba(28, 41, 39, 0.07);
  text-decoration: none !important;
  transition: transform 320ms cubic-bezier(0.22, 1, 0.36, 1), border-color 240ms ease, box-shadow 240ms ease;
}

.course-choice:hover,
.course-choice:focus-visible {
  border-color: var(--vp-c-brand-2);
  box-shadow: 0 30px 72px rgba(23, 95, 90, 0.13);
  outline: none;
  transform: translateY(-7px);
}

.course-choice--map {
  color: #f7f3e9 !important;
  background: #124d49;
}

.course-choice__meta {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
}

.course-choice__meta span {
  color: var(--opends-gold);
  font-family: var(--opends-serif);
  font-size: 2.1rem;
}

.course-choice__meta small {
  color: currentColor;
  font-size: 0.62rem;
  font-weight: 760;
  letter-spacing: 0.16em;
  opacity: 0.58;
  text-transform: uppercase;
}

.course-choice__copy {
  align-self: end;
  max-width: 450px;
}

.course-choice__copy h2 {
  margin: 0 0 10px;
  border: 0;
  padding: 0;
  font-family: var(--opends-serif);
  font-size: clamp(2rem, 3.6vw, 3.4rem);
  letter-spacing: -0.045em;
}

.course-choice__copy p {
  margin: 0;
  color: currentColor;
  font-size: 0.9rem;
  line-height: 1.75;
  opacity: 0.68;
}

.course-choice__action {
  align-self: end;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid color-mix(in srgb, currentColor 18%, transparent);
  padding-top: 18px;
  font-size: 0.8rem;
}

.course-choice__action i { font-size: 1.15rem; font-style: normal; transition: transform 220ms ease; }
.course-choice:hover .course-choice__action i { transform: translateX(5px); }
.course-choice--map:hover .course-choice__action i { transform: translateY(4px); }

.term-preview {
  position: absolute;
  top: 30px;
  right: 30px;
  display: grid;
  width: min(38%, 210px);
  transform: rotate(3deg);
}

.term-preview span {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  padding: 9px 12px;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  font-family: var(--opends-serif);
  font-size: 0.78rem;
  box-shadow: 0 7px 18px rgba(28, 41, 39, 0.05);
}

.term-preview span + span { margin-top: -2px; }

.network-preview {
  position: absolute;
  top: 28px;
  right: 34px;
  width: min(40%, 220px);
  aspect-ratio: 1.35;
  opacity: 0.78;
}

.network-preview__line {
  position: absolute;
  top: 50%;
  left: 12%;
  width: 76%;
  height: 1px;
  background: rgba(247, 243, 233, 0.32);
  transform-origin: center;
}

.network-preview__line--two { transform: rotate(32deg); }
.network-preview__line--three { transform: rotate(-28deg); }

.network-preview__node {
  position: absolute;
  width: 11px;
  height: 11px;
  border: 2px solid #124d49;
  border-radius: 50%;
  background: #77c7bd;
  box-shadow: 0 0 0 6px rgba(119, 199, 189, 0.12);
  animation: portal-node 3.2s ease-in-out infinite;
}

.network-preview__node--one { top: 42%; left: 7%; }
.network-preview__node--two { top: 13%; left: 48%; animation-delay: -0.7s; }
.network-preview__node--three { top: 72%; left: 49%; animation-delay: -1.4s; }
.network-preview__node--four { top: 38%; right: 4%; animation-delay: -2.1s; background: #c18745; }
.network-preview__node--five { top: 43%; left: 47%; animation-delay: -2.7s; background: #f7f3e9; }

@keyframes portal-node { 50% { box-shadow: 0 0 0 11px rgba(119, 199, 189, 0.05); transform: scale(1.12); } }

@media (max-width: 820px) {
  .course-portal { padding-top: 56px; }
  .course-portal__hero { grid-template-columns: 1fr; gap: 18px; }
  .course-portal__eyebrow { margin-bottom: 4px; }
  .course-portal__choices { grid-template-columns: 1fr; }
  .course-choice { min-height: 340px; }
}

@media (max-width: 520px) {
  .course-portal__hero h1 { font-size: 3.35rem; }
  .term-preview,
  .network-preview { opacity: 0.5; }
}

@media (prefers-reduced-motion: reduce) {
  .course-choice,
  .course-choice__action i,
  .network-preview__node { animation: none; transition: none; }
}
</style>
