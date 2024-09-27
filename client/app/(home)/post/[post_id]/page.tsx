'use client';

import React, { useEffect, useState } from 'react';
import { Card } from "@nextui-org/react";
import { Skeleton } from "@/components/ui/skeleton";
import Image from 'next/image';
import { deletePost, getPostDetails, updatePost } from '@/services/postService';
import { SinglePostDetails } from '@/models/post';
import { useSession } from 'next-auth/react';
import { Button } from '@/components/ui/button';
import { toast } from 'react-toastify';
import { useRouter } from 'next/navigation';
import Endpoints from '@/constants/endpoints';
import { Loader2 } from 'lucide-react';
import { Dialog, DialogTrigger, DialogContent, DialogTitle, DialogDescription } from "@/components/ui/dialog"

export default function ShowPost({
    params: { post_id }
}: {
    params: { post_id: string }
}) {
    const router = useRouter();
    const { data: session } = useSession();
    const [isLoading, setIsLoading] = useState(true);
    const [postDetails, setPostDetails] = useState<SinglePostDetails | null>(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [isLoadingDelete, setIsLoadingDelete] = useState(false);
    const [isLoadingUpdate, setIsLoadingUpdate] = useState(false);

    const postExists = Boolean(postDetails?.post?.title);

    useEffect(() => {
        async function fetchData() {
            try {
                const results = await getPostDetails(post_id);
                setPostDetails(results);
                setTitle(results?.post?.title || '');
                setDescription(results?.post?.description || '');
            } catch (error) {
                console.error("Failed to fetch post details", error);
            } finally {
                setIsLoading(false);
            }
        }

        fetchData();
    }, [post_id]);

    const handleDeletePost = async () => {
        setIsLoadingDelete(true);
        try {
            await deletePost(post_id);
            toast.success("Post successfully deleted!", {
                position: 'bottom-right'
            });
            router.push(Endpoints.HOME);
        } catch (error) {
            toast.error("Failed to delete post", {
                position: 'bottom-right'
            });
        }
        setIsLoadingDelete(false);
    };

    const handleUpdatePost = () => {
        setIsDialogOpen(true);
    };

    const handleSaveChanges = async () => {
        setIsLoadingUpdate(true);
        try {
            await updatePost({ post_id, title, description });
            toast.success("Post successfully updated!", {
                position: 'bottom-right'
            });
            setIsDialogOpen(false);

            const updatedDetails = await getPostDetails(post_id);
            setPostDetails(updatedDetails);
        } catch (error) {
            toast.error("Failed to update post", {
                position: 'bottom-right'
            });
        }
        setIsLoadingUpdate(false);
    };

    return (
        <div className="flex justify-center my-10">
            <Card className='flex flex-col md:flex-row md:w-11/12 mx-auto justify-between items-center bg-white shadow-lg rounded-lg p-5'>
                {isLoading ? (
                    <div className="flex flex-col md:flex-row w-full">
                        <div className='md:w-1/2 w-full'>
                            <Skeleton className="h-[300px] w-[300px] rounded-xl mx-auto" />
                        </div>
                        <div className='md:w-1/2 w-full flex flex-col items-center justify-center p-5 space-y-2'>
                            <Skeleton className="h-4 w-[250px]" />
                            <Skeleton className="h-4 w-[250px]" />
                            <Skeleton className="h-4 w-[250px]" />
                        </div>
                    </div>
                ) : (
                    postExists ? (
                        <div className="flex flex-col md:flex-row w-full">
                            <div className='md:w-1/2 w-full'>
                                <Image
                                    src={postDetails?.post?.signed_url || 'Image not available'}
                                    alt='Post Image'
                                    width={300}
                                    height={300}
                                    className='w-full h-auto max-w-md mx-auto border-none rounded-lg'
                                />
                            </div>
                            <div className='md:w-1/2 w-full flex flex-col items-center justify-center p-5 space-y-2'>
                                <h3 className='text-xl font-bold text-gray-800 mb-2'>@{postDetails?.post?.creator}</h3>
                                <h4 className='text-lg font-semibold text-gray-600 mb-4'>{postDetails?.post?.title}</h4>
                                <p className='text-gray-600 text-center mb-4'>{postDetails?.post?.description}</p>
                                { session?.user?.username === postDetails?.post?.creator && (
                                    <div className='flex flex-row gap-5'>
                                        <Button onClick={handleDeletePost}>
                                        {isLoadingDelete ? (
                                            <>
                                                <Loader2 size={20} className="animate-spin" /> &nbsp;
                                                Deleting...
                                            </>
                                            ): ('Delete Moment')
                                        }
                                        </Button>
                                        <Button onClick={handleUpdatePost}>
                                            Update Moment
                                        </Button>
                                    </div>
                                )}
                            </div>
                        </div>
                    ) : (
                        <p>Post cannot be found.</p>
                    )
                )}
            </Card>

            {/* Dialog for updating post */}
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                <DialogTrigger asChild>
                    <Button style={{ display: 'none' }}>Open Dialog</Button>
                </DialogTrigger>
                <DialogContent>
                    <DialogTitle>Edit Post</DialogTitle>
                    <DialogDescription>
                        Update the title and description of your post.
                    </DialogDescription>
                    <form onSubmit={(e) => { e.preventDefault(); handleSaveChanges(); }}>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
                                Title
                            </label>
                            <input
                                id="title"
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
                                Description
                            </label>
                            <textarea
                                id="description"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            />
                        </div>
                        <div className="flex items-center justify-between">
                            <Button type="button" onClick={() => setIsDialogOpen(false)}>
                                Cancel
                            </Button>
                            <Button type="submit" disabled={isLoadingUpdate}>
                            {isLoadingUpdate ? (
                                <>
                                    <Loader2 size={20} className="animate-spin" /> &nbsp;
                                    Updating...
                                </>
                                ): ('Update Moment!')
                            }
                            </Button>
                        </div>
                    </form>
                </DialogContent>
            </Dialog>
        </div>
    );
}
