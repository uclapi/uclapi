// Standard React imports
// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Images
import docs from 'Images/home-page/docs.svg'
import heart from 'Images/home-page/heart.svg'
import placeholder from 'Images/home-page/splash_screen.png'
import star from 'Images/home-page/star.svg'
import uclassistantmarket from 'Images/home-page/uclassistantmarket.png'
import { endpoints, FAQ } from 'Layout/data/homepage_constants.jsx'
// Components
import {
  ButtonView,
  CardView,
  Column,
  Container,
  Demo,
  Footer,
  ImageView,
  NavBar,
  Row,
  TextView,
} from 'Layout/Items.jsx'
// External dependencies
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'
import ReactDOM from 'react-dom'

class HomePage extends React.Component {

  constructor(props) {
    super(props)

    let loggedIn = false
    if (window.initialData.logged_in === `True`) { loggedIn = true }

    if (window.initialData.has_just_logged_out === `True`) { 
      // TODO: Decide on a way to let user know they have not been properly logged out
      //alert("You have been logged out of UCL API. However, you are still logged in to "
      //  + "other UCL services. To log out completely, please close your web browser.")
    }

    this.state = {
      articles: window.initialData.medium_articles,
      host: window.location.hostname,
      loggedIn: loggedIn,
    }
  }

  render() {
    const iconsize = `200px`
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
                text={`Warning! This is our bleeding-edge staging environment. Performance, accuracy and reliability of the API cannot be guaranteed. For our stable, supported API please go to:`}
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
              text={`UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL.`}
              heading={2}
              align={`center`}
            />

            <ButtonView text={startLabel} link={`/dashboard`} centred />
            <ButtonView text={`DOCS`} link={`/docs`} type={`alternate`} centred />
          </Row>
        </Container>

        {/* API Description  */}

        <Container styling='secondary' heading="Our Goals">
          <Row
            width='1-1'
            horizontalAlignment='center'
            maxWidth='1000px'
            className="Row-horizontal"
          >
            <Column width='1-3'>
              <TextView text={`Make Simple Interfaces`} heading={2} align={`center`} />
              <TextView text={`The endpoints are streamlined to enable any developer to easily pick up and use the API. We hope that developers of all ability
                            find our endpoints and website easy to navigate. We do not want to overcomplicate the process of developing
                            awesome apps, we want to be the easiest part of your development process!`}
                align={`justify`}
                heading={5}
              />
              <ImageView src={star} width={iconsize} height={iconsize} description={`an icon of a love heart`} centred />
            </Column>
            <Column width='1-3'>
              <TextView text={`Put Documentation First`} heading={2} align={`center`} />
              <TextView text={`As developers we feel the pain of bad documentation: this is why we are driven by good documentation. We want you
                             to spend less time worrying about how to use our api and more time thinking about how to revolutionise the student experience.
                             With good documentation we allow you to focus on building helpful applications.`}
                align={`justify`}
                heading={5}
              />
              <ImageView src={docs} width={iconsize} height={iconsize} description={`an icon of a clipboard`} centred />
            </Column>
            <Column width='1-3'>
              <TextView text={`Enable Developers`} heading={2} align={`center`} />
              <TextView text={`We want the api to be so comprehensive that any idea, no matter how big, can be created in order to improve students lives. We are always
                             open to suggestions for new endpoints and functionality so we can enable a greater range of applications to be developed. We
                             cannot wait to see what you will develop!`}
                align={`justify`}
                heading={5}
              />
              <ImageView
                src={heart}
                width={iconsize}
                height={iconsize}
                description={`an icon of a star`}
                centred
              />
            </Column>
          </Row>
        </Container>

        {/* API Endpoints */}

        <Container
          styling='splash-parallax'
          heading="Get Started using our APIs"
        >
          <Row width='2-3'
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
            {articles.map(({
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
                          <ImageView
                            src={
                              imageURL == `url_not_found`
                                ? placeholder
                                : imageURL
                            }
                            style={{
                              display: `block`,
                              width: `100%`,
                              height: `200px`,
                              objectFit: `cover`,
                            }}
                            description={title + ` background`}
                            centred
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
          <Row width="2-3" horizontalAlignment="center">
            <Column
              width="1-2"
              className="default"
            >
              <ImageView src={uclassistantmarket} width="367px" height="405px" description="ucl asssitant screen shot" />
            </Column>

            <Column width="1-2"
              textAlign="left"
            >
              <TextView text="UCL MARKETPLACE" heading={1} align="center" />

              <TextView text={`The UCL Marketplace contains all of the applications written
                using UCL API for some of their functionality. We are constantly looking for 
                applications to add to the marketplace and promote so we would love to hear
                about your creations so we can add them!`}
                heading={5}
                align={`left`}
              />

              <TextView text={`One of these applications is UCL Assistant! An app created
                by the UCL API team to provide students with a reliable way to check their 
                timetable, find empty rooms and locate study spaces.`}
                heading={5}
                align={`left`}
              />

              <ButtonView text={`MARKETPLACE`} link={`/marketplace`} type='alternate' centred />
              <ButtonView text={`UCL ASSISTANT`} link={`/marketplace/uclassistant`} type='alternate' centred />
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
            {FAQ.map(({ question, answer }) => (
              <Collapse key={question}>
                <Panel header={question} showArrow>
                  <TextView text={answer} heading={`p`} />
                </Panel>
              </Collapse>
            ))}
          </Row>
        </Container>

        <Footer />

      </>
    )
  }

}

ReactDOM.render(
  <HomePage />,
  document.querySelector(`.app`)
)
