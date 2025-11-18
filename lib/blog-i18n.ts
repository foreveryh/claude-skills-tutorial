// Blog UI translations
export const blogTranslations = {
  en: {
    blog: 'Blog',
    blogDescription: 'Product news and best practices for teams building with Claude.',
    filterAndSort: 'Filter and sort',
    sortBy: 'Sort by',
    category: 'Category',
    difficulty: 'Difficulty',
    tags: 'Tags',
    search: 'Search posts',
    gridView: 'Grid view',
    listView: 'List view',
    posts: 'posts',
    newest: 'Newest',
    oldest: 'Oldest',
    aToZ: 'Alphabetically (A to Z)',
    zToA: 'Alphabetically (Z to A)',
    // Category translations
    categories: {
      development: 'Development',
      'ai-ml': 'AI & Machine Learning',
    },
    // Difficulty translations
    difficulties: {
      beginner: 'Beginner',
      intermediate: 'Intermediate',
      advanced: 'Advanced',
    },
  },
  zh: {
    blog: '博客',
    blogDescription: '使用 Claude 构建团队的产品新闻和最佳实践。',
    filterAndSort: '筛选和排序',
    sortBy: '排序方式',
    category: '分类',
    difficulty: '难度',
    tags: '标签',
    search: '搜索文章',
    gridView: '网格视图',
    listView: '列表视图',
    posts: '篇文章',
    newest: '最新',
    oldest: '最旧',
    aToZ: '按字母顺序 (A 到 Z)',
    zToA: '按字母顺序 (Z 到 A)',
    // Category translations
    categories: {
      development: '开发',
      'ai-ml': 'AI 与机器学习',
    },
    // Difficulty translations
    difficulties: {
      beginner: '初级',
      intermediate: '中级',
      advanced: '高级',
    },
  },
  fr: {
    blog: 'Blog',
    blogDescription: 'Actualités produits et meilleures pratiques pour les équipes utilisant Claude.',
    filterAndSort: 'Filtrer et trier',
    sortBy: 'Trier par',
    category: 'Catégorie',
    difficulty: 'Difficulté',
    tags: 'Étiquettes',
    search: 'Rechercher des articles',
    gridView: 'Vue en grille',
    listView: 'Vue en liste',
    posts: 'articles',
    newest: 'Plus récent',
    oldest: 'Plus ancien',
    aToZ: 'Alphabétique (A à Z)',
    zToA: 'Alphabétique (Z à A)',
    // Category translations
    categories: {
      development: 'Développement',
      'ai-ml': 'IA et Apprentissage Automatique',
    },
    // Difficulty translations
    difficulties: {
      beginner: 'Débutant',
      intermediate: 'Intermédiaire',
      advanced: 'Avancé',
    },
  },
} as const;

export type Language = keyof typeof blogTranslations;
export type BlogTranslations = typeof blogTranslations.en;

export function getBlogTranslations(lang: string): BlogTranslations {
  const normalizedLang = lang.toLowerCase() as Language;
  return (blogTranslations[normalizedLang] || blogTranslations.en) as BlogTranslations;
}

// Helper to translate category
export function translateCategory(category: string | undefined, lang: string): string {
  if (!category) return '';
  const t = getBlogTranslations(lang);
  return t.categories[category as keyof typeof t.categories] || category;
}

// Helper to translate difficulty
export function translateDifficulty(difficulty: string | undefined, lang: string): string {
  if (!difficulty) return '';
  const t = getBlogTranslations(lang);
  return t.difficulties[difficulty as keyof typeof t.difficulties] || difficulty;
}
