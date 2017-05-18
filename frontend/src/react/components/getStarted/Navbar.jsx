import React from 'react';

import AppBar from 'material-ui/AppBar';


let styles = {
  logo: {
    "height": "45px"
  },
  navbar: {
    "paddingLeft": "100px"
  }
}

const Logo = (
  <img
    style={styles.logo}
    src={window.staticURL + 'simpleAPILogoWhite.svg'}
  />
)

const Navbar = () => (
  <AppBar style={styles.navbar} title="UCL API" iconElementLeft={Logo} />
)

export default Navbar;
