import { BlogList } from '@/components/blog-list';
import { getBlogPosts, getCategories, getDifficulties, getTags } from '@/lib/blog-utils';

export default async function HomePage({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;

  // Fetch all data on the server
  const posts = getBlogPosts(lang);
  const categories = getCategories(posts);
  const difficulties = getDifficulties(posts);
  const tags = getTags(posts);

  return (
    <BlogList
      posts={posts}
      categories={categories}
      difficulties={difficulties}
      tags={tags}
      lang={lang}
    />
  );
}
