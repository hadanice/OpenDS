import { defineConfig } from 'vitepress'

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
    nav: [
      { text: '首页', link: '/' },
      { text: '课程', link: '/courses/' },
      { text: '学习资源', link: '/resources' },
      { text: '关于', link: '/about' },
      { text: 'English', link: '/en' }
    ],
    sidebar: [
      {
        text: 'OpenDS',
        items: [
          { text: '项目首页', link: '/' },
          { text: '课程地图', link: '/courses/' },
          { text: '学习资源', link: '/resources' },
          { text: '关于与贡献', link: '/about' },
          { text: 'English', link: '/en' }
        ]
      }
    ],
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
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  }
})
