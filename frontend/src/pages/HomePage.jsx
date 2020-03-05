// Standard React imports
// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// External dependencies
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'
import ReactDOM from 'react-dom'

// Images
import docs from 'Images/home-page/docs.svg'
import heart from 'Images/home-page/heart.svg'
import placeholder from 'Images/home-page/splash_screen.png'
import star from 'Images/home-page/star.svg'
import uclassistantmarket from 'Images/home-page/uclassistantmarket.png'
import { endpoints, FAQ } from 'Layout/data/homepage_constants.jsx'
// Components
import { ButtonView, CardView, Column, Demo, Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

const questionandanswer = (question, answer) => (
  <Collapse>
    <Panel header={question} showArrow>
      <TextView text={answer} heading={`p`} />
    </Panel>
  </Collapse>
)

class HomePage extends React.Component {

  constructor(props) {
    super(props)

    let loggedIn = false
    if (window.initialData.logged_in === `True`) { loggedIn = true }

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

        {host == `staging.ninja` && (
          <Row isPadded styling='warning-red'>
            <Column width='9-10' horizontalAlignment={`center`} >
              <TextView align={`center`} text={`Warning! This is our bleeding-edge staging environment, and therefore performance, accuracy and reliability of the API cannot be guaranteed. For our stable, supported API please go to:`} heading={1} />
              <TextView align={`center`} text={`uclapi.com`} heading={2} link={`https://uclapi.com`} />
            </Column>
          </Row>
        )}

        <Row height='600px' styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
            <TextView text={`UCL API`} heading={1} align={`center`} />
            <TextView text={`UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL.`} heading={2} align={`center`} />
            <ButtonView text={startLabel} link={`/dashboard`} />
            <ButtonView text={`DOCS`} link={`/docs`} type={`alternate`} />
          </Column>
        </Row>

        <Row styling='secondary'>
          <Column width='1-1' horizontalAlignment='center' maxWidth='1000px' minWidth='300px'>
            <TextView text={`Our Goals`} heading={1} align={`center`} />
          </Column>
          <Column
            width='1-1'
            horizontalAlignment='center'
            maxWidth='1000px'
            minWidth='300px'
            className="column-horizontal"
          >
            <CardView width='1-3' minWidth='280px' type='no-bg' snapAlign>
              <TextView text={`Make Simple Interfaces`} heading={2} align={`center`} />
              <TextView text={`The endpoints are streamlined to enable any developer to easily pick up and use the api. We hope that developers of all ability
                            find our endpoints and website easy to navigate. We do not want to overcomplicate the process of developing
                            awesome apps, we want to be the easiest part of your development process!`}
                align={`justify`}
                heading={5}
              />
              <ImageView src={star} width={iconsize} height={iconsize} description={`an icon of a love heart`} centred />
            </CardView>
            <CardView width='1-3' minWidth='280px' type='no-bg' snapAlign>
              <TextView text={`Put Documentation First`} heading={2} align={`center`} />
              <TextView text={`As developers we feel the pain of bad documentation: this is why we are driven by good documentation. We want you
                             to spend less time worrying about how to use our api and more time thinking about how to revolutionise the student experience.
                             With good documentation we allow you to focus on building helpful applications.`}
                align={`justify`}
                heading={5}
              />
              <ImageView src={docs} width={iconsize} height={iconsize} description={`an icon of a clipboard`} centred />
            </CardView>
            <CardView width='1-3' minWidth='280px' type='no-bg' snapAlign>
              <TextView text={`Enable Developers`} heading={2} align={`center`} />
              <TextView text={`We want the api to be so comprehensive that any idea, no matter how big, can be created in order to improve students lives. We are always
                             open to suggestions for new endpoints and functionality so we can enable a greater range of applications to be developed. We
                             cannot wait to see what you will develop!`}
                align={`justify`}
                heading={5}
              />
              <ImageView src={heart} width={iconsize} height={iconsize} description={`an icon of a star`} centred />
            </CardView>
          </Column>
        </Row>

        <Row styling='splash-parallax'>
          <Column width='2-3'
            horizontalAlignment='center'
            maxWidth='1000px'
            minWidth='300px'
          >
            <TextView text={`Get Started using our APIs`} heading={1} align={`center`} />
          </Column>
          <Column width='2-3'
            horizontalAlignment='center'
            maxWidth='1000px'
            minWidth='300px'
            className="column-horizontal"
          >
            {endpoints.map((x, key) => (
              <CardView width={`1-2`} minWidth={`280px`} link={x.link} key={key} snapAlign>
                <Row height='100px' style={{ padding: `20px 0` }} >
                  <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
                    <TextView text={x.name} heading={2} align={`center`} />
                    <TextView text={x.description} heading={5} align={`center`} noMargin />
                  </Column>
                </Row>
              </CardView>))}
          </Column>
        </Row>

        <Demo />

        <Row styling='splash-parallax'>
          <Column width='9-10' horizontalAlignment='center'>
            <TextView text={`Check out our blog`} styling='transparent' heading={1} align={`center`} />
          </Column>
          <Column width='9-10' horizontalAlignment='center' className="column-horizontal">
            {articles.map(x => (
              <CardView width='1-3' minWidth='280px' link={x.url} key={x.link} snapAlign>
                <Column width='1-1'>
                  <Row height='200px'
                    style={{
                      backgroundSize: `Cover`,
                      overflow: `hidden`,
                    }}
                    noPadding
                  >
                    <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
                      <div className="animate-image">
                        <ImageView src={x.image_url == `url_not_found` ? placeholder : x.image_url}
                          style={{
                            display: `block`,
                            width: `100%`,
                            height: `200px`,
                            objectFit: `cover`,
                          }}
                          description={x.title + ` background`}
                          centred
                        />
                      </div>
                      <TextView text={x.title}
                        align={`center`}
                        heading={3}
                        color={`white`}
                        style={{
                          width: `100%`,
                          position: `absolute`,
                          top: `85px`,
                        }}
                      />
                    </Column>
                  </Row>
                  <Row color='transparent'>
                    <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
                      <TextView text={x.creator} align={`center`} heading={6} color={`white`} />
                      <TextView text={x.published.substring(0, 16)} align={`center`} heading={6} color={`white`} />
                    </Column>
                  </Row>
                </Column>
              </CardView>
            ))}
          </Column>
        </Row>

        <div className={`mobile tablet`}>
          <Row styling="secondary" >
            <Column width="2-3" textAlign="center" minWidth="250px" horizontalAlignment="center">
              <TextView text="UCL MARKETPLACE" heading={1} align="center" />

              <TextView text={`The UCL Marketplace contains all of the applications written
                    using UCL API for some of their functionality. We are constantly looking for 
                    applications to add to the marketplace and promote so we would love to hear
                    about your creations so we can add them!`}
                heading={5}
                align={`center`}
              />

              <TextView text={`One of these applications is UCL Assistant! An app created
                    by the UCL API team to provide students with a reliable way to check their 
                    timetable, find empty rooms and locate study spaces.`}
                heading={5}
                align={`center`}
              />

              <ButtonView text={`MARKETPLACE`} link={`/marketplace`} style={{ "marginLeft": `0` }} />
              <ButtonView text={`UCL ASSISTANT`} link={`/marketplace/uclassistant`} type='alternate' />
            </Column>
          </Row>
        </div>
        <div className={`default`}>
          <Row styling="secondary" >
            <Column width="2-3" minWidth="250px" horizontalAlignment="center">
              <Column width="1-2" minWidth="200px">
                <ImageView src={uclassistantmarket} width="367px" height="405px" description="ucl asssitant screen shot" />
              </Column>

              <Column width="1-2" minWidth="200px" textAlign="left" horizontalAlignment="right" verticalAlignment="center">
                <TextView text="UCL MARKETPLACE" heading={1} align="left" />

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

                <ButtonView text={`MARKETPLACE`} link={`/marketplace`} style={{ "marginLeft": `0` }} />
                <ButtonView text={`UCL ASSISTANT`} link={`/marketplace/uclassistant`} type='alternate' />
              </Column>
            </Column>
          </Row>
        </div>

        <Row styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center'>
            <TextView text={`Frequently Asked Questions`} heading={1} align={`center`} />
            {FAQ.map(x => (
              questionandanswer(x.question, x.answer)
            ))}
          </Column>
        </Row>

        <Footer />

      </>
    )
  }

}

ReactDOM.render(
  <HomePage />,
  document.querySelector(`.app`)
)
