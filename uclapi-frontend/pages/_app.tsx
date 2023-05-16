import "@/styles/sass/common/uclapi.scss";
import "@/styles/sass/navbar.scss";
import "../lib/ErrorReporting";
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
