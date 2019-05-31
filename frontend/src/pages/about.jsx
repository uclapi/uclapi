import React from 'react';
import ReactDOM from 'react-dom';

import NavbarConsistent from '../components/appsettings/navbarconsistent.jsx';
import Wil from '../components/about/Wil.jsx';
import PersonContainer from '../components/about/PersonContainer.jsx';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

import { Waypoint } from 'react-waypoint';

import './../sass/about.scss';
import './../sass/hub.scss';

 export default class AboutComponent extends React.Component {

   constructor(props) {
    super(props);

    this.state = {
      h: "500px",
    };

    this.handleScroll = this.handleScroll.bind(this);
   }

   handleScroll() {
    var pos = 500 - window.scrollY;

    if(pos>240 && pos<480) {
      this.setState({
        h: pos + "px",
      });
    } else if(pos>480) {
      this.setState({
        h: "500px",
      });
    } else if(pos<240) {
      this.setState({
        h: "200px",
      });
    }
  };

   componentDidMount() {
    window.addEventListener('scroll', this.handleScroll);
   }

   componentWillUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
   }

   render () {
    console.log("height : " + this.state.h);
    var h = this.state.h;

    return (
      <MuiThemeProvider>
        <NavbarConsistent />
        <Wil h={h}/>
        <PersonContainer />
      </MuiThemeProvider>
    )
  }

 }

ReactDOM.render(
  <AboutComponent />,
  document.querySelector('.app')
);