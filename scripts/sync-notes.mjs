import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs'
import { relative, resolve } from 'node:path'

const workspace = resolve(import.meta.dirname, '..')
const docsRoot = resolve(workspace, 'docs')
const generatedRoot = resolve(docsRoot, 'notes')
const cleanOnly = process.argv.includes('--clean')

if (relative(docsRoot, generatedRoot).startsWith('..')) {
  throw new Error('Refusing to modify a generated path outside docs/.')
}

rmSync(generatedRoot, { recursive: true, force: true })

if (cleanOnly) process.exit(0)

const noteSources = [
  ['advanced-linear-algebra', '高等线性代数'],
  ['numerical-algorithms', '数值算法与案例分析Ⅰ'],
  ['probability', '概率论基础'],
  ['algorithms', '算法与数据结构'],
  ['computer-systems', '计算机原理'],
  ['optimization', '最优化方法'],
  ['database', '数据库及实现'],
  ['nlp-llms', '自然语言处理与大语言模型'],
  ['mathematical-statistics', '统计学基础Ⅰ：数理统计'],
  ['biostatistics', '生物统计学']
]

mkdirSync(generatedRoot, { recursive: true })

for (const [slug, courseDirectory] of noteSources) {
  const source = resolve(workspace, courseDirectory, '笔记')
  const destination = resolve(generatedRoot, slug)

  if (!existsSync(source)) {
    throw new Error(`Missing note source: ${relative(workspace, source)}`)
  }

  cpSync(source, destination, { recursive: true })
}
