// Standard React imports
import React from 'react';
import ReactDOM from 'react-dom';

import splash_screen from 'Images/team/people.jpg';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, Demo, NavBar, Footer } from 'Layout/Items.jsx';

// Team descriptions
import { current, previous } from 'Layout/data/team_members.jsx'

// Styles
import 'Styles/common/uclapi.scss';

// Legacy
import 'Styles/navbar.scss';

const member = (info) => (
    <CardView width={"1-3"} minWidth={"540px"} style={"alternate"} link={info.github}>
      <Column style="1-1">
        <Row height = "400px" src={info.image}>
          <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={info.name} heading={1} align={"center"}/>
          </Column>
        </Row> 
        <Row height = "140px" color="transparent">
          <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={info.title} heading={6} align={"center"} color={"black"} />
              <TextView text={info.email} heading={6} align={"center"} color={"black"} />
              <TextView text={`${info.startYear} - ${info.endYear}`} heading={6} align={"center"} color={"black"} />
              <TextView text="View GitHub" heading={6} align="center" link={info.github} color={"black"} />
          </Column>
        </Row>
      </Column>
    </CardView>
);

class AboutPage extends React.Component {

  constructor (props) {
    super(props);

    this.state = {
      DEBUGGING: false,
    };
  }

  render () {
      return (
        <React.Fragment>
          <NavBar isScroll={"false"}/>

          <Row height = "600px" src={splash_screen}>         
            <Column style="2-3" isCentered={true} isVerticalAlign={true} isCenteredText={true}>
              <TextView text={"The Team"} heading={1} align={"center"}/>
              <TextView text={`UCL API is a student led project founded by Wilhelm Klopp that opens up the massive amount of
                              data collected by UCL and allows UCL students and staff access to develop with it.`} 
                              heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row isPadded = {true} color="dark-grey">         
            <Column style="9-10" isCentered={true} >
              <TextView text={"Current Team"} heading={1} align={"center"}/>
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">
            <Column style="2-3" widthOverride="auto" isCentered={true} isCenteredText={true}>
              {current.map(x =>  member(x) )}
            </Column>
          </Row>

          <Row isPadded = {true} color="ucl-orange">         
            <Column style="9-10" isCentered={true} >
              <TextView text={"Previous developers"} heading={1} align={"center"}/>
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="ucl-orange">
            <Column style="2-3" widthOverride="auto" isCentered={true} isCenteredText={true}>
              {previous.map(x => member(x) )}
            </Column>
          </Row>

          <Footer />

        </React.Fragment>
      );
  }
}

ReactDOM.render(
  <AboutPage />,
  document.querySelector('.app')
);
