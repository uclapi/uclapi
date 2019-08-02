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
import market from 'Images/marketplace/marketplace.png';
import logo from 'Images/home-page/logo.svg';

// Common Components
import { RelativeLayout, Column, TextView, ButtonView, CardView, ImageView } from 'Layout/Items.jsx';

// Application config
const allApps = {
  "uclroombuddy": {
    "name": "UCL Room Buddy", "id": "uclroombuddy", "category": "roombookings", "description": "Find the closest free room at UCL", "logo": roombuddylogo,
    "detailedDescription": `
      <p>Finding a place to get your work done can be hard. Every place you've thought of is somehow already filled up; the libraries, the study pods, the benches outside the Print Room Café...
      <br/> <br/>
      Room Buddy makes use of UCL API to find and direct you to open study spaces that aren't widely known. These rooms are scarcely booked up for timetables and sit waiting for you to grace them with your glory.
      <br/> <br/>
      It's simple: install the app, sign in with your UCL ID, and get going to the closest available space to your current location!
      <br/> <br/>
      UCL Room Buddy was built with the UCL API, which gives student developers programmatic access to UCL's data in order to improve the UCL experience for everyone. Learn more at https://uclapi.com
      <br/> <br/>
      Want to contribute to room buddy? Submit a pull request: <a href="https://github.com/uclapi/room-buddy">https://github.com/uclapi/room-buddy</a> </p>)`,
    "developerContact": "https://github.com/wilhelmklopp",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclroombuddy",
    "screenshots": [
      roombuddy_screenshot1,
      roombuddy_screenshot2,
      roombuddy_screenshot3
    ]
  },
  "uclassistant": {
    "name": "UCL Assistant", "id": "uclassistant", "category": "productivity", "description": "An app to manage your student life at UCL", "logo": uclassistantlogo,
    "detailedDescription": `
                           `,
    "developerContact": "https://github.com/uclapi",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclassistant&hl=en_GB",
    "screenshots": [
      uclassistant_screenshot1,
      uclassistant_screenshot2,
      uclassistant_screenshot3
    ]
  },
}

let categories = {
  "roombookings": {
    name: "Room Bookings",
    description: "Apps to deal with rooms at UCL",
    color: "#80D8FF",
    apps: []
  },
  "productivity": {
    name: "Productivity",
    description: "Apps for productivity",
    color: "#FF9800",
    apps: []
  },
};

let allAppsValues = Object.values(allApps);

for (let i=0; i<allAppsValues.length; i++) {
  if (categories[allAppsValues[i].category]) {
    categories[allAppsValues[i].category].apps.push(allAppsValues[i])
  }
  else {
    console.log(allApps[i].category, categories[allApps[i].category]);
  }
}

categories = Object.values(categories);

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
          <RelativeLayout src={market} height="600px" color="market-green" img_size="auto 60%">         
            <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
              <TextView text={"Apps to improve student life at UCL"} heading={2} align={"center"}/>
            </Column>
          </RelativeLayout>

          <RelativeLayout isPadded={true} color="dark-grey">         
            <Column style="2-3" isCentered={true} isCenteredText={true}>
               { this.state.featuredApps.map((app) => {
                  return (
                    <CardView width={"100%"} minWidth={"250px"} isCenteredText={true} padding={"50px 0"} link={"/marketplace/" + app.id} margin={"0"} 
                      cardType={"alternate"} padding={"50px 0"}>
                      <Column style="1-2" isCentered={true}>
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"black"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"black"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>
          </RelativeLayout>
          <RelativeLayout isPaddedBottom={true} color="dark-grey">         
            <Column style="2-3" isCentered={true} isCenteredText={true}>
               { this.state.appsToRender.map((app) => {
                  return (
                    <CardView width={"47%"} minWidth={"250px"} link={"/marketplace/" + app.id} cardType={"alternate"} padding={"50px 0"}>
                      <Column style="9-10" isCentered={true}>
                        <ImageView src={app.logo} width={iconsize} height={iconsize} />
                        <TextView text={app.name} heading={2} align={"center"} color={"black"}/>
                        <TextView text={app.description} heading={5} align={"center"} color={"black"}/>
                      </Column>
                    </CardView>
                  );
               })}
            </Column>
          </RelativeLayout>

          <RelativeLayout isPadded = {true} src={balloons}>         
            <Column style="1-3" isCentered={true} isCenteredText={true}>
                <TextView text={"UCL API 2019"} heading={1} align={"center"}/>

                <TextView text={"github "} heading={5} align={"center"} isInline={true} link={"https://github.com/uclapi/uclapi"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true} />
                <TextView text={" twitter"} heading={5} align={"center"} isInline={true} link={"https://twitter.com/uclapi?lang=en"}/>
                <TextView text={`-`} heading={5} align={"center"} isInline={true}/>
                <TextView text={" facebook"} heading={5} align={"center"} isInline={true} link={"https://www.facebook.com/uclapi/"}/>

                <ImageView src={logo} width={logosize} height={logosize} description={"ucl api logo"} isCentered={true} />
            </Column>
          </RelativeLayout>
        </div>
      );
    }
}

class AppPage extends React.Component {
  render () {
    return (
      <div className="app-page-container">

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
