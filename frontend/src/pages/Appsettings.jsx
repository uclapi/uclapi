import React from 'react';
import ReactDOM from 'react-dom';
import Hub from '../components/appsettings/hub.jsx';
import LogInLayout from '../components/appsettings/loginlayout.jsx';
import UserApps from '../components/appsettings/userapps.jsx';
import moment from 'moment';

import {cyan500, cyan700,
  pinkA200,
  grey100, grey300, grey400, grey500,
  white, darkBlack, fullBlack,
} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

const muiTheme = getMuiTheme({
  fontFamily: 'Roboto, sans-serif',
  palette: {
    primary1Color: "#434343",
    primary2Color: "#434343",
    primary3Color: grey400,
    accent1Color: pinkA200,
    accent2Color: grey100,
    accent3Color: grey500,
    textColor: darkBlack,
    alternateTextColor: white,
    canvasColor: white,
    borderColor: grey300,
    pickerHeaderColor: cyan500,
    shadowColor: fullBlack,
  },
});

import './../sass/hub.scss';
import './../sass/navbar.scss';

class AppSettings extends React.Component {
  constructor (props) {
    super(props);
    this.state = {data: window.initialData};
  }
  render () {
    if(this.state.data.status!="ONLINE") {
      return <MuiThemeProvider muiTheme={muiTheme}>
          <Hub>   
            <LogInLayout url={this.state.data.url} />
          </Hub>
        </MuiThemeProvider>;
    } else {
      return <MuiThemeProvider muiTheme={muiTheme}>
        <Hub> 
          <UserApps fullname={this.state.data.fullname} department={this.state.data.department} authorised_apps={this.state.data.apps} />  
        </Hub>
      </MuiThemeProvider>;
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector('.app')
);
