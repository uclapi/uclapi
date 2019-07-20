import React from 'react';
import ReactDOM from 'react-dom';
import {cyan500, cyan700,
  pinkA200,
  grey100, grey300, grey400, grey500,
  white, darkBlack, fullBlack,
} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import GetStartedComponent from '../components/getStarted/getStarted.jsx';

import './../sass/getStarted.scss';
import './../sass/navbar.scss';

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

class GetStarted extends React.Component {

  render () {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <GetStartedComponent />
      </MuiThemeProvider>
    )
  }

}

ReactDOM.render(
  <GetStarted />,
  document.querySelector('.app')
);
