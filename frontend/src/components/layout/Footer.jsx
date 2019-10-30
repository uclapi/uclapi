import React from 'react';

// UCL API Logo
import logo from 'Images/home-page/logo.svg';
// Social Media
import facebook from 'Images/home-page/facebook.png';
import github from 'Images/home-page/github.png';
import twitter from 'Images/home-page/twitter.png';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, Demo, NavBar } from 'Layout/Items.jsx';

export default class Footer extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var iconsize = '50px';
    var logosize = '20px';

    return (
      <Row color='secondary' padding='20px 0'>
          <Column width='1-2' horizontalAlignment='center'>
              <Column maxWidth='160px' width='1-1' horizontalAlignment='center'>
                <CardView width='1-3' style='github' link='https://github.com/uclapi'>
                  <ImageView src={github} width={logosize} height={logosize} description={'github logo'} isCentered={true} />
                </CardView>

                <CardView width='1-3' style='facebook' link='https://www.facebook.com/uclapi/'>
                  <ImageView src={facebook} width={logosize} height={logosize} description={'facebook logo'} isCentered={true} />
                </CardView>

                <CardView width='1-3' style='twitter' link='https://twitter.com/uclapi'>
                  <ImageView src={twitter} width={logosize} height={logosize} description={'twitter logo'} isCentered={true} />
                </CardView>
              </Column>
          </Column>
      </Row>
    );
  }

}
