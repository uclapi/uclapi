import React from 'react';

import Navbar from './Navbar.jsx';
import Intro from './Intro.jsx';
import Tagline from './Tagline.jsx';
import Goal from './Goal.jsx';
import Demo from './Demo.jsx';
import Examples from './Examples.jsx';
import Hackathon from './Hackathon.jsx';
import Footer from './Footer.jsx';


export default class GetStartedComponent extends React.Component {

    render () {
      return (
        <div>
          <Navbar />
          <Intro />
          <Tagline />
          <Goal />
          <Demo />
          <Examples />
          <Hackathon />
          <Footer />
        </div>
      )
    }

}
