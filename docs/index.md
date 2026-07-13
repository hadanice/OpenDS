---
layout: home
title: OpenDS
titleTemplate: 数据科学学习档案

hero:
  name: OpenDS
  text: 把学习沉淀为一张知识地图
  tagline: 复旦大学大数据学院课程的笔记、作业、项目与自学资源。持续整理，开放分享。
  actions:
    - theme: brand
      text: 浏览课程
      link: /courses/
    - theme: alt
      text: 查看仓库
      link: https://github.com/hadanice/OpenDS

features:
  - icon: 🗂️
    title: 按学期归档
    details: 从课程全貌进入具体资料，快速找到笔记、作业、代码与项目。
  - icon: ✦
    title: 持续生长
    details: 随学习进度迭代更新，让零散记录逐渐形成可复用的知识结构。
  - icon: ⌘
    title: 开放可追溯
    details: 每份内容都回到 GitHub 原始文件，便于查看历史、提出问题和共同改进。
---

<script setup>
import CourseGrid from './.vitepress/components/CourseGrid.vue'
</script>

<section class="home-section">
  <p class="home-section__eyebrow">Featured archive</p>
  <div class="home-section__head">
    <h2>从一门课程开始</h2>
    <p>这里展示已有资料的代表性课程。完整课程表可以按学期筛选，计划中的内容也会提前列入路线图。</p>
  </div>
  <CourseGrid featured />
</section>

<section class="home-section">
  <p class="home-section__eyebrow">Working principles</p>
  <div class="home-section__head">
    <h2>记录，也是一种学习方法</h2>
  </div>
  <div class="home-principles">
    <article class="principle-card">
      <span class="principle-card__number">01</span>
      <h3>先理解，再归档</h3>
      <p>通过命名、分类和复盘，把一次性的课堂输入变成可检索的长期记忆。</p>
    </article>
    <article class="principle-card">
      <span class="principle-card__number">02</span>
      <h3>保留推导过程</h3>
      <p>结论固然重要，但真正可迁移的是从问题、假设到方法与验证的完整思考路径。</p>
    </article>
    <article class="principle-card">
      <span class="principle-card__number">03</span>
      <h3>分享促进校正</h3>
      <p>开放记录，接受错误、修正和补充。欢迎通过 Issue 提出问题或分享更好的解释。</p>
    </article>
  </div>
</section>
