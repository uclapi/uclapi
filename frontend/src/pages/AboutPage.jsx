// Standard React imports
import React from 'react';
import ReactDOM from 'react-dom';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, Demo, NavBar, Footer } from 'Layout/Items.jsx';

// Team descriptions
import { current, previous } from 'Layout/data/team_members.jsx'

// Styles
import 'Styles/common/uclapi.scss';

// Legacy
import 'Styles/navbar.scss';

const member = (info) => (
    <CardView width='1-6' minWidth='120px' type='emphasis' link={info.github}>
      <Row height='300px' style={ { padding : '20px 0' } }>
        <Column width='1-1' horizontalAlignment='center'>
          <TextView text={info.name} heading={2} align={'center'} color={'white'}/>
          <Row height='100px' src={info.image} style={ { backgroundSize : 'Cover'  } }></Row>
          <Row height='30px' style={ { padding : '20px 0' } }>
            <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
                <TextView text={info.title} heading={6} align={'center'} color={'white'} />
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
          <NavBar isScroll={false}/>

          <Row height = '600px' styling='team-parallax'>
            <Column width='2-3' horizontalAlignment='center' verticalAlignment='center'>
              <TextView text={'About Us'} heading={1} align={'center'}/>
              <TextView text={`UCL API is a student led project, founded by Wilhelm Klopp, that opens up the massive amount of
                              data collected by UCL. This allows UCL alumni and staff to develop apps with UCL data.`}
                              heading={2} align={'center'}/>
            </Column>
          </Row>

          <Row styling='secondary'>
            <Column width='9-10' horizontalAlignment='center'>
              <TextView text={'Current Team'} heading={1} align={'center'}/>
            </Column>
            <Column width='1-1' horizontalAlignment='center'>
              {current.map(x =>  member(x) )}
            </Column>
          </Row>

          <Row styling='team-parallax'>
            <Column width='9-10' horizontalAlignment='center'>
              <TextView text={'Previous developers'} heading={1} align={'center'}/>
            </Column>
            <Column width='1-1' horizontalAlignment='center'>
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
