// Standard React importss
import React from 'react';
import ReactDOM from 'react-dom';

// Styles
import './../sass/common/uclapi.scss';

// Common Components
import { RelativeLayout, Column, TextView, ButtonView, CardView, ImageView } from 'Layout/Items.jsx';

let endpoints = [
  { name: "/oauth", description: "Let your users sign in with their UCL credentials", link: "/docs#oauth" },
  { name: "/roombookings", description: "Get details of all bookable rooms at UCL", link: "/docs#roombookings"},
  { name: "/search", description: "Find people at UCL", link: "/docs#search"},
  { name: "/timetable", description: "Access personal and module timetables", link: "/docs#timetable"},
  { name: "/resources", description: "Find out how many UCL desktops are free", link: "/docs#resources"},
  { name: "/workspaces", description: "See how busy the libraries are right now", link: "/docs#workspaces"}
];

class HomePage extends React.Component {

  constructor (props) {
    super(props);
    this.state = {
      articles: window.initialData.medium_articles,
      host: window.location.hostname
    };
  }

  render () {
    var iconSize = "150px";

    return (
      <div className="landing-page-container">

      {this.state.host == "staging.ninja" && (
        <RelativeLayout isPadded = {true} color="warning-red">         
          <Column style="9-10" isCentered={true} >
            <TextView align={"center"} text={"Warning! This is our bleeding-edge staging environment, and therefore performance, accuracy and reliability of the API cannot be guaranteed. For our stable, supported API please go to:"} heading={1} />
            <TextView align={"center"} text={"uclapi.com"} heading = {2} link = {"https://uclapi.com"}/>
          </Column>
        </RelativeLayout>
      )}

      <RelativeLayout height = "600px" src="home-page/splash_screen.png">         
        <Column style="9-10" isCentered={true} isVerticalAlign={true} isCenteredText={true}>
          <TextView text={"UCL API"} heading={1} align={"center"}/>
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} heading={2} align={"center"}/>
          <ButtonView inline={true} text={"DASHBOARD"} link={"/dashboard"}/>
          <ButtonView inline={true} text={"DOCS"} link={"/docs"} buttonType={"alternate"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column style="9-10" isCentered={true} >
          <TextView text={"Our Goals"} heading={1} align={"center"}/>
        </Column>
      </RelativeLayout>
      <RelativeLayout isPaddedBottom = {true} color="dark-grey">         
        <Column style="2-3" isCentered={true} isCenteredText={true}>
         <Column style="1-3" isInline={true} minWidth={"280px"}>
          <TextView text={"Simple Interfaces"} heading={2} align={"center"}/>
          <TextView text={"The endpoints are streamlined to enable any developer to easily pick up and use the api. We hope that developers of all ability"
                         +" find our endpoints and website easy to navigate. We do not want to overcomplicate the process of developing"
                         +" awesome apps, we want to be the easiest part of your development process!"} align={"justify"} heading={5} />
          <ImageView src={"home-page/heart.svg"} width={iconSize} height={iconSize} description={"an icon of a love heart"} isCentered={true} />
         </Column>
         <Column style="1-3" isInline={true} minWidth={"280px"}>
          <TextView text={"Documentation first"} heading={2} align={"center"}/>
          <TextView text={"As developers we feel the pain of bad documentation: this is why we are driven by good documentation. We want you"
                         +" to spend less time worrying about how to use our api and more time thinking about how to revolutionise the student experience."
                         +" With good documentation we allow you to focus on building helpful applications."} align={"justify"} heading={5} />
          <ImageView src={"home-page/docs.svg"} width={iconSize} height={iconSize} description={"an icon of a clipboard"} isCentered={true} />
         </Column>
         <Column style="1-3" isInline={true} minWidth={"280px"}>
          <TextView text={"Enable developers"} heading={2} align={"center"}/>
          <TextView text={"We want the api to be so comprehensive that any idea, no matter how big, can be created in order to improve students lives. We are always"
                         +" open to suggestions for new endpoints and functionality so we can enable a greater range of applications to be developed. We"
                         +" cannot wait to see what you will develop!"} align={"justify"} heading={5}/>
          <ImageView src={"home-page/heart.svg"} width={iconSize} height={iconSize} description={"an icon of a star"} isCentered={true} />
         </Column>
        </Column>
      </RelativeLayout>
      <RelativeLayout isPaddedBottom = {true} color="dark-grey">         
        <Column style="9-10" isCentered={true} >
          <TextView align={"center"} text={"The UCL API Roadmap is public. Check it out and vote ✅"} align={"center"} heading = {3} link = {"https://trello.com/b/mimLkk3c/ucl-api-roadmap"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="ucl-orange">         
        <Column style="9-10" isCentered={true} >
          <TextView text={"Get Started using our APIs"} heading={1} align={"center"}/>
        </Column>
      </RelativeLayout>
      <RelativeLayout isPaddedBottom = {true} color="ucl-orange">
        <Column style="1300px" widthOverride="auto" isCentered={true} isCenteredText={true}>
          {endpoints.map(x => (
            <CardView  width={"30%"} minWidth={"400px"} link={x.link}>
              <Column style="9-10" isCentered={true}>
                <TextView text={x.name} heading={1} align={"center"}/>
                <TextView text={x.description} heading={3} align={"center"}/>
              </Column>
            </CardView> ) ) }
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column style="9-10" isCentered={true} >
          <TextView text={"Check out our blog for tutorials"} heading={1} align={"center"}/>
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} align={"center"} heading={3} />
          {this.state.articles.map(x => ( <TextView text={x.title} align={"center"} heading = {3} link = {x.url} /> ) ) }
        </Column>
      </RelativeLayout>

      <RelativeLayout src="home-page/market.svg" height="600px" img_size="auto 100%" color="ucl-orange">         
        <Column style="9-10" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
          <TextView text={"UCL Marketplace"} heading={1} align={"center"}/>
          <TextView text={"Check out the UCL Marketplace to find apps built using UCL API"} heading={2} align={"center"}/>
          <ButtonView inline={true} text={"UCL MARKETPLACE"} link={"/marketplace"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column style="9-10" isCentered={true} >
          <TextView text={"We're open source and proud!"} heading={1} align={"center"}/>
          <TextView text={"Check out our fleshy internals on Github!"} heading={3} align={"center"}/>
          <TextView text={"You know you want to!"} heading = {3} link = {"https://github.com/uclapi/uclapi"} align={"center"}/>
        </Column>
      </RelativeLayout>

      </div>
    );
  }

}

ReactDOM.render(
  <HomePage />,
  document.querySelector('.app')
);
