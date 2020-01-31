import {
  cyan500,
  darkBlack, fullBlack,
  grey100, grey300, grey400, grey500,
  pinkA200,
  white,
} from 'material-ui/styles/colors'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import React from 'react'
import ReactDOM from 'react-dom'

import Hub from '../components/appsettings/hub.jsx'
import LogInLayout from '../components/appsettings/loginlayout.jsx'
import UserApps from '../components/appsettings/userapps.jsx'

const muiTheme = getMuiTheme({
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

import 'Styles/hub.scss'
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
      return <MuiThemeProvider muiTheme={muiTheme}>
        <Hub>
          <LogInLayout url={url} />
        </Hub>
      </MuiThemeProvider>
    } else {
      return <MuiThemeProvider muiTheme={muiTheme}>
        <Hub>
          <UserApps
            fullname={fullname}
            department={department}
            authorised_apps={apps}
          />
        </Hub>
      </MuiThemeProvider>
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector(`.app`)
)
