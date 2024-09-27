"use client";

import { useSession } from "next-auth/react";
import { useState } from "react";
import { Button } from "../ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import Image from "next/image";
import { useRouter } from "next/navigation";
import Link from "next/link";
import Endpoints from "@/constants/endpoints";

export default function Header() {
  const router = useRouter();
  const { data: session } = useSession();

  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = () => {
    router.push(`/search/${searchTerm}`);
    setSearchTerm("");
  }

  return (
    <div className="flex w-full mx-auto mt-3 justify-between items-center p-5 rounded-lg shadow-md">
      <Link className="flex flex-row items-center gap-3" href={Endpoints.HOME}>
        <Image
          src="/icons/logo.svg"
          alt="App Logo"
          width={40}
          height={40}
        />
        <div className="text-2xl font-bold">Moments App</div>
      </Link>
      <div className="flex gap-3 w-full max-w-md mx-auto">
        <input
          type="text"
          placeholder="Search..."
          className="p-2 border rounded-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button onClick={handleSearch}>Search</Button>
      </div>
      {session?.user ? (
        <>
          <Popover>
            <PopoverTrigger>
              <Avatar>
                <AvatarImage
                  src="https://github.com/shadcn.png"
                  alt="@shadcn"
                />
                <AvatarFallback>CN</AvatarFallback>
              </Avatar>
            </PopoverTrigger>
            <PopoverContent className="w-[170px] p-2 rounded-lg">
              <div className="flex flex-col gap-2">
                <Link
                  className="w-full cursor-pointer p-2 rounded-md hover:bg-slate-100 transition-colors"
                  href={Endpoints.SIGNOUT}
                >
                  Sign out
                </Link>
              </div>
            </PopoverContent>
          </Popover>
        </>
      ) : (
        <div className="flex gap-4">
          <Button variant={"secondary"}>Login</Button>
          <Button>Register</Button>
        </div>
      )}
    </div>
  );
}
