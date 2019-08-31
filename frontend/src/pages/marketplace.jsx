import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import {
  cyan,
  pink,
  grey,
} from '@material-ui/core/colors';
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles'
import MarketplaceComponent from '../components/marketplace/marketplace.jsx';
import AppPageComponent from '../components/marketplace/AppPage/AppPage.jsx';

import './../sass/marketplace.scss';

const {
  500: cyan500,
  700: cyan700
} = cyan
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

class Marketplace extends React.Component {

  render() {
    return (
      <MuiThemeProvider theme={muiTheme}>
        <MarketplaceComponent />
      </MuiThemeProvider>
    )
  }

}

class AppPage extends React.Component {

  render() {
    return (
      <MuiThemeProvider theme={muiTheme}>
        <AppPageComponent {...this.props} />
      </MuiThemeProvider>
    )
  }

}

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/marketplace' component={Marketplace} />
      <Route path='/marketplace/:appId' render={(props) => (
        <AppPage appId={props.match.params.appId} />
      )} />
    </Switch>
  </main>
)

ReactDOM.render(
  <BrowserRouter>
    <Main />
  </BrowserRouter>,
  document.querySelector('#root')
);
