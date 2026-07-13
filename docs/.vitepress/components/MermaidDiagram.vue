<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useData } from 'vitepress'

const props = defineProps<{
  code: string
}>()

const { isDark } = useData()
const diagram = ref<HTMLElement | null>(null)
const sourceText = ref('')
const errorMessage = ref('')
const loading = ref(true)

let disposed = false
let renderCycle = 0

const decodeSource = () => {
  const bytes = Uint8Array.from(atob(props.code), (character) => character.charCodeAt(0))
  return new TextDecoder().decode(bytes)
}

const renderDiagram = async () => {
  if (!diagram.value) return

  const cycle = ++renderCycle
  loading.value = true
  errorMessage.value = ''
  sourceText.value = decodeSource()

  await nextTick()

  try {
    const { default: mermaid } = await import('mermaid')
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: isDark.value ? 'dark' : 'neutral',
      fontFamily: 'Inter, "Noto Sans SC", "Microsoft YaHei", sans-serif',
      flowchart: {
        htmlLabels: true,
        useMaxWidth: true
      }
    })

    await mermaid.parse(sourceText.value)
    const id = `opends-mermaid-${Date.now()}-${Math.random().toString(36).slice(2)}`
    const { svg, bindFunctions } = await mermaid.render(id, sourceText.value)

    if (disposed || cycle !== renderCycle || !diagram.value) return
    diagram.value.innerHTML = svg
    bindFunctions?.(diagram.value)
  } catch (error) {
    if (disposed || cycle !== renderCycle || !diagram.value) return
    diagram.value.replaceChildren()
    errorMessage.value = error instanceof Error ? error.message : String(error)
  } finally {
    if (!disposed && cycle === renderCycle) loading.value = false
  }
}

onMounted(renderDiagram)
watch(isDark, renderDiagram, { flush: 'post' })

onBeforeUnmount(() => {
  disposed = true
  renderCycle += 1
})
</script>

<template>
  <figure class="mermaid-shell">
    <div
      ref="diagram"
      class="mermaid-diagram"
      role="img"
      aria-label="课程知识图表"
    />
    <p v-if="loading" class="mermaid-status">图表渲染中…</p>
    <details v-if="errorMessage" class="mermaid-error">
      <summary>图表暂时无法渲染</summary>
      <p>{{ errorMessage }}</p>
      <pre><code>{{ sourceText }}</code></pre>
    </details>
  </figure>
</template>

<style scoped>
.mermaid-shell {
  position: relative;
  margin: 1.4rem 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 16px;
  padding: 20px;
  overflow-x: auto;
  background: color-mix(in srgb, var(--vp-c-bg-soft) 72%, transparent);
}

.mermaid-diagram {
  min-width: 520px;
  text-align: center;
}

.mermaid-diagram :deep(svg) {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 0 auto;
}

.mermaid-status {
  margin: 0;
  padding: 28px 12px;
  color: var(--vp-c-text-2);
  text-align: center;
}

.mermaid-error {
  color: var(--vp-c-danger-1);
}

.mermaid-error p {
  font-size: 0.86rem;
}

.mermaid-error pre {
  max-height: 260px;
  overflow: auto;
}

@media (max-width: 640px) {
  .mermaid-shell {
    margin-inline: -12px;
    padding: 14px;
  }

  .mermaid-diagram {
    min-width: 460px;
  }
}
</style>
