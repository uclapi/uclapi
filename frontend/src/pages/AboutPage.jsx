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
    <CardView width="1-6" minWidth="120px" style="emphasis" link={info.github}>
      <Row>
        <Column width="1-1" horizontalAlignment="center">
          <TextView text={info.name} heading={2} align={"center"} color={"white"}/>
          <Row height = "100px" src={info.image}></Row>
          <Row height = "50px">
            <Column width="1-1" horizontalAlignment="center" verticalAlignment="center">
                <TextView text={info.title} heading={6} align={"center"} color={"white"} />
                <TextView text="Click to find out more" heading={6} align="center" link={info.github} color={"white"} />
            </Column>
          </Row>
        </Column>
      </Row>
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

          <Row height = "600px" color="team-parallax">         
            <Column width="2-3" horizontalAlignment="center" verticalAlignment="center">
              <TextView text={"The Team"} heading={1} align={"center"}/>
              <TextView text={`UCL API is a student led project founded by Wilhelm Klopp that opens up the massive amount of
                              data collected by UCL and allows UCL students and staff access to develop with it.`} 
                              heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row color="secondary">         
            <Column width="9-10" horizontalAlignment="center">
              <TextView text={"Current Team"} heading={1} align={"center"}/>
            </Column>
            <Column width="1-1" horizontalAlignment="center">
              {current.map(x =>  member(x) )}
            </Column>
          </Row>

          <Row color="team-parallax">         
            <Column width="9-10" horizontalAlignment="center">
              <TextView text={"Previous developers"} heading={1} align={"center"}/>
            </Column>
            <Column width="1-1" horizontalAlignment="center">
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
