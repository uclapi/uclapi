/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types


// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'
import "react-responsive-carousel/lib/styles/carousel.min.css"

// Standard React imports
import React from 'react'
import ReactDOM from 'react-dom'
// External carousel dependency
import { Carousel } from "react-responsive-carousel"
import { BrowserRouter, Route, Switch } from 'react-router-dom'

// Grab titles and descriptions of app
import { allApps } from 'Layout/data/app_pages.jsx'
// Common Components
import { ButtonView, CardView, Column, Footer, ImageView, 
  NavBar, Container, TextView, Row } from 'Layout/Items.jsx'
// Import page that displays a singular app
import { AppPage } from './AppPage.jsx'

class Marketplace extends React.Component {

  constructor(props) {
    super(props)
    const DEBUGGING = false

    if (DEBUGGING) { console.log(`All apps loaded in: ` + allApps) }

    // Set up the 'featured' apps section
    const featuredApps = []
    featuredApps.push(allApps[`uclassistant`])

    // Segregate into groups of applications if needed
    const appsToRender = []
    appsToRender.push(allApps[`uclroombuddy`])
    appsToRender.push(allApps[`uclassistant`])
    appsToRender.push(allApps[`uclcssa`])

    this.state = {
      'featuredApps': featuredApps,
      'appsToRender': appsToRender,
    }
  }

  render() {
    const iconsize = `100px`
    // const logosize = `150px`
    const {
      featuredApps,
      appsToRender,
    } = this.state

    return (
      <>

        <NavBar isScroll={false} />

        <Container
          height='300px'
          style={{ margin: `60px 0 0 0` }}
          styling='splash-parallax'
        >
          <Row
            width='2-3'
            horizontalAlignment='center'
            verticalAlignment='center'
            alignItems='column'
          >
            <TextView text={`UCL Marketplace`} heading={1} align={`center`} />
            <TextView
              text={`Apps that use UCL API`}
              heading={2}
              align={`center`}
            />
          </Row>
        </Container>

        <Container styling='secondary'>
          <Row 
            width='2-3' 
            horizontalAlignment='center'
            alignItems='column'
          >
            <TextView text={`Featured App`} heading={2} align={`left`} />
            <TextView
              text={`Our favourite usage of the API`}
              heading={5}
              align={`left`}
            />
          </Row>
          <Row
            width='2-3'
            horizontalAlignment='center'
          >
            {featuredApps.map((app, i) => {
              return (
                <CardView
                  key={`featured-app-` + i}
                  width={`1-1`}
                  type={`emphasis`}
                  link={`/marketplace/` + app.id}
                  noPadding
                >
                  <Row 
                    width='1-2' 
                    horizontalAlignment='center'
                    alignItems='column'
                  >
                    <ImageView
                      src={app.logolight}
                      width={iconsize}
                      height={iconsize}
                      style={{ 'margin': `20px 0` }}
                      centred
                    />
                    <TextView
                      text={app.name}
                      heading={2}
                      align={`center`}
                      color={`white`}
                    />
                    <TextView
                      text={app.description}
                      heading={5}
                      align={`center`}
                      color={`white`}
                    />
                  </Row>
                </CardView>
              )
            })}
          </Row>
        </Container>

        <Container styling='splash-parallax'>
          <Row 
            width='2-3' 
            horizontalAlignment='center'
            alignItems='column'
          >
            <TextView text={`All Apps`} heading={2} align={`left`} />
            <TextView
              text={`Every app made using the API`}
              heading={5}
              align={`left`}
            />
          </Row>
          <Row
            width='2-3'
            horizontalAlignment='center'
          >
            {appsToRender.map((app, i) => {
              return (
                <CardView
                  key={`all-apps-` + i}
                  width={`1-2`}
                  type={`alternate`}
                  link={`/marketplace/` + app.id}
                  style={{
                    float: `left`,
                  }}
                  minWidth={`225px`}
                  snapAlign
                >
                  <Row 
                    width='9-10' 
                    horizontalAlignment='center'
                    alignItems='column'
                  >
                    <ImageView
                      src={app.logolight}
                      width={iconsize}
                      height={iconsize}
                      style={{ 'margin': `20px 0` }}
                      centred
                    />
                    <TextView
                      text={app.name}
                      heading={2}
                      align={`center`}
                      color={`black`}
                    />
                    <TextView
                      text={app.description}
                      heading={5}
                      align={`center`}
                      color={`black`}
                    />
                  </Row>
                </CardView>
              )
            })}
          </Row>
        </Container>

        <Footer />

      </>
    )
  }
}

class Main extends React.Component {
  renderAppPage = (props) => (
    <AppPage appId={props.match.params.appId} />
  )
  render() {
    return (
      <main>
        <Switch>
          <Route exact path='/marketplace' component={Marketplace} />
          <Route path='/marketplace/:appId' render={this.renderAppPage} />
        </Switch>
      </main>
    )
  }
}

ReactDOM.render(
  <BrowserRouter>
    <Main />
  </BrowserRouter>,
  document.querySelector(`#root`)
)