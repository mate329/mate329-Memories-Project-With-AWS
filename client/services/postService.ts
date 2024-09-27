import { PostResult, SinglePostDetails } from "@/models/post";

export async function getAllPosts(): Promise<PostResult> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/getAllPosts`,
    { next: { revalidate: 300 } } // https://nextjs.org/docs/app/building-your-application/data-fetching/fetching-caching-and-revalidating#fetching-data-on-the-server-with-fetch
  );

  if (!res.ok) {
    throw new Error("Failed to fetch posts");
  }
  const data: PostResult = await res.json();

  return data;
}

export async function createPost(post: object): Promise<void> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/createPost`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(post),
    }
  );

  if (!res.ok) {
    throw new Error("Failed to create post");
  }
}

export async function getPostDetails(id: string): Promise<SinglePostDetails> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/getPost?postId=${id}`,
    { next: { revalidate: 1 } }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch post details");
  }
  const data: SinglePostDetails = await res.json();

  return data;
}

export async function searchPosts(inquiry: string): Promise<PostResult> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/searchPosts?inquiry=${inquiry}`,
    { next: { revalidate: 10 } }
  );

  if (!res.ok) {
    throw new Error("Failed to search posts");
  }
  const data: PostResult = await res.json();

  return data;
}

export async function getPostsByUser(username: string): Promise<PostResult> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/getPostsByUser?creatorName=${username}`,
    { next: { revalidate: 10 } }
  );

  if (!res.ok) {
    throw new Error(`Failed to get posts by user ${username}`);
  }
  const data: PostResult = await res.json();

  return data;
}

export async function deletePost(post_id: string): Promise<void> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/deletePost`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "post_id": post_id,
      }),
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to delete post ${post_id}`);
  }
}

export async function updatePost(updated_post: object): Promise<void> {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_POST_ROUTE}/Prod/updatePost`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updated_post),
    }
  );

  if (!res.ok) {
    throw new Error(`Failed to delete post ${updated_post}`);
  }
}
