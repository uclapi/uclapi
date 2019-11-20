/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types


// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Standard React imports
import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

// Images
// Backgrounds
// import balloons from 'Images/home-page/balloons.jpg'
// import logo from 'Images/home-page/logo.svg'
// import arrow from 'Images/marketplace/arrow-left.svg'
// import market from 'Images/marketplace/market.svg'
// Grab titles and descriptions of app
import { allApps } from 'Layout/data/app_pages.jsx'
// Common Components
import { ButtonView, CardView, Column, Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

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
            {appsToRender.map((app, i) => {
              // let margin = `0`
              // if (i % 2 == 0) { margin = `0 2% 0 0` }

              return (
                <CardView key={`all-apps-` + i} width={`1-2`} type={`alternate`} link={`/marketplace/` + app.id}
                  style={{ 'padding': `20px 0 ` }}
                >
                  <Column width='9-10' horizontalAlignment='center'>
                    <ImageView src={app.logo} width={iconsize} height={iconsize} />
                    <TextView text={app.name} heading={2} align={`center`} color={`black`} />
                    <TextView text={app.description} heading={5} align={`center`} color={`black`} />
                  </Column>
                </CardView>
              )
            })}
          </Column>
        </Row>

        <Footer />

      </>
    )
  }
}

class AppPage extends React.Component {
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
    const iconsize = `100px`

    const screenshotwidth = `216px`
    const screenshotheight = `384px`

    const {
      app: {
        logo,
        name,
        description,
        screenshots,
        detailedDescription,
        links,
      },
    } = this.state

    return (
      <>
        <NavBar isScroll={false} />

        <Row height='300px' style={{ margin: `60px 0 0 0` }} styling='splash-parallax'>
          <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
            <TextView text={`UCL Marketplace`} heading={1} align={`center`} />
            <TextView text={`Apps that use UCL API`} heading={2} align={`center`} />
          </Column>
        </Row>

        <Row styling='secondary' height='70px' style={{ "padding": `10px 0` }}>
          <Column width='2-3' horizontalAlignment='center'>
            <Column width='fit-content' minWidth={iconsize} typeOfInline='grid' horizontalAlignment='left'>
              <ButtonView type='alternate' text='back' link='/marketplace' 
                style={{ 'float' : 'left', 'margin': '10px 0' }} />
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
            <Column width='fit-content' minWidth={iconsize} horizontalAlignment='left' textAlign='left' style={{ "paddingLeft": `20px` }}>
              <TextView text={name} heading={2} />
              <TextView text={description} heading={5} />
            </Column>
          </Column>
        </Row>
        <Row styling='secondary' style={ { 'padding' : '0' } }>
          <Column width='2-3' horizontalAlignment='center'>
            {screenshots.map((img, i) => (
              <CardView width={'1-'+screenshots.length} minWidth={screenshotwidth} type='no-bg' key={name + ' screenshot number ' + i}>
                <ImageView src={img} width={screenshotwidth} height={screenshotheight}
                  description={name + ' screenshot number ' + i} centred
                />
              </CardView>
            ))}
          </Column>
        </Row>
        <Row styling='secondary' style={ { 'padding' : '0 0 20px 0' } }>
          <Column width='1-2' horizontalAlignment='center' textAlign='left'>
            {detailedDescription}
          </Column>
        </Row>

        {links.length > 0 ? (
          <Row styling='splash-parallax'>
            <Column width='2-3' horizontalAlignment='center'>
              {links.map( (x, key) => (
                <ButtonView text={x.name} link={x.link} 
                  type={key%2==0 ? 'default' : 'alternate'} 
                  key={key} style={{ "marginLeft": `0` }}/>
              ))}
            </Column>
          </Row>
        ) : ( 
          <Row styling='splash-parallax'>
            <Column width='2-3' horizontalAlignment='center'>
              <TextView text='No downloads available' heading={3} align={`center`} style={ { "margin" : "0" } }/>
            </Column>
          </Row>
        )}

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