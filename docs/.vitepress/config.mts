import { defineConfig } from 'vitepress'
import { Buffer } from 'node:buffer'
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { publishedCourses } from './course-data'

const notesRoot = fileURLToPath(new URL('../notes/', import.meta.url))

const markdownPages = (directory: string): string[] => {
  if (!existsSync(directory)) return []

  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = join(directory, entry.name)
    if (entry.isDirectory()) return markdownPages(fullPath)
    return entry.isFile() && entry.name.toLowerCase().endsWith('.md') ? [fullPath] : []
  })
}

const sidebarLabel = (filePath: string) => {
  const content = readFileSync(filePath, 'utf8')
  const heading = content.match(/^#\s+(.+)$/m)?.[1]
  if (heading) return heading.replace(/[`*_]/g, '').replace(/\s+#+$/, '').trim()

  return filePath
    .split(/[\\/]/)
    .pop()!
    .replace(/\.md$/i, '')
    .replace(/_/g, ' · ')
}

const courseSidebar = (course: (typeof publishedCourses)[number]) => {
  const courseRoot = join(notesRoot, course.slug)
  const pages = markdownPages(courseRoot)
    .filter((file) => relative(courseRoot, file).replace(/\\/g, '/') !== 'index.md')
    .sort((left, right) => left.localeCompare(right, 'zh-CN', { numeric: true }))
    .map((file) => ({
      text: sidebarLabel(file),
      link: `/notes/${course.slug}/${relative(courseRoot, file)
        .replace(/\\/g, '/')
        .replace(/\.md$/i, '')}`
    }))

  return [
    {
      text: `${course.code} · ${course.title}`,
      items: [
        { text: '课程概览', link: `/notes/${course.slug}/` },
        ...pages
      ]
    },
    {
      text: '浏览',
      items: [
        { text: '按学期', link: '/courses/terms' },
        { text: '按方向模块', link: '/courses/map' }
      ]
    }
  ]
}

const noteSidebars = Object.fromEntries(
  publishedCourses.map((course) => [`/notes/${course.slug}/`, courseSidebar(course)])
)

export default defineConfig({
  lang: 'zh-CN',
  title: 'OpenDS',
  description: '复旦大学大数据学院课程的笔记。持续整理，开放分享。',
  base: '/OpenDS/',
  cleanUrls: true,
  sitemap: {
    hostname: 'https://hadanice.github.io/OpenDS/'
  },
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/OpenDS/opends-icon.svg' }],
    ['meta', { name: 'theme-color', content: '#111111' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'OpenDS' }],
    ['meta', { property: 'og:title', content: 'OpenDS' }],
    ['meta', { property: 'og:description', content: '复旦大学大数据学院课程的笔记。' }]
  ],
  themeConfig: {
    siteTitle: 'OpenDS',
    logo: { src: '/opends-icon.svg', alt: 'OpenDS' },
    nav: [
      { text: '按学期', link: '/courses/terms' },
      { text: '按方向模块', link: '/courses/map' }
    ],
    sidebar: noteSidebars,
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索站点' },
          modal: {
            noResultsText: '没有找到相关内容',
            resetButtonTitle: '清除查询',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' }
          }
        }
      }
    },
    outline: { label: '本页目录', level: [2, 3] },
    docFooter: { prev: '上一页', next: '下一页' }
  },
  markdown: {
    math: {
      svg: {
        fontCache: 'none'
      }
    },
    languageAlias: { gdb: 'text' },
    config: (markdown) => {
      const defaultFence = markdown.renderer.rules.fence!
      markdown.renderer.rules.fence = (tokens, index, options, env, self) => {
        const token = tokens[index]
        if (token.info.trim().split(/\s+/)[0] === 'mermaid') {
          const code = Buffer.from(token.content, 'utf8').toString('base64')
          return `<MermaidDiagram code="${code}" />`
        }
        return defaultFence(tokens, index, options, env, self)
      }
    },
    lineNumbers: true,
    theme: { light: 'github-light', dark: 'github-dark' }
  }
})
