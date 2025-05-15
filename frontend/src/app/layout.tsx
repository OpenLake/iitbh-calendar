import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ReduxProvider } from "../redux/provider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Timetable Generator",
  description:
    "A online tool to generate your course timetable based on the courses you select",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {" "}
        <ReduxProvider>{children}</ReduxProvider>
      </body>
    </html>
  );
}
