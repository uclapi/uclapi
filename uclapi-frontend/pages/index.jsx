import { endpoints, FAQ } from '@/components/layout/data/homepage_constants.jsx'
import {
  Button,
  CardView,
  Column,
  Container,
  Demo,
  Footer,
  NavBar,
  Row,
  TextView,
} from '@/components/layout/Items.jsx'
import Collapse, { Panel } from 'rc-collapse'
import React from "react";
import Image from 'next/image'

import styles from '../styles/Home.module.scss'

class HomePage extends React.Component {

  constructor(props) {
    super(props)

    let loggedIn = false
    if (typeof window !== 'undefined') {
      if (window.initialData?.logged_in === `True`) { loggedIn = true }

      this.state = {
        articles: window.initialData?.medium_articles,
        host: window.location.hostname,
        loggedIn: loggedIn,
      }
    } else {
      this.state = {}
    }
  }

  render() {
    const iconsize = 200
    const { host, articles, loggedIn } = this.state

    let startLabel = `START BUILDING`

    if (loggedIn) {
      startLabel = `DASHBOARD`
    }

    return (
      <>

        <NavBar isScroll={false} />

        {/* Staging banner */}

        {host == `staging.ninja` && (
          <Container isPadded styling='warning-red'>
            <Row width='9-10' horizontalAlignment={`center`} >
              <TextView
                align={`center`}
                text={
                  `Warning! This is our bleeding-edge staging environment.` +
                  `Performance, accuracy and reliability of the API cannot `+
                  `be guaranteed. For our stable, supported API please go to:`
                }
                heading={1}
              />
              <TextView
                align={`center`}
                text={`uclapi.com`}
                heading={2}
                link={`https://uclapi.com`}
              />
            </Row>
          </Container>
        )}

        {/* API Landing page */}

        <Container height='600px' styling='splash-parallax'>
          <Row width='2-3'
            horizontalAlignment='center'
            verticalAlignment='center'
            alignItems='column'
          >
            <TextView
              text={`UCL API`}
              heading={1}
              align={`center`}
            />
            <TextView
              text={
                `UCL API is a student-built platform for `+
                `developers to improve the experience of `+
                `everyone at UCL.`
              }
              heading={2}
              align={`center`}
            />

            <Row width='1-1'
              horizontalAlignment='center'
              alignItems='row'
            >
              <Button link={`/dashboard`}>{startLabel}</Button>
              <Button link={`/docs`} type={`alternate`}>DOCS</Button>
            </Row>

          </Row>
        </Container>

        {/* API Description  */}

        <Container styling='secondary' heading="Our Goals">
          <Row
            horizontalAlignment='center'
            width='1-1'
            maxWidth='1000px'
            className="Row-horizontal"
          >
            <Column width='1-3'>
              <TextView
                text={`Make Simple Interfaces`}
                heading={2}
                align={`center`}
              />
              <TextView
                text={
                  `The endpoints are streamlined to enable any developer `+
                  `to easily pick up and use the API. We hope that developers `+
                  `of all abilities find our endpoints and website easy to ` +
                  `navigate. We want integrating with our API to be the ` +
                  `easiest part of your development process!`
                }
                align={`justify`}
                heading={5}
              />
              <Image
                src={`/home-page/star.svg`}
                width={iconsize}
                height={iconsize}
              />
            </Column>
            <Column width='1-3'>
              <TextView
                text={`Put Documentation First`}
                heading={2}
                align={`center`}
              />
              <TextView
                text={
                  `As developers we feel the pain of bad documentation: ` +
                  `this is why we are strive to write clear and concise ` +
                  `documentation. We want you to spend less time worrying ` +
                  `about how to use our API and more time thinking about how `+
                  `to revolutionise the student experience. With good ` +
                  `documentation we allow you to focus on building helpful `+
                  `applications.`
                }
                align={`justify`}
                heading={5}
              />
              <Image
                src={`/home-page/docs.svg`}
                width={iconsize}
                height={iconsize}
              />
            </Column>
            <Column width='1-3'>
              <TextView
                text={`Enable Developers`}
                heading={2}
                align={`center`}
              />
              <TextView
                text={
                  `We want the API to be able to support any idea, `+
                  `no matter how big, that improves students' lives. `+
                  `We are always open to suggestions for new endpoints `+
                  `and functionality so we can enable a greater range `+
                  `of applications to be developed. We cannot wait to see ` +
                  `what you will develop!`
                }
                align={`justify`}
                heading={5}
              />
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
          styling='splash-parallax'
          heading="Get Started using our APIs"
        >
          <Row width='1-1'
            horizontalAlignment='center'
            maxWidth='1000px'
            className="Row-horizontal"
          >
            {endpoints.map(({ name, link, description }) => (
              <CardView width={`1-2`} link={link} key={link} >
                <Container height='100px' style={{ padding: `20px 0` }} >
                  <Row width='2-3'
                    horizontalAlignment='center'
                    verticalAlignment='center'
                    alignItems='column'
                  >
                    <TextView text={name} heading={2} align={`center`} />
                    <TextView
                      text={description}
                      heading={5}
                      align={`center`}
                      noMargin
                    />
                  </Row>
                </Container>
              </CardView>))}
          </Row>
        </Container>

        {/* Demo */}

        <Demo />

        {/* Blog */}

        <Container styling='splash-parallax' heading="Check out our blog">
          <Row
            width='9-10'
            horizontalAlignment='center'
            className="Row-horizontal"
          >
            {articles?.map(({
              url, image_url: imageURL, title, creator, published,
            }) => (
                <CardView
                  width='1-3'
                  link={url}
                  key={url}
                  style={{ padding: 0 }}
                >
                  <Row width='1-1'>
                    <Container height='200px'
                      style={{
                        backgroundSize: `Cover`,
                        overflow: `hidden`,
                      }}
                      noPadding
                    >
                      <Row width='1-1'
                        horizontalAlignment='center'
                        verticalAlignment='center'
                      >
                        <div className="animate-image">
                          <Image
                            src={
                              imageURL == `url_not_found`
                                ? '/home-page/splash_screen.png'
                                : imageURL
                            }
                            width='100%'
                            height='200px'
                            style={{
                              display: `block`,
                              objectFit: `cover`,
                            }}
                          />
                        </div>
                        <TextView text={title}
                          align={`center`}
                          heading={3}
                          color={`white`}
                          style={{
                            width: `100%`,
                            position: `absolute`,
                            top: `85px`,
                          }}
                        />
                      </Row>
                    </Container>
                    <Container color='transparent'>
                      <Row width='1-1'
                        horizontalAlignment='center'
                        verticalAlignment='center'
                        alignItems='column'
                      >
                        <TextView
                          text={creator}
                          align={`center`}
                          heading={6}
                          color={`white`}
                        />
                        <TextView
                          text={published.substring(0, 16)}
                          align={`center`}
                          heading={6}
                          color={`white`}
                        />
                      </Row>
                    </Container>
                  </Row>
                </CardView>
              ))}
          </Row>
        </Container>

        {/* Marketplace */}

        <Container styling="secondary" >
          <Row width="1-1" horizontalAlignment="center">
            <Column
              width="1-2"
              className="default"
            >
              <Image
                src={`/home-page/uclassistantmarket.png`}
                width={367}
                height={405}
                description="ucl asssitant screen shot"
              />
            </Column>

            <Column width="1-2"
              textAlign="left"
            >
              <TextView text="UCL MARKETPLACE" heading={1} align="center" />

              <TextView text={
                `The UCL Marketplace contains all known public `+
                `integrations with the UCL API. We are constantly looking ` +
                `for more to add to the marketplace and promote so we ` +
                `would love to hear about your creations so we can add them!`
                }
                heading={5}
                align={`left`}
                style={{ padding: `0 2%` }}
              />

              <TextView text={
                `One of these applications is UCL Assistant! An app created
                by the UCL API team to provide students with a reliable way to
                check their timetable, find empty rooms and locate study
                spaces.`
              }
                heading={5}
                align={`left`}
                style={{ padding: `0 2%` }}
              />

              <Row width='1-1'
                horizontalAlignment='center'
                alignItems='row'
              >
                <Button
                  link={`/marketplace`}
                  type='alternate'
                >
                  MARKETPLACE
                </Button>
                <Button
                  link={`/marketplace/uclassistant`}
                  type='alternate'
                >
                  UCL ASSISTANT
                </Button>
            </Row>
            </Column>
          </Row>
        </Container>

        {/* FAQ */}

        <Container
          styling='splash-parallax'
          heading='Frequently asked questions'
        >
          <Row
            width='2-3'
            horizontalAlignment='center'
            alignItems='column'
          >
            <Collapse>
            {FAQ.map(({ question, answer }) => (
              <Panel
                openAnimation={{}}
                key={question}
                header={question}
                showArrow
              >
                {answer}
              </Panel>
            ))}
          </Collapse>
          </Row>
        </Container>

        <Footer />

      </>
    )
  }
}

export default HomePage
