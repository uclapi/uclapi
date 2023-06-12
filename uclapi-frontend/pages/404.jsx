import Warning from '@/components/layout/Warning.jsx'
import Head from 'next/head';



const NotFoundPage = () => (
  <>
    <Head>
      Error 404 - UCL API
    </Head>

    <Warning
      title="Error 404"
      content="Oops we cannot seem to find that page! Please click below to go back to the front page:"
    />
  </>
)

export default NotFoundPage
