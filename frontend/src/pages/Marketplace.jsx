// Standard React imports
// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

import PropTypes from 'prop-types'
import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

// Images
// Backgrounds
import arrow from 'Images/marketplace/arrow-left.svg'
// Grab titles and descriptions of app
import { allApps } from 'Layout/data/app_pages.jsx'
// Common Components
import { ButtonView, CardView, Column, Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

class Marketplace extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      DEBUGGING: false,
    }

    const { DEBUGGING } = this.state
    if (DEBUGGING) { console.log(`All apps loaded in: ` + allApps) }

    // Set up the 'featured' apps section
    const featuredApps = []
    featuredApps.push(allApps[`uclassistant`])

    // Segregate into groups of applications if needed
    const appsToRender = []
    appsToRender.push(allApps[`uclroombuddy`])
    appsToRender.push(allApps[`uclassistant`])

    this.state = {
      'featuredApps': featuredApps,
      'appsToRender': appsToRender,
    }
  }

  render() {
    const iconsize = `100px`
    const { appsToRender, featuredApps } = this.state

    return (
      <>

        <NavBar isScroll={false} />

        <Row height='300px' style={{ margin: `60px 0 0 0` }} styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
            <TextView text={`UCL Marketplace`} heading={1} align={`center`} />
            <TextView text={`Apps that use UCL API`} heading={2} align={`center`} />
          </Column>
        </Row>

        <Row styling='secondary'>
          <Column width='2-3' horizontalAlignment='center'>
            <TextView text={`Featured App`} heading={2} align={`left`} />
            <TextView text={`Our favourite usage of the API`} heading={5} align={`left`} />
            {featuredApps.map((app, i) => {
              return (
                <CardView key={`featured-app-` + i} width={`1-1`} type={`emphasis`} link={`/marketplace/` + app.id}
                  style={{ 'padding': `20px 0 ` }}
                >
                  <Column width='1-2' horizontalAlignment='center'>
                    <ImageView src={app.logo} width={iconsize} height={iconsize} />
                    <TextView text={app.name} heading={2} align={`center`} color={`white`} />
                    <TextView text={app.description} heading={5} align={`center`} color={`white`} />
                  </Column>
                </CardView>
              )
            })}
          </Column>
        </Row>

        <Row styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center'>
            <TextView text={`All Apps`} heading={2} align={`left`} />
            <TextView text={`Every app made using the API`} heading={5} align={`left`} />
            {appsToRender.map((app, i) => (
              <CardView key={`all-apps-` + i} width={`1-2`} type={`alternate`} link={`/marketplace/` + app.id}
                style={{ 'padding': `20px 0 ` }}
              >
                <Column width='9-10' horizontalAlignment='center'>
                  <ImageView src={app.logo} width={iconsize} height={iconsize} />
                  <TextView text={app.name} heading={2} align={`center`} color={`black`} />
                  <TextView text={app.description} heading={5} align={`center`} color={`black`} />
                </Column>
              </CardView>
            ))}
          </Column>
        </Row>

        <Footer />

      </>
    )
  }
}

class AppPage extends React.Component {
  static propTypes = {
    appId: PropTypes.string.isRequired,
  }

  constructor(props) {
    super(props)


    const { appId } = this.props

    // Grab the app that this page is dealing with
    const app = allApps[appId]
    this.state = {
      'app': app,
    }
  }

  render() {
    const {
      app: {
        name,
        logo,
        description,
        screenshots,
        detailedDescription,
        androidLink,
      },
    } = this.state
    const iconsize = `100px`

    const screenshotwidth = `216px`
    const screenshotheight = `384px`

    return (
      <>
        <NavBar isScroll={false} />

        <Row height='300px' style={{ margin: `60px 0 0 0` }} styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
            <TextView text={`UCL Marketplace`} heading={1} align={`center`} />
            <TextView text={`Apps that use UCL API`} heading={2} align={`center`} />
          </Column>
        </Row>

        <Row styling='secondary' height='100px' noPadding>
          <Column width='2-3' horizontalAlignment='center'>
            <Column width='fit-content' minWidth={iconsize} typeOfInline='grid' horizontalAlignment='left'>
              <ButtonView src={arrow} width={iconsize} height={iconsize} isCircular isInline='block'
                buttonType='image' text='back-to-marketplace' link='/marketplace' margin='0'
              />
            </Column>
          </Column>
        </Row>

        <Row styling='secondary' height='100px' noPadding>
          <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
            <Column width='fit-content' minWidth={iconsize} typeOfInline='grid' horizontalAlignment='left'>
              <ImageView src={logo} width={iconsize} height={iconsize}
                description={name + `logo`} centred style={{ 'margin': `0 auto 0 0` }}
              />
            </Column>
            <Column width='fit-content' minWidth={iconsize} typeOfInline='grid' horizontalAlignment='left' textAlign='left'>
              <TextView text={name} heading={2} />
              <TextView text={description} heading={5} />
            </Column>
          </Column>
        </Row>
        <Row styling='secondary'>
          <Column width='2-3' horizontalAlignment='center'>
            {screenshots.map((img, i) => (
              <CardView width='1-3' minWidth={screenshotwidth} type='no-bg' key={`${name} screenshot number ${i}`}>
                <ImageView src={img} width={screenshotwidth} height={screenshotheight}
                  description={name + ` screenshot number ` + i} centred
                />
              </CardView>
            ))}
          </Column>
        </Row>
        <Row styling='secondary'>
          <Column width='2-3' horizontalAlignment='center' textAlign='left'>
            {detailedDescription}
          </Column>
        </Row>
        <Row styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center'>
            <CardView width={`1-2`} minWidth={`300px`} link={androidLink}>
              <Row height='75px'>
                <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
                  <TextView text='Download Link' heading={2} align={`center`} />
                </Column>
              </Row>
            </CardView>
          </Column>
        </Row>

        <Footer />

      </>
    )
  }

}



class Main extends React.Component {
  static propTypes = {
    match: PropTypes.shape({
      params: PropTypes.shape({
        appId: PropTypes.string.isRequired,
      }),
    }),
  }
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
