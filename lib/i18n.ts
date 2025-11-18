import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'zh'],
  parser: 'dir', // 使用目录结构解析语言 (en/, fr/, zh/)
  localePrefix: 'as-needed', // 只在需要时添加语言前缀
});
