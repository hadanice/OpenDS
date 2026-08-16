export type CourseTerm = '25秋' | '26春' | '26秋' | '27春' | '方向选修'
export type CourseDirection = '专业核心' | '统计分析' | '系统与数据挖掘' | '理医工' | '社会科学'

export interface Course {
  title: string
  code: string
  term: CourseTerm
  direction: CourseDirection
  slug?: string
}

export const courses: Course[] = [
  { title: '高等线性代数', code: 'MATH10003', term: '25秋', direction: '专业核心', slug: 'advanced-linear-algebra' },
  { title: '数值算法与案例分析Ⅰ', code: 'MATH20007', term: '25秋', direction: '专业核心', slug: 'numerical-algorithms' },
  { title: '概率论基础', code: 'STAT20011', term: '25秋', direction: '专业核心', slug: 'probability' },
  { title: '算法与数据结构', code: 'CS20017h', term: '25秋', direction: '专业核心', slug: 'algorithms' },
  { title: '计算机原理', code: 'CS20018', term: '25秋', direction: '专业核心', slug: 'computer-systems' },
  { title: '最优化方法', code: 'MATH20008', term: '26春', direction: '专业核心', slug: 'optimization' },
  { title: '数据库及实现', code: 'CS20019', term: '26春', direction: '专业核心', slug: 'database' },
  { title: '自然语言处理与大语言模型', code: 'CS40008', term: '26春', direction: '系统与数据挖掘', slug: 'nlp-llms' },
  { title: '统计学基础Ⅰ：数理统计', code: 'STAT20010h', term: '26春', direction: '专业核心', slug: 'mathematical-statistics' },
  { title: '生物统计学', code: 'STAT50025', term: '26春', direction: '理医工', slug: 'biostatistics' },
  { title: '统计计算', code: 'STAT30016h', term: '26秋', direction: '专业核心' },
  { title: '统计（机器）学习概论', code: 'STAT30015', term: '26秋', direction: '专业核心' },
  { title: '人工智能', code: 'CS50020', term: '26秋', direction: '专业核心' },
  { title: '图像处理与数据可视化', code: 'CS30065h', term: '26秋', direction: '专业核心' },
  { title: '图数据管理与挖掘', code: 'CS50027', term: '26秋', direction: '系统与数据挖掘' },
  { title: '多模态数据同化', code: 'AIS410010', term: '26秋', direction: '统计分析' },
  { title: '神经网络与深度学习', code: 'CS30064', term: '27春', direction: '专业核心' },
  { title: '时间序列与空间统计', code: 'STAT50016', term: '方向选修', direction: '统计分析' },
  { title: '计算机视觉', code: 'CS50028', term: '方向选修', direction: '系统与数据挖掘' },
  { title: '社会科学数据挖掘', code: 'CS50019', term: '方向选修', direction: '社会科学' },
  { title: '金融工程', code: 'STAT50022', term: '方向选修', direction: '社会科学' }
]

export type PublishedCourse = Course & { slug: string }

export const publishedCourses = courses.filter(
  (course): course is PublishedCourse => Boolean(course.slug)
)

export const termOrder: CourseTerm[] = ['25秋', '26春', '26秋', '27春', '方向选修']
export const directionOrder: CourseDirection[] = ['专业核心', '统计分析', '系统与数据挖掘', '理医工', '社会科学']
