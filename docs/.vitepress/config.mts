import { defineConfig } from 'vitepress'
import { Buffer } from 'node:buffer'
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { publishedCourses } from './course-manifest.mjs'

const notesRoot = fileURLToPath(new URL('../notes/', import.meta.url))

const markdownPages = (directory: string): string[] => {
  if (!existsSync(directory)) return []

  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = join(directory, entry.name)
    if (entry.isDirectory()) return markdownPages(fullPath)
    return entry.isFile() && entry.name.toLowerCase().endsWith('.md')
      ? [fullPath]
      : []
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
      text: '课程导航',
      items: [
        { text: '返回课程入口', link: '/courses/' },
        { text: '查看课程地图', link: '/courses/map' },
        { text: '查看 GitHub 源目录', link: `https://github.com/hadanice/OpenDS/tree/main/docs/notes/${course.slug}` }
      ]
    }
  ]
}

const noteSidebars = Object.fromEntries(
  publishedCourses.map((course) => [
    `/notes/${course.slug}/`,
    courseSidebar(course)
  ])
)

export default defineConfig({
  lang: 'zh-CN',
  title: 'OpenDS',
  description: '复旦大学数据科学课程笔记、作业、项目与学习资源',
  base: '/OpenDS/',
  cleanUrls: true,
  lastUpdated: true,
  sitemap: {
    hostname: 'https://hadanice.github.io/OpenDS/'
  },
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/OpenDS/opends-icon.svg' }],
    ['meta', { name: 'theme-color', content: '#175f5a' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:site_name', content: 'OpenDS' }],
    ['meta', { property: 'og:title', content: 'OpenDS · 数据科学学习档案' }],
    ['meta', {
      property: 'og:description',
      content: '课程笔记、作业、项目与自学资源的开放索引。'
    }]
  ],
  themeConfig: {
    siteTitle: 'OpenDS',
    logo: '/opends-icon.svg',
    nav: [
      { text: '首页', link: '/' },
      { text: '课程', link: '/courses/' },
      { text: '学习资源', link: '/resources' },
      { text: '关于', link: '/about' },
      { text: 'English', link: '/en' }
    ],
    sidebar: {
      ...noteSidebars,
      '/': [
        {
          text: 'OpenDS',
          items: [
            { text: '项目首页', link: '/' },
            { text: '课程', link: '/courses/' },
            { text: '学习资源', link: '/resources' },
            { text: '关于与贡献', link: '/about' },
            { text: 'English', link: '/en' }
          ]
        }
      ]
    },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索',
            buttonAriaLabel: '搜索站点'
          },
          modal: {
            noResultsText: '没有找到相关内容',
            resetButtonTitle: '清除查询',
            footer: {
              selectText: '选择',
              navigateText: '切换',
              closeText: '关闭'
            }
          }
        }
      }
    },
    outline: {
      label: '本页目录',
      level: [2, 3]
    },
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'medium',
        timeStyle: 'short'
      }
    },
    editLink: {
      pattern: 'https://github.com/hadanice/OpenDS/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/hadanice/OpenDS' }
    ],
    footer: {
      message: '知识因整理而清晰，因分享而生长。',
      copyright: 'Released under the MIT License · OpenDS'
    }
  },
  markdown: {
    math: {
      svg: {
        // Keep every formula self-contained. The global cache emits <use>
        // references without their shared <defs> in statically rendered pages.
        fontCache: 'none'
      }
    },
    languageAlias: {
      gdb: 'text'
    },
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
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  }
})
