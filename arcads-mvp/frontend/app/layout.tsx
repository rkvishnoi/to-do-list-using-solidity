import "./globals.css";
import Providers from "@/components/Providers";
import { ReactNode } from "react";

export const metadata = { title: "Arcads MVP", description: "UGC ad generator" };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <div className="min-h-screen">
            <header className="border-b bg-white">
              <div className="max-w-5xl mx-auto p-4 flex justify-between items-center">
                <div className="font-semibold">Arcads MVP</div>
                <a className="text-sm text-blue-600" href="/dashboard">Dashboard</a>
              </div>
            </header>
            <main className="max-w-5xl mx-auto p-4">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}