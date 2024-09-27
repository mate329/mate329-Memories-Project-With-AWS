import "@/styles/globals.css";
import { Session } from "next-auth";
import Provider from "@/providers";

interface LayoutProps {
  children: React.ReactNode;
  params: {
    session: Session;
  };
}

export default function Layout({ children, params }: LayoutProps) {
  return (
    <html lang="en">
      <body>
        <Provider session={params.session}>
          {children}
        </Provider>
      </body>
    </html>
  );
}
