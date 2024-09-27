"use client"

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import Endpoints from "@/constants/endpoints";
import Link from "next/link";
import { Loader2 } from 'lucide-react';
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";
import { signIn } from "next-auth/react";
import { processAuthRequest } from "@/services/authService";
import { useState } from "react";

interface AuthFormProps {
  type: "sign-in" | "sign-up";
}

const AuthForm = ({ type }: AuthFormProps) => {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    event.preventDefault();
    const endpoint = type === "sign-in" ? "login" : "register";
    const data = new FormData(event.currentTarget);

    if (type === "sign-in") {
      const res = await signIn("credentials", {
        email: data.get("email") as string,
        password: data.get("password") as string,
        redirect: false,
      });
  
      if (res?.ok) {
        router.push(Endpoints.HOME);
      } else {
        toast.error(
          "An error occurred. Please check your email and password and try again."
        );
        setIsLoading(false);
      }
    } else {
      processAuthRequest({
        email: data.get("email"),
        password: data.get("password"),
        last_name: data.get("last_name"),
        first_name: data.get("first_name"),
      }, endpoint);
    }
    setIsLoading(false);
  };

  const renderFormFields = () => (
    <>
      <Label htmlFor="email">Email Address</Label>
      <Input required id="email" name="email" autoComplete="email" />

      <Label htmlFor="password">Password</Label>
      <Input
        required
        name="password"
        type="password"
        id="password"
        autoComplete={type === "sign-in" ? "current-password" : "new-password"}
      />

      {type === "sign-up" && (
        <>
          <Label htmlFor="first_name">First Name</Label>
          <Input required name="first_name" id="first_name" />

          <Label htmlFor="last_name">Last Name</Label>
          <Input required name="last_name" id="last_name" />
        </>
      )}
    </>
  );

  return (
    <div className="flex flex-col items-center gap-5">
      <h1>{type === "sign-in" ? "Sign In" : "Sign Up"}</h1>
      <form noValidate className="flex flex-col gap-3" onSubmit={handleSubmit}>
        {renderFormFields()}
        <Button type="submit" disabled={isLoading}>
          {isLoading ? (
            <>
              <Loader2 size={20} className="animate-spin" /> &nbsp;
              Loading...
            </>
          ) : type === 'sign-in' 
            ? 'Sign In' : 'Sign Up'}
        </Button>
        <footer className="flex justify-center gap-1">
          <p>{type === "sign-in" ? "Don't have an account?" : "Already have an account?"}</p>
          <Link href={type === "sign-in" ? "/sign-up" : "/sign-in"}>
            <p className="text-blue-500">{type === "sign-in" ? "Sign up!" : "Sign in!"}</p>
          </Link>
        </footer>
      </form>
    </div>
  );
};

export default AuthForm;
