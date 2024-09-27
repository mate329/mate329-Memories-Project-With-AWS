'use client'

import React from "react";
import { Card, CardFooter, Image, Button } from "@nextui-org/react";
import { Post } from "@/models/post";
import Link from "next/link";

interface PostCardProps {
  post: Post;
}

export default function PostCard( { post }: PostCardProps ) {
  return (
    <div>
      <Card
        className="border-none rounded-xl max-w-96 max-h-96"
      >
        <Image
          alt={post.title}
          className="object-cover w-full h-full"
          src={post.signed_url}
        />
        <CardFooter className="backdrop-blur rounded-xl justify-between before:bg-white/10 border-white/20 border-1 overflow-hidden py-1 absolute bottom-1 w-[calc(100%_-_8px)] shadow-small ml-1 z-10">
          <Link href={`/user/${post.creator}`} className="text-center text-wrap text-white/80">@{post.creator}</Link>
          <Link href={`/post/${post.id}`}>
            <Button className="text-tiny text-white bg-black/20" variant="flat" color="default" size="sm">
              Details
            </Button>
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
}
