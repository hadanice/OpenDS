import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import MermaidDiagram from '../components/MermaidDiagram.vue'
import SidebarControls from '../components/SidebarControls.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, {
    'layout-bottom': () => h(SidebarControls)
  }),
  enhanceApp({ app }) {
    app.component('MermaidDiagram', MermaidDiagram)
  }
}
