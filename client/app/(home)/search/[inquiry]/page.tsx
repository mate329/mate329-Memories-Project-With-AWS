'use client';

import PostCard from "@/components/PostCard";
import { searchPosts } from "@/services/postService";
import { PostResult } from "@/models/post";
import { Skeleton } from "@/components/ui/skeleton";
import { useEffect, useState } from "react";
import { Post } from "@/models/post";

export default function SearchPage({
    params: { inquiry }
}: {
    params: { inquiry: string }
}) {
    const [isLoading, setIsLoading] = useState(true);
    const [searchResults, setSearchResults] = useState<PostResult | null>(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const results = await searchPosts(inquiry);
                setSearchResults(results);
            } catch (error) {
                console.error("Failed to search posts", error);
            } finally {
                setIsLoading(false);
            }
        }

        fetchData();
    }, [inquiry]);

    return (
        <div className="w-screen flex justify-center py-10">
            <div className="container mx-auto px-5">
                <h1 className="text-3xl font-bold text-gray-800 mb-6">Search Results</h1>
                <div className="grid gap-10 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                    {isLoading ? (
                        <>
                            <Skeleton className="h-[300px] w-full rounded-xl" />
                            <Skeleton className="h-[300px] w-full rounded-xl" />
                            <Skeleton className="h-[300px] w-full rounded-xl" />
                        </>
                    ) : (
                        searchResults?.posts.map((post: Post) => (
                            <div>
                                <PostCard key={post.id} post={post} />
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}
