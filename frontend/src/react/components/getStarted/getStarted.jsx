import React from 'react';

import Navbar from './Navbar.jsx';
import Demo from './Demo.jsx';


export default class GetStartedComponent extends React.Component {

    render () {
      return (
        <div>
          <Navbar />
          <Demo />
        </div>
      )
    }

}
