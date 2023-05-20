import "rsuite/dist/rsuite-no-reset.min.css";
import "@/styles/sass/common/uclapi.scss";
import "@/styles/sass/navbar.scss";
import "../lib/ErrorReporting";
import type { AppProps } from "next/app";
import { SessionProvider } from "next-auth/react";
import { NavBar,Footer } from '@/components/layout/Items.jsx'

export default function App({
  Component,
  pageProps: { session, ...pageProps },
}: AppProps) {
  return (
    <SessionProvider session={session}>
      <NavBar isScroll={false} />
      <Component {...pageProps} />
      <Footer />
    </SessionProvider>
  );
}
