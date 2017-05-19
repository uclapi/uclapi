import React from 'react';

import Navbar from './Navbar.jsx';
import Jumbotron from './Jumbotron.jsx';
import Demo from './Demo.jsx';
import Examples from './Examples.jsx';


export default class GetStartedComponent extends React.Component {

    render () {
      return (
        <div>
          <Navbar />
          <Jumbotron />
          <Demo />
          <Examples />
        </div>
      )
    }

}
