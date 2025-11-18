// Server-side utilities that require Node.js APIs
import { source } from '@/lib/source';

export type { BlogPost } from './blog-utils.client';
export { getCategoryColor, formatDate, getCategoryIcon } from './blog-utils.client';

import type { BlogPost } from './blog-utils.client';

// Get all blog posts for a specific language
export function getBlogPosts(lang: string): BlogPost[] {
  const pages = source.getPages(lang);

  const posts: BlogPost[] = pages
    .filter((page) => {
      // Filter out index pages and include regular content pages
      // Index pages typically have empty slugs or are named 'index'
      return page.slugs.length > 0 && !page.slugs.includes('index');
    })
    .map((page) => {
      const data = page.data as any;

      // Try multiple ways to access frontmatter
      const exports = data._exports || data.exports || {};

      // Frontmatter fields might be直接在 data 上，或在 exports 中
      const getFrontmatter = (key: string) => {
        return data[key] || exports[key] || undefined;
      };

      return {
        id: page.url,
        title: data.title || 'Untitled',
        description: data.description || '',
        date: getFrontmatter('published_date') || getFrontmatter('date') || '',
        category: getFrontmatter('category'),
        difficulty: getFrontmatter('difficulty'),
        tags: getFrontmatter('tags') || [],
        slug: page.slugs.join('/'),
        url: page.url,
        lang,
        author: getFrontmatter('author'),
        image: getFrontmatter('image'),
      };
    })
    .sort((a, b) => {
      // Sort by date, newest first
      if (!a.date) return 1;
      if (!b.date) return -1;
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    });

  return posts;
}

// Extract unique categories from all posts
export function getCategories(posts: BlogPost[]): string[] {
  const categories = new Set<string>();
  posts.forEach((post) => {
    if (post.category) {
      categories.add(post.category);
    }
  });
  return Array.from(categories).sort();
}

// Extract unique difficulty levels from all posts
export function getDifficulties(posts: BlogPost[]): string[] {
  const difficulties = new Set<string>();
  posts.forEach((post) => {
    if (post.difficulty) {
      difficulties.add(post.difficulty);
    }
  });
  return Array.from(difficulties).sort();
}

// Extract unique tags from all posts
export function getTags(posts: BlogPost[]): string[] {
  const tags = new Set<string>();
  posts.forEach((post) => {
    post.tags.forEach((tag) => tags.add(tag));
  });
  return Array.from(tags).sort();
}

