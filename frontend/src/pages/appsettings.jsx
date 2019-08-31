import React from 'react';
import ReactDOM from 'react-dom';
import Hub from '../components/appsettings/hub.jsx';
import LogInLayout from '../components/appsettings/loginlayout.jsx';
import UserApps from '../components/appsettings/userapps.jsx';

import {
  cyan,
  pink,
  grey,
  white,
} from '@material-ui/core/colors';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles'

const { 500: cyan500 } = cyan
const { A200: pinkA200 } = pink
const {
  100: grey100,
  300: grey300,
  400: grey400,
  500: grey500,
  900: darkBlack,
} = grey
const white = `#ffffff`
const fullBlack = `#000000`

const muiTheme = createMuiTheme({
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
  constructor(props) {
    super(props);
    this.state = { data: window.initialData };
  }
  render() {
    const { data: {
      status,
      url,
      fullname,
      department,
      apps
    } } = this.state
    if (status !== "ONLINE") {
      return <MuiThemeProvider theme={muiTheme}>
        <Hub>
          <LogInLayout url={url} />
        </Hub>
      </MuiThemeProvider>;
    } else {
      return <MuiThemeProvider theme={muiTheme}>
        <Hub>
          <UserApps
            fullname={fullname}
            department={department}
            authorised_apps={apps}
          />
        </Hub>
      </MuiThemeProvider>;
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector('.app')
);
