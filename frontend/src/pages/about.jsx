import React from 'react';

import Navbar from '../components/about/Navbar.jsx';
import Wil from '../components/about/Wil.jsx';
import PersonContainer from '../components/about/PersonContainer.jsx';


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