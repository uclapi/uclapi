import React from 'react';

import AppBar from 'material-ui/AppBar';


const Logo = (
  <img
    src={window.staticURL + 'simpleAPILogoWhite.svg'}
  />
)

const Navbar = () => (
  <AppBar className="navbar" title="UCL API" iconElementLeft={Logo} />
)

export default Navbar;
