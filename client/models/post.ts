export interface Post {
  description: string;
  creator: string;
  id: string;
  title: string;
  image_id: string;
  signed_url: string;
}

export interface PostResult {
  posts: Post[];
}

export interface SinglePostDetails {
  post: Post;
}