import {
  defineConfig,
  defineDocs,
  frontmatterSchema,
  metaSchema,
} from 'fumadocs-mdx/config';
import { z } from 'zod';

// Extend frontmatter schema with custom fields
const customFrontmatterSchema = frontmatterSchema.extend({
  category: z.string().optional(),
  difficulty: z.string().optional(),
  tags: z.array(z.string()).optional(),
  published_date: z.string().optional(),
  date: z.string().optional(),
  author: z.string().optional(),
  image: z.string().optional(),
  lang: z.string().optional(),
  source_url: z.string().optional(),
});

// You can customise Zod schemas for frontmatter and `meta.json` here
// see https://fumadocs.dev/docs/mdx/collections
export const docs = defineDocs({
  dir: 'content/docs',
  docs: {
    schema: customFrontmatterSchema,
    postprocess: {
      includeProcessedMarkdown: true,
    },
  },
  meta: {
    schema: metaSchema,
  },
});

export default defineConfig({
  mdxOptions: {
    // MDX options
  },
});
