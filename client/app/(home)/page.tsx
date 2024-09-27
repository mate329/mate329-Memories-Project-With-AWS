import PostCard from "@/components/PostCard";
import SideMenu from "@/components/SideMenu";
import { getAllPosts } from "@/services/postService";

export default async function HomePage() {
  const posts = await getAllPosts();
  return (
    <div className="w-screen flex justify-center">
      <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10 p-5">
        {posts.posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
      </div>
      <SideMenu />
    </div>
  );
}
