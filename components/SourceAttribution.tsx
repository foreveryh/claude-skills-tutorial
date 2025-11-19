import React from 'react';
import { Globe, ExternalLink, Calendar, User } from 'lucide-react';

interface SourceInfo {
  url: string;
  name: string;
  author?: string;
  publishedDate?: string;
  accessedDate?: string;
  license?: string;
}

interface SourceAttributionProps {
  source: SourceInfo;
  languages: string[]; // ['en', 'zh', 'fr', 'ko']
  currentLang: string;
  className?: string;
}

/**
 * SourceAttribution Component
 *
 * Displays original article information at the top of imported articles.
 * Used by the fumadocs-article-importer skill to attribute content sources.
 *
 * @example
 * <SourceAttribution
 *   source={{
 *     url: "https://claude.com/blog/skills-explained",
 *     name: "Claude Blog",
 *     author: "Claude Team",
 *     publishedDate: "2025-11-13",
 *     accessedDate: "2025-11-16"
 *   }}
 *   languages={['en', 'zh', 'fr', 'ko']}
 *   currentLang="en"
 * />
 */
export function SourceAttribution({ source, languages, currentLang, className }: SourceAttributionProps) {
  // Add defensive checks for undefined props
  if (!source || !languages || !currentLang) {
    return null;
  }

  // Validate source object has required properties
  if (!source.url || !source.name) {
    return null;
  }

  const langNames: Record<string, string> = {
    en: 'English',
    zh: '简体中文',
    fr: 'Français',
    ko: '한국어'
  };

  const otherLangs = languages.filter(lang => lang !== currentLang);

  return (
    <div className={["mb-8 rounded-lg border border-border bg-muted/50 dark:bg-muted/30 p-4", className].join(' ')}>
      <div className="flex flex-col gap-3">
        {/* Header */}
        <div className="flex items-center gap-2">
          <Globe className="h-4 w-4 text-muted-foreground" />
          <h3 className="text-sm font-semibold text-foreground dark:text-muted-foreground">
            📚 Source Information
          </h3>
        </div>

        {/* Main source info */}
        <div className="grid gap-2 pl-6">
          <div className="flex items-center gap-2 text-sm">
            <ExternalLink className="h-3 w-3 text-muted-foreground" />
            <span className="text-muted-foreground">Original article:</span>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-primary hover:underline dark:text-blue-400"
            >
              {source.name}
            </a>
          </div>

          {source.author && (
            <div className="flex items-center gap-2 text-sm">
              <User className="h-3 w-3 text-muted-foreground" />
              <span className="text-muted-foreground">Author:</span>
              <span className="font-medium text-foreground">{source.author}</span>
            </div>
          )}

          {source.publishedDate && (
            <div className="flex items-center gap-2 text-sm">
              <Calendar className="h-3 w-3 text-muted-foreground" />
              <span className="text-muted-foreground">Published:</span>
              <span className="font-medium text-foreground">
                {new Date(source.publishedDate).toLocaleDateString('en-US')}
              </span>
            </div>
          )}
        </div>

        {/* Language selector */}
        {otherLangs.length > 0 && (
          <div className="mt-3 border-t border-border pt-3 pl-6">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs text-muted-foreground">🌐 Available in:</span>
              {languages.map(lang => {
                const isActive = lang === currentLang;

                return (
                  <span
                    key={lang}
                    className={`text-xs rounded-full px-2 py-1 ${
                      isActive
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted text-muted-foreground dark:bg-muted/50'
                    }`}
                  >
                    {langNames[lang]}
                  </span>
                );
              })}
            </div>
          </div>
        )}

        {/* Import notes */}
        <div className="mt-3 border-t border-border pt-3 pl-6">
          <p className="text-xs text-muted-foreground">
            ℹ️ This article was automatically imported and translated using Claude AI.
            {source.accessedDate && ` Imported on ${new Date(source.accessedDate).toLocaleDateString()}.`}
          </p>
        </div>
      </div>
    </div>
  );
}

export default SourceAttribution;
