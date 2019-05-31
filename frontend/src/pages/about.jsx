import React from 'react';
import ReactDOM from 'react-dom';

import Navbar from '../components/about/Navbar.jsx';
import Wil from '../components/about/Wil.jsx';
import PersonContainer from '../components/about/PersonContainer.jsx';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import './../sass/about.scss';

 export default class AboutComponent extends React.Component {

   render () {
    return (
      <MuiThemeProvider>
        <Navbar />
        <Wil />
        <PersonContainer />
      </MuiThemeProvider>
    )
  }

 }

ReactDOM.render(
  <AboutComponent />,
  document.querySelector('.app')
);