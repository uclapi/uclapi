import {
  cyan,
  grey,
  pink,
} from '@material-ui/core/colors'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import React from 'react'
import ReactDOM from 'react-dom'

import { Footer, NavBar } from 'Layout/Items.jsx'

import LogInLayout from '../components/appsettings/LogInLayout.jsx'
import SettingsLayout from '../components/appsettings/SettingsLayout.jsx'

const {
  500: cyan500,
} = cyan
const {
  100: grey100,
  300: grey300,
  400: grey400,
  500: grey500,
  900: darkBlack,
} = grey
const {
  A200: pinkA200,
} = pink
const white = `#ffffff`
const fullBlack = `#000000`

const muiTheme = createMuiTheme({
  fontFamily: `Roboto, sans-serif`,
  palette: {
    primary1Color: `#434343`,
    primary2Color: `#434343`,
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
})

import 'Styles/common/uclapi.scss'
import 'Styles/navbar.scss'

class AppSettings extends React.Component {
  constructor(props) {
    super(props)
    this.state = { data: window.initialData }
  }
  render() {
    const { data: {
      status,
      url,
      fullname,
      department,
      apps,
    } } = this.state
    if (status !== `ONLINE`) {
      return <MuiThemeProvider theme={muiTheme}>
        <NavBar isScroll={false} />
        <LogInLayout url={url} />
        <Footer />
      </MuiThemeProvider>
    } else {
      return <MuiThemeProvider theme={muiTheme}>
        <NavBar isScroll={false} />
        <SettingsLayout
          fullname={fullname}
          department={department}
          authorised_apps={apps}
        />
        <Footer />
      </MuiThemeProvider>
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector(`.app`)
)
