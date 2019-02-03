import React from 'react';
import logo from './../../images/simpleAPILogoWhite.svg';

class NavbarConsistent extends React.Component {
  render () {
    return <div className="navbarconsistent centered">
      <a href={"/dashboard/"}>
      	<img src={logo}/>
      </a>
      <div className="logoTextWhite"><div>UCL API</div></div>
    </div>;
  }
}

export default NavbarConsistent;
