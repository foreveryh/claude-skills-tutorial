import { source } from '@/lib/source';
import { createFromSource } from 'fumadocs-core/search/server';
import { createTokenizer } from '@orama/tokenizers/mandarin';

export const { GET } = createFromSource(source, {
  // https://docs.orama.com/docs/orama-js/supported-languages
  // Configure language-specific search options
  localeMap: {
    // Chinese requires special tokenizer
    zh: {
      components: {
        tokenizer: createTokenizer(),
      },
      search: {
        threshold: 0,
        tolerance: 0,
      },
    },
    // French uses built-in language support
    fr: { language: 'french' },
    // English uses built-in language support
    en: { language: 'english' },
  },
});
