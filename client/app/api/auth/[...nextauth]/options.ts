import { DefaultSession, NextAuthOptions, Session, User } from "next-auth";
import { JWT } from "next-auth/jwt";
import CredentialsProvider from "next-auth/providers/credentials";

interface MyUser {
  email: string;
  username: string;
}
declare module "next-auth" {
  interface User {
    user: MyUser;
    jwt: string;
  }
  interface Session extends DefaultSession {
    user: MyUser;
    accessToken: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    user: MyUser;
    accessToken: string;
  }
}

export const authOptions: NextAuthOptions = {
  callbacks: {
    async jwt({
      token,
      user,
    }: {
      token: JWT;
      trigger?: "signIn" | "update" | "signUp";
      user: User;
      session?: Session;
    }) {
      if (user) {
        const jwt = user.jwt;
        const [, payload] = jwt.split(".");

        const decodedPayload = JSON.parse(atob(payload));
        token.accessToken = user.jwt;
        token.user = {
          email: decodedPayload.email,
          username: decodedPayload.username,
        };
      }
      return token;
    },
    async session({ session, token }: { session: Session; token: JWT }) {
      session.accessToken = token.accessToken;
      session.user = token.user;
      return session;
    },
  },
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {},
      async authorize(data: any) {
        const { email, password } = data;
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_AUTH_ROUTE}/Prod/login`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: email,
              password: password,
            }),
          }
        );
        const user = await res.json();

        if (res.ok && user) {
          return user;
        }
        return null;
      },
    }),
  ],
  pages: {
    error: "/sign-in",
    signIn: "/sign-in",
  },
};
