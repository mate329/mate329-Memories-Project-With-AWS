'use-client'

import Image from 'next/image';

interface AuthPageLayoutProps {
    children: React.ReactNode;
}

export default function AuthPageLayout({
    children,
}: AuthPageLayoutProps) {
    return (
        <main className="flex m-0 relative h-screen">
            <div className="flex items-center justify-center w-full md:w-1/2 flex-col">
                <div className="flex items-center flex-col gap-4">
                    <Image
                        src="/icons/logo.svg"
                        alt="App Logo"
                        width={60}
                        height={60}
                    />
                    <div className="w-full max-w-md">
                        {children}
                    </div>
                </div>
            </div>
            <div className="hidden md:block md:w-1/2 relative h-screen">
                <Image 
                    src="/images/rijeka.jpeg" 
                    alt="Rijeka" 
                    layout="fill"
                    objectFit='cover'
                    priority
                />
            </div>
        </main>
    );
}
