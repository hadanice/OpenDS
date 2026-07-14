<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import CourseGrid from './CourseGrid.vue'

const repository = 'https://github.com/hadanice/OpenDS'
const activeScene = ref(0)
const transitionDirection = ref<'forward' | 'backward'>('forward')
const sceneElements: HTMLElement[] = []
const sceneLabels = ['开场', '如何使用', '开始阅读', '学习方法']

let touchStartX = 0
let touchStartY = 0

const setSceneRef = (element: unknown, index: number) => {
  if (element instanceof HTMLElement) sceneElements[index] = element
}

const goToScene = (index: number) => {
  const nextScene = Math.max(0, Math.min(index, sceneLabels.length - 1))
  if (nextScene === activeScene.value) return

  transitionDirection.value = nextScene > activeScene.value ? 'forward' : 'backward'
  activeScene.value = nextScene
  void nextTick(() => {
    const panel = sceneElements[nextScene]
    if (panel) panel.scrollTop = 0
  })
}

const onTouchStart = (event: TouchEvent) => {
  const touch = event.changedTouches[0]
  touchStartX = touch.clientX
  touchStartY = touch.clientY
}

const onTouchEnd = (event: TouchEvent) => {
  if (!window.matchMedia('(max-width: 900px)').matches) return

  const touch = event.changedTouches[0]
  const deltaX = touch.clientX - touchStartX
  const deltaY = touch.clientY - touchStartY
  const isHorizontalSwipe = Math.abs(deltaX) > 56 && Math.abs(deltaX) > Math.abs(deltaY) * 1.25

  if (isHorizontalSwipe) goToScene(activeScene.value + (deltaX < 0 ? 1 : -1))
}

onMounted(() => {
  document.documentElement.classList.add('opends-story-mode')
})

onBeforeUnmount(() => {
  document.documentElement.classList.remove('opends-story-mode')
})
</script>

<template>
  <main
    class="scroll-story"
    :class="`is-moving-${transitionDirection}`"
    @touchstart.passive="onTouchStart"
    @touchend.passive="onTouchEnd"
  >
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
        <span>{{ index + 1 }}</span>
      </button>
    </nav>

    <div class="story-track" :style="{ transform: `translate3d(-${activeScene * 100}%, 0, 0)` }">
      <section
        id="story-intro"
        :ref="(element: unknown) => setSceneRef(element, 0)"
        class="story-scene story-scene--intro"
        :class="{ 'is-active': activeScene === 0 }"
      >
        <div class="story-scene__panel story-intro">
          <div class="story-intro__orbit" aria-hidden="true"><i /><i /><i /></div>
          <div class="story-intro__content story-reveal">
            <p class="story-kicker">Fudan Data Science · Open archive</p>
            <h1>OpenDS</h1>
            <h2>用知识沉淀一张地图</h2>
            <p>复旦大学大数据学院课程的笔记、作业、项目与自学资源。持续整理，开放分享。</p>
          </div>
        </div>
      </section>

      <section
        id="story-archive"
        :ref="(element: unknown) => setSceneRef(element, 1)"
        class="story-scene story-scene--archive"
        :class="{ 'is-active': activeScene === 1 }"
      >
        <div class="story-scene__panel story-archive">
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
        <div class="story-scene__panel story-courses">
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
        <div class="story-scene__panel story-method">
          <div class="story-section-head story-reveal">
            <div><p class="story-kicker">04 · Method</p><h2>记录，也是一种学习方法</h2></div>
          </div>
          <div class="story-principles">
            <article class="story-principle story-reveal" style="--delay: 70ms"><span>01</span><h3>先理解，再归档</h3><p>通过命名、分类和复盘，把一次性的课堂输入变成可检索的长期记忆。</p></article>
            <article class="story-principle story-reveal" style="--delay: 140ms"><span>02</span><h3>保留推导过程</h3><p>结论固然重要，但真正可迁移的是从问题、假设到方法与验证的完整思考路径。</p></article>
            <article class="story-principle story-reveal" style="--delay: 210ms"><span>03</span><h3>分享促进校正</h3><p>开放记录，接受错误、修正和补充，让每次反馈都成为知识网络的新连接。</p></article>
          </div>
          <footer class="story-end-footer story-reveal">
            <strong>知识因整理而清晰，因分享而生长。</strong>
            <span>Released under the MIT License · OpenDS</span>
          </footer>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
:global(html.opends-story-mode),
:global(html.opends-story-mode body) {
  overflow: hidden;
}

.scroll-story {
  position: relative;
  height: 100svh;
  margin-top: calc(var(--vp-nav-height) * -1);
  overflow: hidden;
  background: var(--vp-c-bg);
  touch-action: pan-y;
}

.story-track {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 860ms cubic-bezier(0.22, 1, 0.36, 1);
  will-change: transform;
}

.story-scene {
  flex: 0 0 100%;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  overscroll-behavior: contain;
  scrollbar-color: var(--vp-c-divider) transparent;
  scrollbar-width: thin;
}

.story-scene__panel {
  --story-gutter: max(28px, calc((100vw - 1240px) / 2));
  position: relative;
  display: flex;
  min-height: 100%;
  padding: calc(var(--vp-nav-height) + 44px) var(--story-gutter) 48px;
  overflow: hidden;
}

.story-progress {
  position: absolute;
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
  opacity: 0;
  transform: translateY(46px) scale(0.98);
  transition: opacity 560ms ease-out var(--delay, 100ms), transform 650ms cubic-bezier(0.22, 1, 0.36, 1) var(--delay, 100ms);
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
  display: inline-block;
  margin: 0;
  background: linear-gradient(120deg, var(--vp-c-brand-1) 14%, var(--vp-c-brand-3) 58%, var(--opends-gold));
  background-clip: text;
  color: transparent;
  font-family: var(--opends-serif);
  font-size: clamp(4.5rem, 11.5vw, 9.5rem);
  font-weight: 800;
  letter-spacing: -0.075em;
  line-height: 1.08;
  padding-bottom: 0.08em;
}

.story-intro h2 {
  max-width: 820px;
  margin: clamp(8px, 2vh, 24px) 0 18px;
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
  inset: 0;
  border-radius: 50%;
  animation: story-orbit 24s linear infinite;
}

.story-intro__orbit i::after {
  position: absolute;
  top: -5px;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--vp-c-brand-2);
  box-shadow: 0 0 0 7px var(--vp-c-brand-soft);
  content: '';
  transform: translateX(-50%);
}

.story-intro__orbit i:nth-child(1) { inset: 0; animation-delay: -2s; animation-duration: 22s; }
.story-intro__orbit i:nth-child(2) { inset: 19%; animation-delay: -10s; animation-duration: 28s; animation-direction: reverse; }
.story-intro__orbit i:nth-child(2)::after { background: var(--opends-gold); }
.story-intro__orbit i:nth-child(3) { inset: 39%; animation-delay: -17s; animation-duration: 34s; }

@keyframes story-orbit {
  to { transform: rotate(1turn); }
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

.story-course-grid { width: 100%; }
.story-course-grid :deep(.course-browser) { margin-top: 0; }
.story-course-grid :deep(.course-card) { min-height: 205px; padding: 18px; }
.story-course-grid :deep(.course-card h3) { margin-top: 15px; font-size: 1rem; }
.story-course-grid :deep(.course-materials) { margin-top: 12px; }
.story-course-grid :deep(.course-card__link) { padding-top: 14px; }

.story-method {
  padding-bottom: 0;
  background:
    radial-gradient(circle at 84% 18%, rgba(178, 116, 50, 0.09), transparent 27rem),
    var(--vp-c-bg-alt);
}

.story-principles {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  width: 100%;
  margin-bottom: 32px;
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

.story-end-footer {
  align-self: stretch;
  width: auto;
  margin: auto calc(0px - var(--story-gutter)) 0;
  border-top: 1px solid var(--vp-c-gutter);
  padding: 32px;
  color: var(--vp-c-text-2);
  background-color: var(--vp-c-bg);
  text-align: center;
}

.story-end-footer strong,
.story-end-footer span {
  display: block;
  color: var(--vp-c-text-2);
  font-family: var(--vp-font-family-base);
  font-size: 14px;
  font-weight: 500;
  line-height: 24px;
}

@media (min-width: 901px) {
  .scroll-story.is-moving-forward .story-scene.is-active .story-scene__panel {
    animation: story-arrive-forward 760ms cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  .scroll-story.is-moving-backward .story-scene.is-active .story-scene__panel {
    animation: story-arrive-backward 760ms cubic-bezier(0.22, 1, 0.36, 1) both;
  }

  @keyframes story-arrive-forward {
    from { opacity: 0.55; filter: blur(5px); transform: translateX(54px) scale(0.985); }
    to { opacity: 1; filter: blur(0); transform: translateX(0) scale(1); }
  }

  @keyframes story-arrive-backward {
    from { opacity: 0.55; filter: blur(5px); transform: translateX(-54px) scale(0.985); }
    to { opacity: 1; filter: blur(0); transform: translateX(0) scale(1); }
  }
}

@media (max-width: 900px) {
  .story-progress { display: none; }
  .story-scene__panel {
    min-height: 100%;
    padding-top: calc(var(--vp-nav-height) + 40px);
    padding-bottom: 54px;
  }
  .story-intro__orbit { right: -24%; width: 78vw; opacity: 0.55; }
  .story-archive { display: flex; align-items: stretch; flex-direction: column; justify-content: center; gap: 44px; }
  .story-section-head { align-items: flex-start; flex-direction: column; gap: 12px; }
  .story-principles { grid-template-columns: 1fr; }
  .story-courses,
  .story-method { justify-content: flex-start; }
  .story-method { padding-bottom: 0; }
}

@media (max-width: 640px) {
  .story-scene__panel { --story-gutter: 22px; padding-inline: var(--story-gutter); }
  .story-intro h1 { font-size: clamp(4rem, 23vw, 6.5rem); line-height: 1.08; }
  .story-intro h2 { font-size: 2.35rem; }
  .story-feature { grid-template-columns: 44px 1fr; padding: 18px; }
  .story-feature > span { width: 42px; height: 42px; font-size: 1.15rem; }
  .story-principle h3 { margin-top: 18px; }
}

@media (prefers-reduced-motion: reduce) {
  .story-track,
  .story-reveal,
  .story-progress button::after,
  .story-button {
    transition: none;
  }

  .story-scene__panel,
  .story-intro__orbit i {
    animation: none !important;
  }

  .story-reveal {
    opacity: 1;
    transform: none;
  }
}
</style>
