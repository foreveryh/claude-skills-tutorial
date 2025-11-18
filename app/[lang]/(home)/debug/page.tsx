import { getBlogPosts, getCategories, getDifficulties, getTags } from '@/lib/blog-utils';

export default async function DebugPage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  const posts = getBlogPosts(lang);
  const categories = getCategories(posts);
  const difficulties = getDifficulties(posts);
  const tags = getTags(posts);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Debug Info for {lang}</h1>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Posts Count: {posts.length}</h2>
        <div className="space-y-4">
          {posts.slice(0, 3).map((post) => (
            <div key={post.id} className="border p-4 rounded">
              <h3 className="font-bold">{post.title}</h3>
              <p className="text-sm text-gray-600">URL: {post.url}</p>
              <p className="text-sm">Category: {post.category || 'none'}</p>
              <p className="text-sm">Difficulty: {post.difficulty || 'none'}</p>
              <p className="text-sm">Tags: {post.tags.join(', ') || 'none'}</p>
              <p className="text-sm">Date: {post.date || 'none'}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Available Categories ({categories.length})</h2>
        <pre className="bg-gray-100 p-4 rounded">{JSON.stringify(categories, null, 2)}</pre>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Available Difficulties ({difficulties.length})</h2>
        <pre className="bg-gray-100 p-4 rounded">{JSON.stringify(difficulties, null, 2)}</pre>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Available Tags ({tags.length})</h2>
        <pre className="bg-gray-100 p-4 rounded">{JSON.stringify(tags, null, 2)}</pre>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">All Posts Data</h2>
        <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto max-h-96">
          {JSON.stringify(posts, null, 2)}
        </pre>
      </div>
    </div>
  );
}
