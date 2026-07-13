import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  rmSync,
  statSync,
  writeFileSync
} from 'node:fs'
import { dirname, join, relative, resolve, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { publishedCourses } from './site-course-manifest.mjs'

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const docsRoot = resolve(repositoryRoot, 'docs')
const generatedRoot = resolve(docsRoot, 'notes')

if (!generatedRoot.startsWith(`${docsRoot}${sep}`)) {
  throw new Error(`Refusing to replace content outside docs: ${generatedRoot}`)
}

const markdownFiles = (directory) =>
  readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = join(directory, entry.name)
    if (entry.isDirectory()) return markdownFiles(fullPath)
    return entry.isFile() && entry.name.toLowerCase().endsWith('.md')
      ? [fullPath]
      : []
  })

const pageTitle = (content, fallback) => {
  const heading = content.match(/^#\s+(.+)$/m)?.[1]
  return (heading || fallback)
    .replace(/[`*_]/g, '')
    .replace(/\s+#+$/, '')
    .trim()
}

const yamlString = (value) => JSON.stringify(value)

rmSync(generatedRoot, { recursive: true, force: true })
mkdirSync(generatedRoot, { recursive: true })

let pageCount = 0

for (const course of publishedCourses) {
  const sourceRoot = resolve(repositoryRoot, course.source)
  const targetRoot = resolve(generatedRoot, course.slug)

  if (!existsSync(sourceRoot) || !statSync(sourceRoot).isDirectory()) {
    throw new Error(`Course source directory is missing: ${course.source}`)
  }

  for (const sourceFile of markdownFiles(sourceRoot)) {
    const sourceRelativePath = relative(sourceRoot, sourceFile)
    const isCourseReadme = sourceRelativePath.toLowerCase() === 'readme.md'
    const targetRelativePath = isCourseReadme ? 'index.md' : sourceRelativePath
    const targetFile = resolve(targetRoot, targetRelativePath)
    const content = readFileSync(sourceFile, 'utf8')
    const siteContent = content.replace(
      /^```math\s*\r?\n([\s\S]*?)^```\s*$/gm,
      (_match, formula) => `$$\n${formula.trim()}\n$$`
    )
    const fallbackTitle = isCourseReadme
      ? course.title
      : sourceRelativePath.replace(/\.md$/i, '')

    mkdirSync(dirname(targetFile), { recursive: true })
    writeFileSync(
      targetFile,
      [
        '---',
        `title: ${yamlString(pageTitle(content, fallbackTitle))}`,
        `course: ${yamlString(course.title)}`,
        `sourceFile: ${yamlString(`${course.source}/${sourceRelativePath}`)}`,
        '---',
        '',
        siteContent
      ].join('\n'),
      'utf8'
    )
    pageCount += 1
  }
}

console.log(`Synced ${pageCount} course pages into ${relative(repositoryRoot, generatedRoot)}.`)
