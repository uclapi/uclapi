// Standard React importss
import React from 'react';
import ReactDOM from 'react-dom';

// Styles
import './../sass/common/uclapi.scss';

// Common Components
import { RelativeLayout, Column, TextView, ButtonView } from 'Layout/Items.jsx';

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

      <RelativeLayout height = "600px" src = "splash_screen.png">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"UCL API"} heading={1} />
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} heading={2} />
          <ButtonView inline={true} text={"DASHBOARD"} link={"/dashboard"}/>
          <ButtonView inline={true} text={"DOCS"} link={"/docs"} buttonType={"alternate"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Our Goal"} heading={1} />
          <TextView text={"Create a ridiculously simple, documentation first, and comprehensive API around UCL's digital services and establish an ecosystem of third party UCL apps and services that use the API."} heading={2} />
          <TextView text={"The UCL API Roadmap is public. Check it out and vote ✅"} heading = {2} link = {"https://trello.com/b/mimLkk3c/ucl-api-roadmap"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="ucl-green">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Get Started using our APIs"} heading={1} />
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Check out our blog for tutorials"} heading={1} />
          <TextView text={"UCL API is a student-built platform for student developers to improve the student experience of everyone at UCL."} heading={2} />
          {this.state.articles.map(item => ( <TextView text={item.title} heading = {2} link = {item.url} /> ) ) }
        </Column>
      </RelativeLayout>

      <RelativeLayout src="market.svg" height="600px" img_size="auto 100%" color="ucl-green">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"Marketplace"} heading={1} />
          <TextView text={"Check out the UCL Marketplace to find apps built using UCL API"} heading={2} />
          <ButtonView inline={true} text={"UCL MARKETPLACE"} link={"/marketplace"} buttonType={"alternate"}/>
        </Column>
      </RelativeLayout>

      <RelativeLayout isPadded = {true} color="dark-grey">         
        <Column width="800px" isCentered={true} isJustifiedText={true}>
          <TextView text={"We're open source and proud!"} heading={1} />
          <TextView text={"Check out our fleshy internals on Github!"} heading={2} />
          <TextView text={"You know you want to!"} heading = {2} link = {"https://github.com/uclapi/uclapi"} />
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
