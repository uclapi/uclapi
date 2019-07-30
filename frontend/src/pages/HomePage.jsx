// Standard React importss
import React from 'react';
import ReactDOM from 'react-dom';

// Styles
import './../sass/common/uclapi.scss';

// Common Components
import { RelativeLayout, Column, TextView, ButtonView, CardView } from 'Layout/Items.jsx';

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
    var isStaging = false;

    return (
      <div className="landing-page-container">

      {this.state.host == "staging.ninja" && (
        <RelativeLayout isPadded = {true} color="warning-red">         
          <Column width="800px" isCentered={true} isJustifiedText={true}>
            <TextView text={"Warning! This is our bleeding-edge staging environment, and therefore performance, accuracy and reliability of the API cannot be guaranteed. For our stable, supported API please go to:"} heading={1} />
            <TextView text={"uclapi.com"} heading = {2} link = {"https://uclapi.com"}/>
          </Column>
        </RelativeLayout>
      )}

      <RelativeLayout height = "600px" src="splash_screen.png">         
        <Column width="800px" isCentered={true} isJustifiedText={true} isVerticalAlign={true}>
          <TextView text={"UCL API"} heading={1} />
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} heading={2} />
          <ButtonView inline={true} text={"DASHBOARD"} link={"/dashboard"}/>
          <ButtonView inline={true} text={"DOCS"} link={"/docs"} buttonType={"alternate"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Our Goal"} heading={1} />
          <TextView text={"Create a ridiculously simple, documentation first, and comprehensive API around UCL's digital services and establish an ecosystem of third party UCL apps and services that use the API."} heading={3} />
          <TextView text={"The UCL API Roadmap is public. Check it out and vote ✅"} heading = {3} link = {"https://trello.com/b/mimLkk3c/ucl-api-roadmap"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="ucl-orange">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Get Started using our APIs"} heading={1} />
        </Column>
      </RelativeLayout>
      <RelativeLayout isPaddedBottom = {true} color="ucl-orange">
        <Column width="1300px" widthOverride="auto" isCentered={true} isJustifiedText={true}>
          {endpoints.map(x => (
            <CardView isJustifiedText={true} width={"30%"} minWidth={"400px"} link={x.link}>
              <Column width="90%" isCentered={true} isJustifiedText={true} isRelativeVerticalAlign={true}>
                <TextView text={x.name} heading={1}/>
                <TextView text={x.description} heading={3}/>
              </Column>
            </CardView> ) ) }
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Check out our blog for tutorials"} heading={1} />
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} heading={3} />
          {this.state.articles.map(x => ( <TextView text={x.title} heading = {3} link = {x.url} /> ) ) }
        </Column>
      </RelativeLayout>

      <RelativeLayout src="market.svg" height="600px" img_size="auto 100%" color="ucl-orange">         
        <Column width="800px" isCentered={true} isJustifiedText={true} isVerticalAlign={true}>
          <TextView text={"UCL Marketplace"} heading={1} />
          <TextView text={"Check out the UCL Marketplace to find apps built using UCL API"} heading={2} />
          <ButtonView inline={true} text={"UCL MARKETPLACE"} link={"/marketplace"} buttonType={"alternate"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"We're open source and proud!"} heading={1} />
          <TextView text={"Check out our fleshy internals on Github!"} heading={3} />
          <TextView text={"You know you want to!"} heading = {3} link = {"https://github.com/uclapi/uclapi"} />
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
