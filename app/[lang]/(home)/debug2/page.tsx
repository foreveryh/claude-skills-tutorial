import { source } from '@/lib/source';

export default async function Debug2Page({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  const pages = source.getPages(lang);

  // Get first page with actual data
  const samplePage = pages.find(p => p.slugs.includes('agent-skills-sdk'));

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Raw Page Object Debug</h1>

      {samplePage && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Sample Page: {samplePage.data.title}</h2>

          <div className="mb-4">
            <h3 className="font-bold">Page URL:</h3>
            <pre className="bg-gray-100 p-2">{samplePage.url}</pre>
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Page Slugs:</h3>
            <pre className="bg-gray-100 p-2">{JSON.stringify(samplePage.slugs, null, 2)}</pre>
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Page Data Type:</h3>
            <pre className="bg-gray-100 p-2">{typeof samplePage.data}</pre>
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Page Data Keys:</h3>
            <pre className="bg-gray-100 p-2">{JSON.stringify(Object.keys(samplePage.data), null, 2)}</pre>
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Full Page Data:</h3>
            <pre className="bg-gray-100 p-2 text-xs overflow-auto max-h-96">
              {JSON.stringify(samplePage.data, null, 2)}
            </pre>
          </div>

          <div className="mb-4">
            <h3 className="font-bold">Full Page Object (all keys):</h3>
            <pre className="bg-gray-100 p-2">{JSON.stringify(Object.keys(samplePage), null, 2)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}
