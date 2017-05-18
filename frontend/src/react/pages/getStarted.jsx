import React from 'react';
import ReactDOM from 'react-dom';
import Layout from '../components/layout.jsx';

import injectTapEventPlugin from 'react-tap-event-plugin';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import GetStartedComponent from '../components/getStarted/getStarted.jsx';


// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

class GetStarted extends React.Component {

  render () {
    return (
      <MuiThemeProvider>
        <GetStartedComponent />
      </MuiThemeProvider>
    )
  }

}

ReactDOM.render(
  <GetStarted />,
  document.querySelector('.app')
);
