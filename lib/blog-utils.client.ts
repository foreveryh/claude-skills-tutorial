// Client-side utilities that don't require Node.js APIs

export interface BlogPost {
  id: string;
  title: string;
  description: string;
  date: string;
  category?: string;
  difficulty?: string;
  tags: string[];
  slug: string;
  url: string;
  lang: string;
  author?: string;
  image?: string;
}

// Get color based on category
export function getCategoryColor(category?: string): string {
  const colors: Record<string, string> = {
    development: 'from-[#8ca978] to-[#7a9068]', // green
    'ai-ml': 'from-[#7db3e0] to-[#6b9bd4]', // blue
    tutorial: 'from-[#d4869c] to-[#c87890]', // pink
    guide: 'from-[#e89a6c] to-[#e08558]', // orange
    default: 'from-[#e0d4c8] to-[#d4c8b8]', // beige
  };

  return `bg-gradient-to-br ${colors[category || 'default'] || colors.default}`;
}

// Format date for display
export function formatDate(dateString: string, lang: string = 'en'): string {
  if (!dateString) return '';

  try {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };

    const locales: Record<string, string> = {
      en: 'en-US',
      zh: 'zh-CN',
      fr: 'fr-FR',
    };

    return date.toLocaleDateString(locales[lang] || 'en-US', options);
  } catch {
    return dateString;
  }
}

// Get icon name based on category
export function getCategoryIcon(category?: string): string {
  const icons: Record<string, string> = {
    development: 'Code',
    'ai-ml': 'Sparkles',
    tutorial: 'BookOpen',
    guide: 'Compass',
    default: 'FileText',
  };

  return icons[category || 'default'] || icons.default;
}
