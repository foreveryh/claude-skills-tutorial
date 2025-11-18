'use client';

import { ExternalLink } from 'lucide-react';
import projectsData from '@/data/projects.json';

interface Project {
  name: string;
  description: string;
  url: string;
  tags?: string[];
}

interface ProjectShowcaseProps {
  lang: string;
}

const projects: Project[] = projectsData;

export function ProjectShowcase({ lang }: ProjectShowcaseProps) {
  const titles = {
    en: 'Featured Open Source Projects',
    zh: '精选开源项目',
    fr: 'Projets Open Source en Vedette',
  };

  const viewProject = {
    en: 'View on GitHub',
    zh: '在 GitHub 上查看',
    fr: 'Voir sur GitHub',
  };

  const title = titles[lang as keyof typeof titles] || titles.en;
  const viewText = viewProject[lang as keyof typeof viewProject] || viewProject.en;

  return (
    <div className="mb-8">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>

      {/* Horizontal Scrollable Container */}
      <div className="relative">
        <div className="overflow-x-auto pb-3 hide-scrollbar">
          <div className="flex gap-3 min-w-max">
            {projects.map((project) => (
              <a
                key={project.name}
                href={project.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex-shrink-0 w-56 bg-white rounded-lg border border-gray-200 hover:border-blue-400 hover:shadow-md transition-all duration-200"
              >
                {/* Compact Project Card */}
                <div className="p-4">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="text-sm font-semibold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                      {project.name}
                    </h4>
                    <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600 transition-colors flex-shrink-0 ml-2" />
                  </div>

                  {/* Description */}
                  <p className="text-xs text-gray-600 mb-3 line-clamp-2 leading-relaxed">
                    {project.description}
                  </p>

                  {/* Tags */}
                  {project.tags && project.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1.5">
                      {project.tags.slice(0, 3).map((tag) => (
                        <span
                          key={tag}
                          className="inline-flex items-center text-[10px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded-md font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </a>
            ))}
          </div>
        </div>

        {/* Gradient Overlay for scroll hint */}
        <div className="absolute right-0 top-0 bottom-3 w-12 bg-gradient-to-l from-gray-50 to-transparent pointer-events-none" />
      </div>

      <style jsx>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>
    </div>
  );
}
