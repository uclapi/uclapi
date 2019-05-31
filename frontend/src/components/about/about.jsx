import React from 'react';

import Navbar from './Navbar.jsx';
import Wil from './Wil.jsx';
import PersonContainer from './PersonContainer.jsx';


export default class AboutComponent extends React.Component {

  render () {
    return (
      <div>
        <Navbar />
        <Wil />
        <PersonContainer />
      </div>
    )
  }

}
