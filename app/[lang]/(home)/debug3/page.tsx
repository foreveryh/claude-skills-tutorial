import { source } from '@/lib/source';

export default async function Debug3Page({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;

  // Get all pages
  const allPages = source.pageTree;

  // Get pages for specific language
  const pages = source.getPages(lang);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Language Debug: {lang}</h1>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Page Tree Structure</h2>
        <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto max-h-96">
          {JSON.stringify(allPages, null, 2)}
        </pre>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Pages for lang="{lang}": {pages.length}</h2>
        <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto max-h-96">
          {JSON.stringify(pages.map(p => ({
            url: p.url,
            slugs: p.slugs,
            locale: p.locale,
          })), null, 2)}
        </pre>
      </div>
    </div>
  );
}
