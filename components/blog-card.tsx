import Link from 'next/link';
import * as Icons from 'lucide-react';
import { type BlogPost, getCategoryColor, getCategoryIcon, formatDate } from '@/lib/blog-utils.client';
import { translateCategory, translateDifficulty } from '@/lib/blog-i18n';

interface BlogCardProps {
  post: BlogPost;
  viewMode?: 'grid' | 'list';
  lang: string;
}

export function BlogCard({ post, viewMode = 'grid', lang }: BlogCardProps) {
  const iconName = getCategoryIcon(post.category);
  const IconComponent = Icons[iconName as keyof typeof Icons] as React.ComponentType<{ className?: string }>;
  const colorClass = getCategoryColor(post.category);
  const displayDate = formatDate(post.date, post.lang);
  const categoryName = translateCategory(post.category, lang);
  const difficultyName = translateDifficulty(post.difficulty, lang);

  // Check if there's a custom illustration
  const hasCustomIllustration = post.image && (post.image.startsWith('/illustrations/') || post.image.startsWith('/images/') || post.image.startsWith('/assets/'));

  // Normalize image URL to bypass i18n middleware
  // Remove language prefix if present (e.g., /en/images/ -> /images/)
  const normalizedImageUrl = post.image
    ? post.image.replace(/^\/[^/]+\/images\//, '/images/')
        .replace(/^\/[^/]+\/illustrations\//, '/illustrations/')
        .replace(/^\/[^/]+\/assets\//, '/assets/')
    : undefined;

  if (viewMode === 'list') {
    return (
      <Link
        href={post.url}
        className="group block rounded-2xl overflow-hidden bg-white border border-gray-200 hover:shadow-lg transition-all duration-300"
      >
        <div className="flex items-center gap-6 p-6">
          {/* Custom Illustration or Icon */}
          <div className="flex-shrink-0 w-32 h-32 rounded-xl overflow-hidden">
            {hasCustomIllustration ? (
              <img
                src={normalizedImageUrl}
                alt={post.title}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className={`w-full h-full ${colorClass} flex items-center justify-center`}>
                {IconComponent && <IconComponent className="w-16 h-16 text-white/90" />}
              </div>
            )}
          </div>

          <div className="flex-1 min-w-0">
            <time className="text-sm text-gray-500 block mb-2">
              {displayDate}
            </time>
            <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-gray-700 transition-colors line-clamp-2">
              {post.title}
            </h3>
            <p className="text-sm text-gray-600 mb-3 line-clamp-2">
              {post.description}
            </p>
            <div className="flex items-center gap-2 flex-wrap">
              {post.category && (
                <span className="inline-flex items-center gap-1.5 text-xs text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
                  {categoryName}
                </span>
              )}
              {post.difficulty && (
                <span className="inline-flex items-center gap-1.5 text-xs text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
                  {difficultyName}
                </span>
              )}
            </div>
          </div>
        </div>
      </Link>
    );
  }

  return (
    <Link
      href={post.url}
      className="group block rounded-2xl overflow-hidden bg-white border border-gray-200 hover:shadow-lg transition-all duration-300"
    >
      {/* Icon Section - Custom Illustration or Gradient Background */}
      <div className="relative h-48 overflow-hidden">
        {hasCustomIllustration ? (
          <img
            src={normalizedImageUrl}
            alt={post.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className={`w-full h-full ${colorClass} flex items-center justify-center`}>
            {IconComponent && <IconComponent className="w-24 h-24 text-white/90" />}
          </div>
        )}
      </div>

      {/* Content Section */}
      <div className="p-6">
        <time className="text-sm text-gray-500 block mb-2">
          {displayDate}
        </time>

        <h3 className="text-lg font-semibold text-gray-900 mb-3 group-hover:text-gray-700 transition-colors line-clamp-2">
          {post.title}
        </h3>

        <div className="flex items-center gap-2 flex-wrap">
          {post.category && (
            <span className="inline-flex items-center gap-1.5 text-xs text-gray-600 bg-gray-100 px-3 py-1 rounded-full">
              {categoryName}
            </span>
          )}
          {post.difficulty && (
            <span className="inline-flex items-center gap-1.5 text-xs text-blue-600 bg-blue-50 px-3 py-1 rounded-full">
              {difficultyName}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}
