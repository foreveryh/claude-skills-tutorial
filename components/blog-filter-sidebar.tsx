'use client';

import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import { getBlogTranslations, translateCategory, translateDifficulty } from '@/lib/blog-i18n';

interface BlogFilterSidebarProps {
  categories: string[];
  difficulties: string[];
  tags: string[];
  selectedCategories: string[];
  selectedDifficulties: string[];
  selectedTags: string[];
  onCategoryChange: (categories: string[]) => void;
  onDifficultyChange: (difficulties: string[]) => void;
  onTagChange: (tags: string[]) => void;
  onSortChange: (sort: string) => void;
  lang: string;
}

export function BlogFilterSidebar({
  categories,
  difficulties,
  tags,
  selectedCategories,
  selectedDifficulties,
  selectedTags,
  onCategoryChange,
  onDifficultyChange,
  onTagChange,
  onSortChange,
  lang,
}: BlogFilterSidebarProps) {
  const t = getBlogTranslations(lang);

  const [expandedSections, setExpandedSections] = useState({
    sort: true,
    category: true,
    difficulty: true,
    tags: false,
  });

  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const handleCheckboxChange = (
    value: string,
    selectedValues: string[],
    onChange: (values: string[]) => void
  ) => {
    if (selectedValues.includes(value)) {
      onChange(selectedValues.filter((v) => v !== value));
    } else {
      onChange([...selectedValues, value]);
    }
  };

  return (
    <div className="w-full space-y-1">
      <h2 className="text-lg font-semibold mb-4">{t.filterAndSort}</h2>

      {/* Sort By */}
      <div className="border-b border-gray-200 pb-4">
        <button
          onClick={() => toggleSection('sort')}
          className="flex items-center justify-between w-full text-left py-2 text-sm font-medium"
        >
          {t.sortBy}
          <ChevronDown
            className={`w-4 h-4 transition-transform ${expandedSections.sort ? 'rotate-180' : ''}`}
          />
        </button>
        {expandedSections.sort && (
          <div className="mt-2 space-y-2">
            <label className="flex items-center text-sm cursor-pointer">
              <input
                type="radio"
                name="sort"
                value="newest"
                defaultChecked
                onChange={(e) => onSortChange(e.target.value)}
                className="mr-2"
              />
              {t.newest}
            </label>
            <label className="flex items-center text-sm cursor-pointer">
              <input
                type="radio"
                name="sort"
                value="oldest"
                onChange={(e) => onSortChange(e.target.value)}
                className="mr-2"
              />
              {t.oldest}
            </label>
            <label className="flex items-center text-sm cursor-pointer">
              <input
                type="radio"
                name="sort"
                value="a-z"
                onChange={(e) => onSortChange(e.target.value)}
                className="mr-2"
              />
              {t.aToZ}
            </label>
            <label className="flex items-center text-sm cursor-pointer">
              <input
                type="radio"
                name="sort"
                value="z-a"
                onChange={(e) => onSortChange(e.target.value)}
                className="mr-2"
              />
              {t.zToA}
            </label>
          </div>
        )}
      </div>

      {/* Category */}
      <div className="border-b border-gray-200 pb-4">
        <button
          onClick={() => toggleSection('category')}
          className="flex items-center justify-between w-full text-left py-2 text-sm font-medium"
        >
          {t.category}
          <ChevronDown
            className={`w-4 h-4 transition-transform ${expandedSections.category ? 'rotate-180' : ''}`}
          />
        </button>
        {expandedSections.category && (
          <div className="mt-2 space-y-2">
            {categories.map((category) => (
              <label key={category} className="flex items-center text-sm cursor-pointer">
                <input
                  type="checkbox"
                  checked={selectedCategories.includes(category)}
                  onChange={() =>
                    handleCheckboxChange(category, selectedCategories, onCategoryChange)
                  }
                  className="mr-2"
                />
                {translateCategory(category, lang)}
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Difficulty */}
      <div className="border-b border-gray-200 pb-4">
        <button
          onClick={() => toggleSection('difficulty')}
          className="flex items-center justify-between w-full text-left py-2 text-sm font-medium"
        >
          {t.difficulty}
          <ChevronDown
            className={`w-4 h-4 transition-transform ${expandedSections.difficulty ? 'rotate-180' : ''}`}
          />
        </button>
        {expandedSections.difficulty && (
          <div className="mt-2 space-y-2">
            {difficulties.length > 0 ? (
              difficulties.map((difficulty) => (
                <label key={difficulty} className="flex items-center text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedDifficulties.includes(difficulty)}
                    onChange={() =>
                      handleCheckboxChange(difficulty, selectedDifficulties, onDifficultyChange)
                    }
                    className="mr-2"
                  />
                  {translateDifficulty(difficulty, lang)}
                </label>
              ))
            ) : (
              <p className="text-sm text-gray-500">No difficulties available</p>
            )}
          </div>
        )}
      </div>

      {/* Tags */}
      <div className="pb-4">
        <button
          onClick={() => toggleSection('tags')}
          className="flex items-center justify-between w-full text-left py-2 text-sm font-medium"
        >
          {t.tags}
          <ChevronDown
            className={`w-4 h-4 transition-transform ${expandedSections.tags ? 'rotate-180' : ''}`}
          />
        </button>
        {expandedSections.tags && (
          <div className="mt-2 space-y-2 max-h-64 overflow-y-auto">
            {tags.length > 0 ? (
              tags.map((tag) => (
                <label key={tag} className="flex items-center text-sm cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedTags.includes(tag)}
                    onChange={() =>
                      handleCheckboxChange(tag, selectedTags, onTagChange)
                    }
                    className="mr-2"
                  />
                  {tag}
                </label>
              ))
            ) : (
              <p className="text-sm text-gray-500">No tags available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
