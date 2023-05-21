import { useRouter } from "next/router";
import { allApps } from "@/data/app_pages.jsx";

// Import page that displays a singular app
import { AppPage } from '@/components/AppPage.jsx'
export default function MarketplaceApp() {
  const router = useRouter();
  const { app } = router.query;
  return <AppPage appId={app} />;
}

export async function getStaticPaths() {
  return {
    paths: Object.keys(allApps).map(app => ({params: {app}})) ,
    fallback: false,
  };
}

export async function getStaticProps(context) {
  return { props: { appId: context.params.app } };
}
