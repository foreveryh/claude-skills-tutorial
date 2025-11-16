import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // 使用目录结构解析语言 (en/, fr/, ko/, zh/)
});
