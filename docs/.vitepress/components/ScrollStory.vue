<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import CourseGrid from './CourseGrid.vue'

const repository = 'https://github.com/hadanice/OpenDS'
const activeScene = ref(0)
const sceneElements: HTMLElement[] = []
let observer: IntersectionObserver | undefined

const sceneLabels = ['开场', '如何使用', '开始阅读', '学习方法']

const setSceneRef = (element: unknown, index: number) => {
  if (element instanceof HTMLElement) sceneElements[index] = element
}

const goToScene = (index: number) => {
  const target = sceneElements[Math.max(0, Math.min(index, sceneElements.length - 1))]
  if (!target) return
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' })
}

const onKeydown = (event: KeyboardEvent) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return
  const target = event.target as HTMLElement | null
  if (target?.closest('a, button, input, textarea, select, [contenteditable="true"]')) return

  const forward = event.key === 'ArrowDown' || event.key === 'PageDown' || event.key === ' '
  const backward = event.key === 'ArrowUp' || event.key === 'PageUp'
  if (!forward && !backward) return
  event.preventDefault()
  goToScene(activeScene.value + (forward ? 1 : -1))
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]
      if (!visible) return
      const index = sceneElements.indexOf(visible.target as HTMLElement)
      if (index >= 0) activeScene.value = index
    },
    { threshold: [0.25, 0.5, 0.7] }
  )
  sceneElements.forEach((element) => observer?.observe(element))
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <main class="scroll-story">
    <nav class="story-progress" aria-label="首页章节导航">
      <button
        v-for="(label, index) in sceneLabels"
        :key="label"
        type="button"
        :class="{ 'is-active': activeScene === index }"
        :aria-current="activeScene === index ? 'step' : undefined"
        :aria-label="`前往第 ${index + 1} 幕：${label}`"
        @click="goToScene(index)"
      >
        <span>{{ String(index + 1).padStart(2, '0') }}</span>
      </button>
    </nav>

    <section
      id="story-intro"
      :ref="(element: unknown) => setSceneRef(element, 0)"
      class="story-scene story-scene--intro"
      :class="{ 'is-active': activeScene === 0 }"
    >
      <div class="story-scene__sticky story-intro">
        <div class="story-intro__orbit" aria-hidden="true"><i /><i /><i /></div>
        <div class="story-intro__content story-reveal">
          <p class="story-kicker">Fudan Data Science · Open archive</p>
          <h1>OpenDS</h1>
          <h2>用知识沉淀一张地图</h2>
          <p>复旦大学大数据学院课程的笔记、作业、项目与自学资源。持续整理，开放分享。</p>
        </div>
        <button class="story-scroll-cue" type="button" @click="goToScene(1)">
          <span>向下展开</span><i aria-hidden="true" />
        </button>
      </div>
    </section>

    <section
      id="story-archive"
      :ref="(element: unknown) => setSceneRef(element, 1)"
      class="story-scene story-scene--archive"
      :class="{ 'is-active': activeScene === 1 }"
    >
      <div class="story-scene__sticky story-archive">
        <div class="story-archive__lead story-reveal">
          <p class="story-kicker">02 · Archive</p>
          <h2>沿着地图，进入每一份学习现场</h2>
          <div class="story-actions">
            <a class="story-button story-button--brand" :href="withBase('/courses/')">浏览课程</a>
            <a class="story-button" :href="repository" target="_blank" rel="noreferrer">查看仓库 ↗</a>
          </div>
        </div>
        <div class="story-feature-list">
          <article class="story-feature story-reveal" style="--delay: 80ms">
            <span aria-hidden="true">🗂️</span>
            <div><h3>按学期归档</h3><p>从课程全貌进入具体资料，快速找到笔记、作业、代码与项目。</p></div>
          </article>
          <article class="story-feature story-reveal" style="--delay: 160ms">
            <span aria-hidden="true">✦</span>
            <div><h3>持续生长</h3><p>随学习进度迭代更新，让零散记录逐渐形成可复用的知识结构。</p></div>
          </article>
          <article class="story-feature story-reveal" style="--delay: 240ms">
            <span aria-hidden="true">⌘</span>
            <div><h3>开放可追溯</h3><p>每份内容都回到 GitHub 原始文件，便于查看历史、提出问题和共同改进。</p></div>
          </article>
        </div>
      </div>
    </section>

    <section
      id="story-courses"
      :ref="(element: unknown) => setSceneRef(element, 2)"
      class="story-scene story-scene--courses"
      :class="{ 'is-active': activeScene === 2 }"
    >
      <div class="story-scene__sticky story-courses">
        <div class="story-section-head story-reveal">
          <div><p class="story-kicker">03 · First step</p><h2>从一门课程开始</h2></div>
          <p>不必一次看完整张地图。选择眼前最需要的一门课，沿着章节、公式、图表和项目继续向前。</p>
        </div>
        <div class="story-course-grid story-reveal"><CourseGrid featured /></div>
      </div>
    </section>

    <section
      id="story-method"
      :ref="(element: unknown) => setSceneRef(element, 3)"
      class="story-scene story-scene--method"
      :class="{ 'is-active': activeScene === 3 }"
    >
      <div class="story-scene__sticky story-method">
        <div class="story-section-head story-reveal">
          <div><p class="story-kicker">04 · Method</p><h2>记录，也是一种学习方法</h2></div>
        </div>
        <div class="story-principles">
          <article class="story-principle story-reveal" style="--delay: 70ms"><span>01</span><h3>先理解，再归档</h3><p>通过命名、分类和复盘，把一次性的课堂输入变成可检索的长期记忆。</p></article>
          <article class="story-principle story-reveal" style="--delay: 140ms"><span>02</span><h3>保留推导过程</h3><p>结论固然重要，但真正可迁移的是从问题、假设到方法与验证的完整思考路径。</p></article>
          <article class="story-principle story-reveal" style="--delay: 210ms"><span>03</span><h3>分享促进校正</h3><p>开放记录，接受错误、修正和补充，让每次反馈都成为知识网络的新连接。</p></article>
        </div>
        <footer class="story-footer story-reveal">
          <strong>知识因整理而清晰，因分享而生长。</strong>
          <span>Released under the MIT License · OpenDS。</span>
        </footer>
      </div>
    </section>
  </main>
</template>

<style scoped>
.scroll-story {
  position: relative;
  margin-top: calc(var(--vp-nav-height) * -1);
  background: var(--vp-c-bg);
}

.story-scene {
  position: relative;
  min-height: 110svh;
  scroll-margin-top: var(--vp-nav-height);
}

.story-scene__sticky {
  position: sticky;
  top: 0;
  display: flex;
  min-height: 100svh;
  padding: calc(var(--vp-nav-height) + 44px) max(28px, calc((100vw - 1240px) / 2)) 48px;
  overflow: hidden;
}

.story-progress {
  position: fixed;
  top: 50%;
  right: clamp(10px, 2vw, 30px);
  z-index: 20;
  display: flex;
  flex-direction: column;
  gap: 11px;
  transform: translateY(-50%);
}

.story-progress button {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 34px;
  border: 0;
  padding: 0;
  color: var(--vp-c-text-2);
  background: transparent;
  font: inherit;
  font-size: 0.62rem;
  cursor: pointer;
}

.story-progress button::after {
  width: 12px;
  height: 2px;
  margin-left: 7px;
  background: var(--vp-c-divider);
  content: '';
  transition: width 220ms ease, background-color 220ms ease;
}

.story-progress button.is-active::after,
.story-progress button:hover::after,
.story-progress button:focus-visible::after {
  width: 25px;
  background: var(--vp-c-brand-1);
}

.story-reveal {
  opacity: 0.22;
  transform: translateY(42px) scale(0.985);
  transition: opacity 520ms ease-out var(--delay, 0ms), transform 520ms cubic-bezier(0.22, 1, 0.36, 1) var(--delay, 0ms);
}

.story-scene.is-active .story-reveal {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.story-kicker {
  margin: 0 0 16px;
  color: var(--opends-gold);
  font-size: 0.72rem;
  font-weight: 780;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.story-intro {
  align-items: center;
  background:
    radial-gradient(circle at 72% 42%, rgba(178, 116, 50, 0.12), transparent 24rem),
    radial-gradient(circle at 18% 18%, rgba(23, 95, 90, 0.13), transparent 31rem),
    var(--vp-c-bg);
}

.story-intro__content {
  position: relative;
  z-index: 2;
  max-width: 920px;
}

.story-intro h1 {
  margin: 0;
  background: linear-gradient(120deg, var(--vp-c-brand-1) 14%, var(--vp-c-brand-3) 58%, var(--opends-gold));
  background-clip: text;
  color: transparent;
  font-family: var(--opends-serif);
  font-size: clamp(5rem, 15vw, 12rem);
  font-weight: 800;
  letter-spacing: -0.09em;
  line-height: 0.78;
}

.story-intro h2 {
  max-width: 820px;
  margin: clamp(34px, 6vh, 74px) 0 18px;
  font-family: var(--opends-serif);
  font-size: clamp(2rem, 5vw, 4.8rem);
  letter-spacing: -0.055em;
  line-height: 1.08;
}

.story-intro__content > p:last-child {
  max-width: 660px;
  margin: 0;
  color: var(--vp-c-text-2);
  font-size: clamp(0.96rem, 1.5vw, 1.12rem);
  line-height: 1.85;
}

.story-intro__orbit {
  position: absolute;
  top: 11%;
  right: 7%;
  width: min(42vw, 610px);
  aspect-ratio: 1;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  box-shadow: 0 0 0 46px rgba(23, 95, 90, 0.025), 0 0 0 92px rgba(178, 116, 50, 0.018);
}

.story-intro__orbit::before,
.story-intro__orbit::after {
  position: absolute;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  content: '';
}

.story-intro__orbit::before { inset: 19%; }
.story-intro__orbit::after { inset: 39%; }

.story-intro__orbit i {
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--vp-c-brand-2);
  box-shadow: 0 0 0 7px var(--vp-c-brand-soft);
}

.story-intro__orbit i:nth-child(1) { top: 11%; left: 26%; }
.story-intro__orbit i:nth-child(2) { top: 53%; right: -5px; background: var(--opends-gold); }
.story-intro__orbit i:nth-child(3) { bottom: 13%; left: 20%; }

.story-scroll-cue {
  position: absolute;
  bottom: 35px;
  left: 50%;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 0;
  color: var(--vp-c-text-2);
  background: transparent;
  font: inherit;
  font-size: 0.7rem;
  cursor: pointer;
  transform: translateX(-50%);
}

.story-scroll-cue i {
  display: block;
  width: 1px;
  height: 35px;
  background: linear-gradient(var(--vp-c-brand-1), transparent);
}

.story-archive {
  align-items: center;
  display: grid;
  grid-template-columns: minmax(0, 0.85fr) minmax(480px, 1.15fr);
  gap: clamp(50px, 8vw, 130px);
  background: var(--vp-c-bg-alt);
}

.story-archive__lead h2,
.story-section-head h2 {
  margin: 0;
  font-family: var(--opends-serif);
  font-size: clamp(2.5rem, 5vw, 5rem);
  letter-spacing: -0.06em;
  line-height: 1.08;
}

.story-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 34px;
}

.story-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 999px;
  padding: 0 20px;
  color: var(--vp-c-text-1) !important;
  background: var(--vp-c-bg);
  font-size: 0.86rem;
  font-weight: 740;
  text-decoration: none !important;
  transition: transform 160ms ease, box-shadow 160ms ease;
}

.story-button--brand {
  border-color: var(--vp-c-brand-1);
  color: white !important;
  background: var(--vp-c-brand-1);
  box-shadow: 0 12px 30px rgba(23, 95, 90, 0.18);
}

.story-button:hover { transform: translateY(-2px); }

.story-feature-list {
  display: grid;
  gap: 14px;
}

.story-feature {
  display: grid;
  grid-template-columns: 54px 1fr;
  gap: 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 18px;
  padding: 22px;
  background: color-mix(in srgb, var(--vp-c-bg) 84%, transparent);
  box-shadow: 0 10px 30px rgba(28, 41, 39, 0.045);
  backdrop-filter: blur(8px);
}

.story-feature > span {
  display: grid;
  place-items: center;
  width: 50px;
  height: 50px;
  border-radius: 14px;
  background: var(--vp-c-brand-soft);
  font-size: 1.45rem;
}

.story-feature h3 { margin: 0 0 6px; font-size: 1rem; }
.story-feature p { margin: 0; color: var(--vp-c-text-2); font-size: 0.88rem; line-height: 1.7; }

.story-courses,
.story-method {
  align-content: center;
  flex-direction: column;
  justify-content: center;
}

.story-courses {
  background:
    linear-gradient(rgba(23, 95, 90, 0.028) 1px, transparent 1px),
    var(--vp-c-bg);
  background-size: 100% 34px;
}

.story-section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 36px;
  width: 100%;
  margin-bottom: 28px;
}

.story-section-head > p {
  max-width: 450px;
  margin: 0;
  color: var(--vp-c-text-2);
  line-height: 1.75;
}

.story-course-grid {
  width: 100%;
}

.story-course-grid :deep(.course-browser) { margin-top: 0; }
.story-course-grid :deep(.course-card) { min-height: 205px; padding: 18px; }
.story-course-grid :deep(.course-card h3) { margin-top: 15px; font-size: 1rem; }
.story-course-grid :deep(.course-materials) { margin-top: 12px; }
.story-course-grid :deep(.course-card__link) { padding-top: 14px; }

.story-method {
  background:
    radial-gradient(circle at 84% 18%, rgba(178, 116, 50, 0.09), transparent 27rem),
    var(--vp-c-bg-alt);
}

.story-principles {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  width: 100%;
}

.story-principle {
  border-top: 1px solid var(--vp-c-divider);
  padding: 24px 18px 10px 0;
}

.story-principle span {
  color: var(--opends-gold);
  font-family: var(--opends-serif);
  font-size: 1.8rem;
}

.story-principle h3 { margin: 34px 0 10px; font-family: var(--opends-serif); font-size: 1.15rem; }
.story-principle p { max-width: 340px; margin: 0; color: var(--vp-c-text-2); line-height: 1.75; }

.story-footer {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 30px;
  width: 100%;
  margin-top: clamp(55px, 10vh, 110px);
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 22px;
}

.story-footer strong { font-family: var(--opends-serif); font-size: clamp(1.2rem, 2vw, 1.75rem); }
.story-footer span { color: var(--vp-c-text-2); font-size: 0.76rem; }

@media (max-width: 900px) {
  .story-scene { min-height: auto; }
  .story-scene__sticky { position: relative; top: auto; min-height: 100svh; }
  .story-progress { display: none; }
  .story-intro__orbit { right: -24%; width: 78vw; opacity: 0.55; }
  .story-archive { display: flex; align-items: stretch; flex-direction: column; justify-content: center; gap: 44px; }
  .story-section-head { align-items: flex-start; flex-direction: column; gap: 12px; }
  .story-principles { grid-template-columns: 1fr; }
  .story-footer { align-items: flex-start; flex-direction: column; }
  .story-courses { padding-top: calc(var(--vp-nav-height) + 70px); padding-bottom: 80px; }
}

@media (min-width: 901px) and (max-width: 1100px) {
  .story-scene--courses {
    min-height: auto;
  }

  .story-courses {
    position: relative;
    top: auto;
    min-height: auto;
    padding-top: calc(var(--vp-nav-height) + 70px);
    padding-bottom: 80px;
    overflow: visible;
  }
}

@media (max-width: 640px) {
  .story-scene__sticky { padding-inline: 22px; }
  .story-intro h1 { font-size: clamp(4.4rem, 25vw, 7rem); }
  .story-intro h2 { font-size: 2.35rem; }
  .story-feature { grid-template-columns: 44px 1fr; padding: 18px; }
  .story-feature > span { width: 42px; height: 42px; font-size: 1.15rem; }
}

@media (prefers-reduced-motion: reduce) {
  .story-reveal,
  .story-progress button::after,
  .story-button {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .story-scene { min-height: auto; }
  .story-scene__sticky { position: relative; min-height: 100svh; }
}
</style>
