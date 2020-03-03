import 'Styles/documentation.scss'

import {
  cyan500,
  darkBlack,
  fullBlack,
  grey100,
  grey300,
  grey400,
  grey500,
  pinkA200,
  white,
} from 'material-ui/styles/colors'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import React from 'react'
import ReactDOM from 'react-dom'

import DocumentationComponent from '../components/documentation/Documentation.jsx'

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

class Documentation extends React.Component {

  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <DocumentationComponent />
      </MuiThemeProvider>
    )
  }

}

ReactDOM.render(
  <Documentation />,
  document.querySelector(`.app`)
)
