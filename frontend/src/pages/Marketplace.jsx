// Standard React imports
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

// Styles
import 'Styles/common/uclapi.scss';

// Legacy
import 'Styles/navbar.scss';

// Images
// Backgrounds
import balloons from 'Images/home-page/balloons.jpg';
import market from 'Images/marketplace/market.svg';
import logo from 'Images/home-page/logo.svg';
import arrow from 'Images/marketplace/arrow-left.svg';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, NavBar, Footer } from 'Layout/Items.jsx';

// Grab titles and descriptions of app
import { allApps } from 'Layout/data/app_pages.jsx';

class Marketplace extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      DEBUGGING: false,
    }

    if(this.state.DEBUGGING) { console.log("All apps loaded in: " + allApps); }

    // Set up the 'featured' apps section 
    let featuredApps = [];
    featuredApps.push(allApps['uclassistant']);

    // Segregate into groups of applications if needed
    let appsToRender = [];
    appsToRender.push(allApps['uclroombuddy']);
    appsToRender.push(allApps['uclassistant']);

    this.state = {
      "featuredApps": featuredApps,
      "appsToRender": appsToRender,
    };
  }

  render () {
      var iconsize = "100px";
      var logosize = "150px";

      return (
        <React.Fragment>

          <NavBar isScroll={"true"} />

          <Row height="600px" color="splash-parallax" img_size="auto 60%">         
            <Column width="2-3" horizontalAlignment="center" verticalAlignment="center">
              <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
              <TextView text={"Apps to improve student life at UCL"} heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row color="secondary">         
            <Column width="2-3" horizontalAlignment="center">
               <TextView text={"Featured App"} heading={2} align={"left"} />
               <TextView text={"Our favourite usage of the API"} heading={5} align={"left"} />
               { this.state.featuredApps.map((app, i) => {
                  return (
                    <CardView key={"featured-app-"+i} width={"1-1"} style={"emphasis"} link={"/marketplace/" + app.id} addPadding={true}>
                      <Column width="1-2" horizontalAlignment="center">
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"white"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"white"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>    
          </Row>

          <Row color="splash-parallax">
            <Column width="2-3" horizontalAlignment="center">
               <TextView text={"All Apps"} heading={2} align={"left"} />
               <TextView text={"Every app made using the API"} heading={5} align={"left"} />
               { this.state.appsToRender.map((app, i) => {
                  var margin = "0";
                  if(i%2 == 0) {margin = "0 2% 0 0"}

                  return (
                    <CardView key={"all-apps-"+i} width={"1-2"} style={"alternate"} link={"/marketplace/" + app.id} addPadding={true}>
                      <Column width="9-10" horizontalAlignment="center">
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"black"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"black"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>
          </Row>
          
          <Footer />

        </React.Fragment>
      );
    }
}

class AppPage extends React.Component {
  constructor(props) {
    super(props);

    // Grab the app that this page is dealing with
    let app = allApps[this.props.appId];
    this.state = {
      "app": app
    };
  }

  render () {
    var iconsize = "100px";
    var logosize = "150px";

    var screenshotwidth = "216px";
    var screenshotheight = "384px";

    return (
      <React.Fragment>
]
          <NavBar isScroll={"true"} />

          <Row src={market} height="600px" color="primary" img_size="auto 60%">         
            <Column width="2-3" horizontalAlignment="center" verticalAlignment="center">
              <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
              <TextView text={"Apps to improve student life at UCL"} heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row color="secondary" height="100px">      
            <Column width="2-3" horizontalAlignment="center">
              <Column width="fit-content" minWidth={iconsize} typeOfInline="grid" horizontalAlignment="left">
                <ButtonView src={arrow} width={iconsize} height={iconsize} isCircular={true} isInline="block" 
                  buttonType="image" text="back-to-marketplace" link="/marketplace" margin="0" />
              </Column>
            </Column>
          </Row>

          <Row color="secondary" height="100px">   
            <Column width="2-3" horizontalAlignment="center" verticalAlignment="center">
              <Column width="fit-content" minWidth={iconsize} typeOfInline="grid" horizontalAlignment="left">
                <ImageView src={this.state.app.logo} width={iconsize} height={iconsize} 
                  description={this.state.app.name  + "logo"} isCentered={true} margin={"0 auto 0 0"}/>
              </Column>
              <Column width="fit-content" minWidth={iconsize} typeOfInline="grid" horizontalAlignment="left">
               <TextView text={this.state.app.name} heading={2} align={"left"} />
               <TextView text={this.state.app.description} heading={5} align={"left"} />
              </Column>
            </Column>
          </Row>
          <Row color="secondary">         
            <Column width="2-3" horizontalAlignment="center">
              {this.state.app.screenshots.map((img, i) => ( 
                <CardView width="fit-content" minWidth="300px" style={"wrap-around"} height={screenshotheight} horizontalAlignment="left">
                  <ImageView src={img} width={screenshotwidth} height={screenshotheight}
                    description={this.state.app.name  + " screenshot number " + i} isCentered={true} />
                </CardView>
                ) ) }
            </Column>
          </Row>
          <Row color="secondary">         
            <Column width="2-3" horizontalAlignment="center">
              {this.state.app.detailedDescription}
              <ButtonView isCentered={true} buttonType={"alternate"} text={"DOWNLOAD LINK"} link={this.state.app.androidLink} />
            </Column>
          </Row>

          <Footer />

      </React.Fragment>
    );
  }

}

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/marketplace' component={Marketplace}/>
      <Route path='/marketplace/:appId' render={(props) => (
        <AppPage appId={props.match.params.appId} />
      )}/>
    </Switch>
  </main>
)

ReactDOM.render(
  <BrowserRouter>
    <Main />
  </BrowserRouter>,
  document.querySelector('#root')
);
