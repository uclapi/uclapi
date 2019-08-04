// Standard React imports
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

// Styles
import 'Styles/common/uclapi.scss';

// Images
// Room Buddy
import roombuddylogo from 'Images/marketplace/roombuddy/logo.png';
import roombuddy_screenshot1 from 'Images/marketplace/roombuddy/screenshot_1.png';
import roombuddy_screenshot2 from 'Images/marketplace/roombuddy/screenshot_2.png';
import roombuddy_screenshot3 from 'Images/marketplace/roombuddy/screenshot_3.png';
// UCL Assistant
import uclassistantlogo from 'Images/marketplace/uclassistant/logo.png';
import uclassistant_screenshot1 from 'Images/marketplace/uclassistant/screenshot_1.png';
import uclassistant_screenshot2 from 'Images/marketplace/uclassistant/screenshot_2.png';
import uclassistant_screenshot3 from 'Images/marketplace/uclassistant/screenshot_3.png';
// Backgrounds
import balloons from 'Images/home-page/balloons.jpg';
import market from 'Images/marketplace/market.svg';
import logo from 'Images/home-page/logo.svg';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView } from 'Layout/Items.jsx';

// Application config
let roombuddydescription = (
  <div className="roombuddy-full-description" style={ { "display": "inline-block", "padding": "0 6%" } } >
       <TextView heading={"3"} text={"Finding a place to get your work done can be hard. Every place you've thought of"
        + " is somehow already filled up: the libraries, the study pods, the benches outside the Print Room Café..."} />
       <TextView heading={"3"} text={"Room Buddy makes use of UCL API to find and direct you to open study spaces"
        + " that aren't widely known. These rooms are scarcely booked up for timetables and sit waiting for you to" 
        + " grace them with your glory."} />
       <TextView heading={"3"} text={"It's simple: install the app, sign in with your UCL ID, and get going to the"
        + " closest available space to your current location!"} />
       <TextView heading={"3"} text={"UCL Room Buddy was built with the UCL API, which gives student developers"
        + " programmatic access to UCL's data in order to improve the UCL experience for everyone."} />
       <TextView heading={"3"} text={"Want to contribute to room buddy? Submit a pull request:"}/>
       <ButtonView buttonType={"alternate"} text={"VISIT GITHUB"} isCentered={true} link={"https://github.com/uclapi/ucl-assistant-app"} />
       <TextView heading={"3"} text={"This app and its platform have been built by the UCL API Team, a group of students"
        + " working with UCL's Information Services Division (ISD) to provide students with a brand new ecosystem that allows"
        + " anyone within the UCL Community to build apps with UCL data. Interested in building an app just like UCL Room Buddy"
        + " yourself? Head over to uclapi.com and log in with your UCL Account."}/>
  </div>
);

let uclassistantdescription = (
  <div className="uclassistant-full-description" style={ {"display": "inline-block", "padding" : "0 6%" } } >
       <TextView heading={"3"} text={"✨✨A brand new and beautiful app to manage your student life at UCL!✨✨"} />
       <TextView heading={"3"} text={"✅ View your personal timetable and get instant directions to your lectures."} />
       <TextView heading={"3"} text={"✅ Check the availability of all UCL libraries and study spaces, including in"
        + " the new Student Centre. Want to know which floor or room has the most seats free? You now have that"
        + " information right in the palm of your hand! Not sure which seats are free? No problem! Just use the live"
        + " seating maps to see every seat that has been unoccupied for over half an hour on whichever library" 
        + " floor you choose."} />
       <TextView heading={"3"} text={"✅ Search for members of the UCL community, including students and lecturers,"
        + " and tap to email them. Nice and easy!"}/>
       <TextView heading={"3"} text={"✅ Find every centrally bookable room at UCL, see how big it is and whether it is"
        + " currently in use, and then tap to navigate right there."}/>
       <TextView heading={"3"} text={"✅ Made with love 💖 by and for students"}/>
       <TextView heading={"3"} text={"✅ Fully open source. Got feedback, suggestions or even some new code to improve" 
        + " the app? We welcome it:"}/>
       <ButtonView buttonType={"alternate"} isCentered={true} text={"VISIT GITHUB"} link={"https://github.com/uclapi/ucl-assistant-app"} />
       <TextView heading={"3"} text={"This app and its platform have been built by the UCL API Team, a group of students"
        + " working with UCL's Information Services Division (ISD) to provide students with a brand new ecosystem that allows"
        + " anyone within the UCL Community to build apps with UCL data. Interested in building an app just like UCL Assistant"
        + " yourself? Head over to uclapi.com and log in with your UCL Account."}/>
  </div>
);

const allApps = {
  "uclroombuddy": {
    "name": "UCL Room Buddy", "id": "uclroombuddy", "category": "roombookings", "description": "Find the closest free room at UCL", "logo": roombuddylogo,
    "detailedDescription": roombuddydescription, "developerContact": "https://github.com/wilhelmklopp",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclroombuddy",
    "screenshots": [ roombuddy_screenshot1, roombuddy_screenshot2, roombuddy_screenshot3 ]
  },
  "uclassistant": {
    "name": "UCL Assistant", "id": "uclassistant", "category": "productivity", "description": "An app to manage your student life at UCL", "logo": uclassistantlogo,
    "detailedDescription": uclassistantdescription, "developerContact": "https://github.com/uclapi",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclassistant&hl=en_GB",
    "screenshots": [ uclassistant_screenshot1, uclassistant_screenshot2, uclassistant_screenshot3 ]
  },
}

class Marketplace extends React.Component {

  constructor(props) {
    super(props);

    // Set up the 'featured' apps section 
    let featuredApps = [];
    featuredApps.push(allApps['uclroombuddy']);

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
        <div className="marketplace-container">
          <Row src={market} height="600px" color="ucl-orange" img_size="auto 60%">         
            <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
              <TextView text={"Apps to improve student life at UCL"} heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row isPadded={true} color="dark-grey">         
            <Column style="2-3" isCentered={true} isCenteredText={true}>
               <TextView text={"Featured App"} heading={2} align={"left"} />
               <TextView text={"Our favourite usage of the API"} heading={5} align={"left"} />
               { this.state.featuredApps.map((app, i) => {
                  return (
                    <CardView key={"featured-app-"+i} width={"100%"} size={"small"} isCenteredText={true} 
                    padding={"50px 0"} link={"/marketplace/" + app.id} margin={"0"} cardType={"emphasis"} padding={"50px 0"}>
                      <Column style="1-2" isCentered={true}>
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"white"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"white"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">         
            <Column style="2-3" isCentered={true} isCenteredText={true}>
               <TextView text={"All Apps"} heading={2} align={"left"} />
               <TextView text={"Every app made using the API"} heading={5} align={"left"} />
               { this.state.appsToRender.map((app, i) => {
                  var margin = "0";
                  if(i%2 == 0) {margin = "0 2% 0 0"}

                  return (
                    <CardView key={"all-apps-"+i} width={"49%"} size={"small"} link={"/marketplace/" + app.id} cardType={"alternate"} padding={"50px 0"} margin={margin}>
                      <Column style="9-10" isCentered={true}>
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"black"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"black"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>
          </Row>

          <Row isPadded = {true} src={balloons}>         
            <Column style="1-2" isCentered={true} isCenteredText={true}>
                <TextView text={"UCL API"} heading={1} align={"center"}/>

                <TextView text={"github "} heading={5} align={"center"} isInline={true} link={"https://github.com/uclapi/uclapi"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true} />
                <TextView text={" twitter"} heading={5} align={"center"} isInline={true} link={"https://twitter.com/uclapi?lang=en"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true}/>
                <TextView text={" facebook"} heading={5} align={"center"} isInline={true} link={"https://www.facebook.com/uclapi/"}/>

                <ImageView src={logo} width={logosize} height={logosize} description={"ucl api logo"} isCentered={true} />
            </Column>
          </Row>
        </div>
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
      <div className="marketplace-container">
          <Row src={market} height="600px" color="ucl-orange" img_size="auto 60%">         
            <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
              <TextView text={"Apps to improve student life at UCL"} heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row isPadded={true} color="dark-grey" height={"100px"}>         
            <Column style="2-3" isCenteredText={true} isCentered={true}>
              <Column style="1-4" minWidth={iconsize} isInline={"grid"} isCenteredText={true}
                 padding={"2% 0"} position={"relative"} float={"left"}>
                <ImageView src={this.state.app.logo} width={iconsize} height={iconsize} description={this.state.app.name + " logo"} isCentered={true} />
              </Column>
              <Column style="1-4" minWidth={iconsize} isInline={"grid"} isCenteredText={true} 
                padding={"3% 0"} position={"relative"} float={"left"}>
               <TextView text={this.state.app.name} heading={2} align={"left"} />
               <TextView text={this.state.app.description} heading={5} align={"left"} />
              </Column>
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">         
            <Column style="2-3" isCentered={true} isCenteredItems={true}>
              {this.state.app.screenshots.map((img, i) => ( 
                <CardView width={"30%"} minWidth={"small"} cardType={"wrap-around"} height={screenshotheight}>
                  <ImageView src={img} width={screenshotwidth} height={screenshotheight}
                    description={this.state.app.name + " screenshot number " + i} isCentered={true} />
                </CardView>
                ) ) }
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">         
            <Column style="2-3" isCentered={true}>
              {this.state.app.detailedDescription}
              <ButtonView isCentered={true} buttonType={"alternate"} text={"DOWNLOAD LINK"} link={this.state.app.androidLink} />
            </Column>
          </Row>

          <Row isPadded={true} src={balloons}>         
            <Column style="1-2" isCentered={true} isCenteredText={true}>
                <TextView text={"UCL API"} heading={1} align={"center"}/>

                <TextView text={"github "} heading={5} align={"center"} isInline={true} link={"https://github.com/uclapi/uclapi"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true} />
                <TextView text={" twitter"} heading={5} align={"center"} isInline={true} link={"https://twitter.com/uclapi?lang=en"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true}/>
                <TextView text={" facebook"} heading={5} align={"center"} isInline={true} link={"https://www.facebook.com/uclapi/"}/>

                <ImageView src={logo} width={logosize} height={logosize} description={"ucl api logo"} isCentered={true} />
            </Column>
          </Row>
      </div>
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
