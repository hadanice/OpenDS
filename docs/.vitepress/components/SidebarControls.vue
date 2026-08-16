<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vitepress'

type SidebarSide = 'left' | 'right'

const LEFT_DEFAULT = 300
const LEFT_MIN = 220
const LEFT_MAX = 480
const RIGHT_DEFAULT = 288
const RIGHT_MIN = 220
const RIGHT_MAX = 480
const CONTENT_RESERVE = 720

const route = useRoute()
const leftWidth = ref(LEFT_DEFAULT)
const rightWidth = ref(RIGHT_DEFAULT)
const leftCollapsed = ref(false)
const rightCollapsed = ref(false)
const leftAvailable = ref(false)
const rightAvailable = ref(false)
const leftControlX = ref(18)
const rightControlX = ref(0)
const dragging = ref<SidebarSide | null>(null)

let resizeObserver: ResizeObserver | undefined
let dragStartX = 0
let dragStartWidth = 0

const clamp = (value: number, minimum: number, maximum: number) =>
  Math.min(Math.max(value, minimum), Math.max(minimum, maximum))

const currentLeftMaximum = () => {
  const rightSpace = rightCollapsed.value || !rightAvailable.value ? 0 : rightWidth.value
  return Math.min(LEFT_MAX, window.innerWidth - rightSpace - CONTENT_RESERVE)
}

const currentRightMaximum = () => {
  const leftSpace = leftCollapsed.value || !leftAvailable.value ? 0 : leftWidth.value
  return Math.min(RIGHT_MAX, window.innerWidth - leftSpace - CONTENT_RESERVE)
}

const savePreferences = () => {
  try {
    localStorage.setItem('opends:left-sidebar-width', String(leftWidth.value))
    localStorage.setItem('opends:right-sidebar-width', String(rightWidth.value))
    localStorage.setItem('opends:left-sidebar-collapsed', String(leftCollapsed.value))
    localStorage.setItem('opends:right-sidebar-collapsed', String(rightCollapsed.value))
  } catch {
    // Storage may be unavailable in privacy modes; the controls still work.
  }
}

const loadPreferences = () => {
  try {
    const storedLeftWidth = Number(localStorage.getItem('opends:left-sidebar-width'))
    const storedRightWidth = Number(localStorage.getItem('opends:right-sidebar-width'))
    if (Number.isFinite(storedLeftWidth) && storedLeftWidth > 0) leftWidth.value = storedLeftWidth
    if (Number.isFinite(storedRightWidth) && storedRightWidth > 0) rightWidth.value = storedRightWidth
    leftCollapsed.value = localStorage.getItem('opends:left-sidebar-collapsed') === 'true'
    rightCollapsed.value = localStorage.getItem('opends:right-sidebar-collapsed') === 'true'
  } catch {
    // Use defaults when storage cannot be read.
  }
}

const applyLayoutState = () => {
  const root = document.documentElement
  leftWidth.value = clamp(leftWidth.value, LEFT_MIN, currentLeftMaximum())
  rightWidth.value = clamp(rightWidth.value, RIGHT_MIN, currentRightMaximum())
  root.style.setProperty('--opends-left-sidebar-width', `${leftWidth.value}px`)
  root.style.setProperty('--opends-right-sidebar-width', `${rightWidth.value}px`)
  root.classList.toggle('opends-left-sidebar-collapsed', leftCollapsed.value)
  root.classList.toggle('opends-right-sidebar-collapsed', rightCollapsed.value)
}

const updateControlPositions = () => {
  const leftSidebar = document.querySelector<HTMLElement>('.VPSidebar')
  const rightAside = document.querySelector<HTMLElement>('.VPDoc.has-aside .aside')

  leftAvailable.value = window.matchMedia('(min-width: 960px)').matches && Boolean(leftSidebar)
  rightAvailable.value = window.matchMedia('(min-width: 1280px)').matches && Boolean(rightAside)

  leftControlX.value = leftCollapsed.value || !leftSidebar
    ? 18
    : Math.round(leftSidebar.getBoundingClientRect().right)
  rightControlX.value = rightCollapsed.value || !rightAside
    ? window.innerWidth - 18
    : Math.round(rightAside.getBoundingClientRect().left)
}

const refreshLayout = async () => {
  applyLayoutState()
  await nextTick()
  requestAnimationFrame(() => {
    updateControlPositions()
    resizeObserver?.disconnect()
    resizeObserver = new ResizeObserver(updateControlPositions)
    const leftSidebar = document.querySelector<HTMLElement>('.VPSidebar')
    const rightAside = document.querySelector<HTMLElement>('.VPDoc.has-aside .aside')
    if (leftSidebar) resizeObserver.observe(leftSidebar)
    if (rightAside) resizeObserver.observe(rightAside)
  })
}

const toggleSidebar = (side: SidebarSide) => {
  if (side === 'left') leftCollapsed.value = !leftCollapsed.value
  else rightCollapsed.value = !rightCollapsed.value
  applyLayoutState()
  savePreferences()
  requestAnimationFrame(updateControlPositions)
}

const resizeSidebar = (side: SidebarSide, nextWidth: number) => {
  if (side === 'left') leftWidth.value = clamp(nextWidth, LEFT_MIN, currentLeftMaximum())
  else rightWidth.value = clamp(nextWidth, RIGHT_MIN, currentRightMaximum())
  applyLayoutState()
  requestAnimationFrame(updateControlPositions)
}

const onPointerMove = (event: PointerEvent) => {
  if (!dragging.value) return
  const delta = event.clientX - dragStartX
  resizeSidebar(
    dragging.value,
    dragging.value === 'left' ? dragStartWidth + delta : dragStartWidth - delta
  )
}

const stopDragging = () => {
  if (!dragging.value) return
  dragging.value = null
  document.documentElement.classList.remove('opends-resizing-sidebar')
  window.removeEventListener('pointermove', onPointerMove)
  window.removeEventListener('pointerup', stopDragging)
  savePreferences()
}

const startDragging = (side: SidebarSide, event: PointerEvent) => {
  if (event.button !== 0) return
  event.preventDefault()
  dragging.value = side
  dragStartX = event.clientX
  dragStartWidth = side === 'left' ? leftWidth.value : rightWidth.value
  document.documentElement.classList.add('opends-resizing-sidebar')
  window.addEventListener('pointermove', onPointerMove)
  window.addEventListener('pointerup', stopDragging)
}

const onSeparatorKeydown = (side: SidebarSide, event: KeyboardEvent) => {
  const currentWidth = side === 'left' ? leftWidth.value : rightWidth.value
  const direction = side === 'left'
    ? event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0
    : event.key === 'ArrowLeft' ? 1 : event.key === 'ArrowRight' ? -1 : 0
  if (!direction) return
  event.preventDefault()
  resizeSidebar(side, currentWidth + direction * 16)
  savePreferences()
}

const resetWidth = (side: SidebarSide) => {
  resizeSidebar(side, side === 'left' ? LEFT_DEFAULT : RIGHT_DEFAULT)
  savePreferences()
}

const onWindowResize = () => refreshLayout()

onMounted(() => {
  loadPreferences()
  refreshLayout()
  window.addEventListener('resize', onWindowResize)
})

watch(() => route.path, refreshLayout, { flush: 'post' })

onBeforeUnmount(() => {
  stopDragging()
  resizeObserver?.disconnect()
  window.removeEventListener('resize', onWindowResize)
})
</script>

<template>
  <template v-if="leftAvailable">
    <button
      class="opends-sidebar-toggle opends-sidebar-toggle--left"
      type="button"
      :style="{ left: `${leftControlX}px` }"
      :aria-expanded="!leftCollapsed"
      aria-controls="VPSidebarNav"
      :aria-label="leftCollapsed ? '展开左侧课程目录' : '收起左侧课程目录'"
      :title="leftCollapsed ? '展开课程目录' : '收起课程目录'"
      @click="toggleSidebar('left')"
    >
      <span aria-hidden="true">{{ leftCollapsed ? '›' : '‹' }}</span>
    </button>
    <div
      v-show="!leftCollapsed"
      class="opends-sidebar-resizer opends-sidebar-resizer--left"
      :class="{ 'is-dragging': dragging === 'left' }"
      :style="{ left: `${leftControlX}px` }"
      role="separator"
      aria-label="调整左侧课程目录宽度"
      aria-orientation="vertical"
      :aria-valuemin="LEFT_MIN"
      :aria-valuemax="Math.round(currentLeftMaximum())"
      :aria-valuenow="Math.round(leftWidth)"
      tabindex="0"
      title="拖动调整宽度；双击恢复默认"
      @pointerdown="startDragging('left', $event)"
      @keydown="onSeparatorKeydown('left', $event)"
      @dblclick="resetWidth('left')"
    />
  </template>

  <template v-if="rightAvailable">
    <button
      class="opends-sidebar-toggle opends-sidebar-toggle--right"
      type="button"
      :style="{ left: `${rightControlX}px` }"
      :aria-expanded="!rightCollapsed"
      aria-label="切换右侧本页目录"
      :title="rightCollapsed ? '展开本页目录' : '收起本页目录'"
      @click="toggleSidebar('right')"
    >
      <span aria-hidden="true">{{ rightCollapsed ? '‹' : '›' }}</span>
    </button>
    <div
      v-show="!rightCollapsed"
      class="opends-sidebar-resizer opends-sidebar-resizer--right"
      :class="{ 'is-dragging': dragging === 'right' }"
      :style="{ left: `${rightControlX}px` }"
      role="separator"
      aria-label="调整右侧本页目录宽度"
      aria-orientation="vertical"
      :aria-valuemin="RIGHT_MIN"
      :aria-valuemax="Math.round(currentRightMaximum())"
      :aria-valuenow="Math.round(rightWidth)"
      tabindex="0"
      title="拖动调整宽度；双击恢复默认"
      @pointerdown="startDragging('right', $event)"
      @keydown="onSeparatorKeydown('right', $event)"
      @dblclick="resetWidth('right')"
    />
  </template>
</template>

<style scoped>
.opends-sidebar-toggle,
.opends-sidebar-resizer {
  display: none;
}

@media (min-width: 960px) {
  .opends-sidebar-toggle {
    position: fixed;
    top: calc(var(--vp-nav-height) + 14px);
    z-index: calc(var(--vp-z-index-sidebar) + 3);
    display: grid;
    place-items: center;
    width: 24px;
    height: 32px;
    border: 1px solid var(--vp-c-divider);
    border-radius: 2px;
    color: var(--vp-c-text-2);
    background: var(--vp-c-bg);
    box-shadow: none;
    font-size: 20px;
    line-height: 1;
    cursor: pointer;
    transform: translateX(-50%);
    transition: color 0.2s, border-color 0.2s, background-color 0.2s;
  }

  .opends-sidebar-toggle:hover,
  .opends-sidebar-toggle:focus-visible {
    border-color: var(--vp-c-text-1);
    color: var(--vp-c-text-1);
    outline: none;
  }

  .opends-sidebar-resizer {
    position: fixed;
    top: var(--vp-nav-height);
    bottom: 0;
    z-index: calc(var(--vp-z-index-sidebar) + 2);
    display: block;
    width: 10px;
    cursor: col-resize;
    touch-action: none;
    transform: translateX(-50%);
  }

  .opends-sidebar-resizer::after {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 1px;
    background: var(--vp-c-divider);
    content: '';
    transform: translateX(-50%);
    transition: width 0.15s, background-color 0.15s;
  }

  .opends-sidebar-resizer:hover::after,
  .opends-sidebar-resizer:focus-visible::after,
  .opends-sidebar-resizer.is-dragging::after {
    width: 3px;
    background: var(--vp-c-text-1);
  }

  .opends-sidebar-resizer:focus-visible {
    outline: none;
  }
}

@media (min-width: 1280px) {
  .opends-sidebar-toggle--right,
  .opends-sidebar-resizer--right {
    display: grid;
  }

  .opends-sidebar-resizer--right {
    display: block;
  }
}
</style>
