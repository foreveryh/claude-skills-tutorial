'use client';

import { useState, useMemo } from 'react';
import { Search, Grid3x3, List } from 'lucide-react';
import { BlogCard } from './blog-card';
import { BlogFilterSidebar } from './blog-filter-sidebar';
import { ProjectShowcase } from './project-showcase';
import { type BlogPost } from '@/lib/blog-utils.client';
import { getBlogTranslations } from '@/lib/blog-i18n';

interface BlogListProps {
  posts: BlogPost[];
  categories: string[];
  difficulties: string[];
  tags: string[];
  lang: string;
}

export function BlogList({ posts, categories, difficulties, tags, lang }: BlogListProps) {
  const t = getBlogTranslations(lang);
  const allPosts = posts;
  const availableCategories = categories;
  const availableDifficulties = difficulties;
  const availableTags = tags;

  const [searchQuery, setSearchQuery] = useState('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState('newest');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedDifficulties, setSelectedDifficulties] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  const filteredAndSortedPosts = useMemo(() => {
    let filtered = allPosts;

    // Apply search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (post) =>
          post.title.toLowerCase().includes(query) ||
          post.description.toLowerCase().includes(query) ||
          post.tags.some((tag) => tag.toLowerCase().includes(query)) ||
          post.author?.toLowerCase().includes(query)
      );
    }

    // Apply category filter
    if (selectedCategories.length > 0) {
      filtered = filtered.filter((post) =>
        post.category && selectedCategories.includes(post.category)
      );
    }

    // Apply difficulty filter
    if (selectedDifficulties.length > 0) {
      filtered = filtered.filter((post) =>
        post.difficulty && selectedDifficulties.includes(post.difficulty)
      );
    }

    // Apply tags filter
    if (selectedTags.length > 0) {
      filtered = filtered.filter((post) =>
        post.tags.some((tag) => selectedTags.includes(tag))
      );
    }

    // Apply sorting
    const sorted = [...filtered];
    switch (sortBy) {
      case 'newest':
        sorted.sort(
          (a, b) => new Date(b.date || 0).getTime() - new Date(a.date || 0).getTime()
        );
        break;
      case 'oldest':
        sorted.sort(
          (a, b) => new Date(a.date || 0).getTime() - new Date(b.date || 0).getTime()
        );
        break;
      case 'a-z':
        sorted.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'z-a':
        sorted.sort((a, b) => b.title.localeCompare(a.title));
        break;
    }

    return sorted;
  }, [allPosts, searchQuery, selectedCategories, selectedDifficulties, selectedTags, sortBy]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{t.blog}</h1>
          <p className="text-lg text-gray-600">
            {t.blogDescription}
          </p>
        </div>

        {/* Project Showcase */}
        <ProjectShowcase lang={lang} />

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-64 flex-shrink-0">
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <BlogFilterSidebar
                categories={availableCategories}
                difficulties={availableDifficulties}
                tags={availableTags}
                selectedCategories={selectedCategories}
                selectedDifficulties={selectedDifficulties}
                selectedTags={selectedTags}
                onCategoryChange={setSelectedCategories}
                onDifficultyChange={setSelectedDifficulties}
                onTagChange={setSelectedTags}
                onSortChange={setSortBy}
                lang={lang}
              />
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1">
            {/* Search and View Controls */}
            <div className="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <div className="relative flex-1 max-w-md">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  placeholder={t.search}
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded ${
                    viewMode === 'grid'
                      ? 'bg-gray-100 text-gray-900'
                      : 'text-gray-500 hover:text-gray-900'
                  }`}
                  aria-label={t.gridView}
                >
                  <Grid3x3 className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded ${
                    viewMode === 'list'
                      ? 'bg-gray-100 text-gray-900'
                      : 'text-gray-500 hover:text-gray-900'
                  }`}
                  aria-label={t.listView}
                >
                  <List className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Results Count */}
            <p className="text-sm text-gray-600 mb-4">
              {filteredAndSortedPosts.length} {t.posts}
            </p>

            {/* Blog Posts Grid/List */}
            {filteredAndSortedPosts.length > 0 ? (
              <div
                className={
                  viewMode === 'grid'
                    ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
                    : 'space-y-4'
                }
              >
                {filteredAndSortedPosts.map((post) => (
                  <BlogCard key={post.id} post={post} viewMode={viewMode} lang={lang} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No posts found matching your criteria.</p>
                <button
                  onClick={() => {
                    setSearchQuery('');
                    setSelectedCategories([]);
                    setSelectedDifficulties([]);
                    setSelectedTags([]);
                  }}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
                >
                  Clear all filters
                </button>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
