import { getServerSession } from "next-auth";
import { authOptions } from "../api/auth/[...nextauth]/options";
import { redirect } from "next/navigation";
import Endpoints from "@/constants/endpoints";
import Header from "@/components/Header";

interface HomePageLayoutProps {
  children: React.ReactNode;
}

export default async function HomePageLayout({
  children,
}: HomePageLayoutProps) {
  const session = await getServerSession(authOptions);

  if (!session?.user) {
    redirect(Endpoints.SIGNIN);
  }
  return (
    <div>
      <Header />
      {children}
    </div>)
}
