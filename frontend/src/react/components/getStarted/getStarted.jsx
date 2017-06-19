import React from 'react';

import Navbar from './Navbar.jsx';
import Intro from './Intro.jsx';
import Goal from './Goal.jsx';
import Demo from './Demo.jsx';
import Examples from './Examples.jsx';
import Footer from './Footer.jsx';


export default class GetStartedComponent extends React.Component {

    render () {
      return (
        <div>
          <Navbar />
          <Intro />
          <Goal />
          <Demo />
          <Examples />
          <Footer />
        </div>
      )
    }

}
