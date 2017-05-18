import React from 'react';
import ReactDOM from 'react-dom';

import AppBar from 'material-ui/AppBar';


export default class Navbar extends React.Component {

  render () {
    const Logo = (
      <img
        style={{height:"45px"}}
        src={window.staticURL + 'simpleAPILogoWhite.svg'}
      />
    )

    return (
        <AppBar title="UCL API" iconElementLeft={Logo} />
    )
  }

}
