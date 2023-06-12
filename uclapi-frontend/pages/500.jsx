import Warning from '@/components/layout/Warning.jsx'
import Head from 'next/head';


const InternalServerErrorPage = () => (
  <>
    <Head>
      Error 500 - UCL API
    </Head>

    <Warning
      title="Error 500"
      content="Oops... something went wrong! Sorry for the inconvenience. Our team is working on it, if you have an urgent concern please get in touch with us at isd.apiteam@ucl.ac.uk. Click below to go back to the front page:"
    />
  </>
)

export default InternalServerErrorPage
