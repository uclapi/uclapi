import React from 'react';

import AppBar from 'material-ui/AppBar';
import {getStyles} from 'material-ui/AppBar/AppBar';
import Drawer from 'material-ui/Drawer';
import MenuItem from 'material-ui/MenuItem';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';
import IconButton from 'material-ui/IconButton';
import ActionMenu from 'material-ui/svg-icons/navigation/menu';

import apiLogo from './../../images/simpleAPILogoWhite.svg';


export default class Navbar extends React.Component {

  render() {
    const Logo = (<img src={apiLogo}/>)

    let rightButtons = (
      <div>
        <a href={"/"}>
          <FlatButton label="Home" style={{"color": "white"}}/>
        </a>
        <a href={"/docs/"}>
          <FlatButton label="Documentation" style={{"color": "white"}}/>
        </a>
      </div>
    )

    return (<AppBar className="navbar" title="UCL API" iconElementLeft={Logo} iconElementRight={rightButtons}/>);
  }

}
