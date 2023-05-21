import { endpoints, FAQ } from '@/data/homepage_constants'
import {
  CardView,
  Column,
  Container,
  Demo,
  Row,
} from '@/components/layout/Items.jsx'
import { Panel, PanelGroup, Button } from 'rsuite'
import React from "react";
import Image from 'next/image'
import withSession from '@/lib/withSession.jsx'
const { XMLParser } = require("fast-xml-parser");

import styles from '../styles/Home.module.scss'

export const getStaticProps = async (context) => {
  const mediumBlogFeedXml = await fetch('https://medium.com/feed/ucl-api').then(res => res.text());
  const parser = new XMLParser();
  const mediumBlogFeedJson = parser.parse(mediumBlogFeedXml);

  const articles = mediumBlogFeedJson.rss.channel.item.slice(0, 3).map(i => {
    let imageURL = null;
    const content = i['content:encoded'];
    if (content.startsWith("<figure><img")) {
      imageURL = content.substring(25).split('" />')[0];
    }
    return {
      title: i.title,
      url: i.link,
      imageURL,
      creator: i['dc:creator'],
      published: i.pubDate,
    };
  })

  return {
    props: {articles},
    // Refresh every day (ISR: https://nextjs.org/docs/pages/building-your-application/data-fetching/incremental-static-regeneration)
    revalidate: 86400,
  };
}

class HomePage extends React.Component {
  componentDidMount() {
    this.setState({host: window.location.hostname});
  }

  render() {
    const iconsize = 200;

    const startLabel = !!this.props.session ? "DASHBOARD" : `START BUILDING`;

    return (
      <>
        {/* Staging banner */}
        {this.props.host == `staging.ninja` && (
          <Container isPadded styling="warning-red">
            <Row width="9-10" horizontalAlignment={`center`}>
              <h1>
                  Warning! This is our bleeding-edge staging environment.
                  Performance, accuracy and reliability of the API cannot
                  be guaranteed. For our stable, supported API please go to:
              </h1>
              <a href='https://uclapi.com'>
                <h2>
                  uclapi.com
                </h2>
              </a>
            </Row>
          </Container>
        )}

        {/* API Landing page */}

        <Container height="600px" styling="splash-parallax">
          <Row
            width="2-3"
            horizontalAlignment="center"
            verticalAlignment="center"
            alignItems="column"
          >
            <h1>UCL API</h1>
            <h2>
              UCL API is a student-built platform for developers to improve the
              experience of everyone at UCL.
            </h2>

            <Row width="1-1" horizontalAlignment="center" alignItems="row">
              <Button size="lg" className="grey-btn" href={`/dashboard`}>
                {startLabel}
              </Button>
              <Button size="lg" href={`/docs`}>
                DOCS
              </Button>
            </Row>
          </Row>
        </Container>

        {/* API Description  */}

        <Container styling="secondary" heading="Our Goals">
          <Row
            horizontalAlignment="center"
            width="1-1"
            maxWidth="1000px"
            className="Row-horizontal"
          >
            <Column width="1-3">
              <h2>Make Simple Interfaces</h2>
              <p className='description'>
                The endpoints are streamlined to enable any developer to easily
                pick up and use the API. We hope that developers of all
                abilities find our endpoints and website easy to navigate. We
                want integrating with our API to be the easiest part of your
                development proces.
              </p>
              <Image
                src={`/home-page/star.svg`}
                width={iconsize}
                height={iconsize}
              />
            </Column>
            <Column width="1-3">
              <h2>Put Documentation First</h2>
              <p className='description'>
                As developers we feel the pain of bad documentation: this is why
                we are strive to write clear and concise documentation. We want
                you to spend less time worrying about how to use our API and
                more time thinking about how to revolutionise the student
                experience. With good documentation we allow you to focus on
                building helpful application.
              </p>
              <Image
                src={`/home-page/docs.svg`}
                width={iconsize}
                height={iconsize}
              />
            </Column>
            <Column width="1-3">
              <h2>Enable Developers</h2>
              <p className='description'>
                We want the API to be able to support any idea, no matter how
                big, that improves students' lives. We are always open to
                suggestions for new endpoints and functionality so we can enable
                a greater range of applications to be developed. We cannot wait
                to see what you will develop!
              </p>
              <Image
                src={`/home-page/heart.svg`}
                width={iconsize}
                height={iconsize}
              />
            </Column>
          </Row>
        </Container>

        {/* API Endpoints */}

        <Container
          styling="splash-parallax"
          heading="Get Started using our APIs"
        >
          <div className={styles.apiEndpointsWrapper}>
            {endpoints.map(({ name, link, description }) => (
              <CardView width={`1`} link={link} key={link}>
                <h2>{name}</h2>
                <p className={`description ${styles.centerAlign}`}>
                  {description}
                </p>
              </CardView>
            ))}
          </div>
        </Container>

        {/* Demo */}

        <Demo />

        {/* Blog */}

        <Container styling="splash-parallax" heading="Check out our blog">
          <Row
            width="9-10"
            horizontalAlignment="center"
            className="Row-horizontal"
          >
            {this.props.articles?.map(
              ({ url, imageURL, title, creator, published }) => (
                <CardView
                  width="1-3"
                  link={url}
                  key={url}
                  style={{ padding: 0 }}
                >
                  <Row width="1-1">
                    <Container
                      height="200px"
                      style={{
                        backgroundSize: `Cover`,
                        overflow: `hidden`,
                      }}
                      noPadding
                    >
                      <Row
                        width="1-1"
                        horizontalAlignment="center"
                        verticalAlignment="center"
                      >
                        <div className="animate-image">
                          <Image
                            src={imageURL ?? "/home-page/splash_screen.png"}
                            width={100}
                            height={200}
                            style={{
                              display: `block`,
                              objectFit: `cover`,
                              width: `100%`,
                            }}
                          />
                        </div>
                        <h3
                          style={{
                            width: `100%`,
                            position: `absolute`,
                            top: `85px`,
                          }}
                        >
                          {title}
                        </h3>
                      </Row>
                    </Container>
                    <Container color="transparent">
                      <Row
                        width="1-1"
                        horizontalAlignment="center"
                        verticalAlignment="center"
                        alignItems="column"
                      >
                        <p>{creator}</p>
                        <p>
                          {published.substring(0, 16)}
                        </p>
                      </Row>
                    </Container>
                  </Row>
                </CardView>
              )
            )}
          </Row>
        </Container>

        {/* Marketplace */}

        <Container styling="secondary">
          <Row width="1-1" horizontalAlignment="center">
            <Column width="1-2" className="default">
              <Image
                src={`/home-page/uclassistantmarket.png`}
                width={367}
                height={405}
                description="ucl asssitant screen shot"
              />
            </Column>

            <Column width="1-2" textAlign="left">
              <h1>UCL MARKETPLACE</h1>

              <p className='description'>
                The UCL Marketplace contains all known public integrations with
                the UCL API. We are constantly looking for more to add to the
                marketplace and promote so we would love to hear about your
                creations so we can add them!
              </p>
              <p className='description'>
                One of these applications is UCL Assistant! An app created by
                the UCL API team to provide students with a reliable way to
                check their timetable, find empty rooms and locate study spaces.
              </p>

              <Row width="1-1" horizontalAlignment="center" alignItems="row">
                <Button size="lg" href={`/marketplace`}>
                  MARKETPLACE
                </Button>
                <Button size="lg" href={`/marketplace/uclassistant`}>
                  UCL ASSISTANT
                </Button>
              </Row>
            </Column>
          </Row>
        </Container>

        {/* FAQ */}

        <Container
          styling="splash-parallax"
          heading="Frequently asked questions"
        >
          <Row width="2-3" horizontalAlignment="center" alignItems="column">
            <PanelGroup accordion>
              {FAQ.map(({ question, answer }, i) => (
                <Panel className={styles.faq} eventKey={i} header={question}>
                  {answer}
                </Panel>
              ))}
            </PanelGroup>
          </Row>
        </Container>
      </>
    );
  }
}

export default withSession(HomePage)
