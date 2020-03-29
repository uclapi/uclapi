import 'Styles/documentation.scss'

import {
  cyan,
  grey,
  pink,
} from '@material-ui/core/colors'
import {
  createMuiTheme, MuiThemeProvider, StylesProvider,
} from '@material-ui/core/styles'
import React from 'react'
import ReactDOM from 'react-dom'

import DocumentationComponent from
  '../components/documentation/Documentation.jsx'



const {
  500: cyan500,
} = cyan
const {
  A200: pinkA200,
} = pink
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
      <StylesProvider injectFirst>
        <MuiThemeProvider theme={muiTheme}>
          <DocumentationComponent />
        </MuiThemeProvider>
      </StylesProvider>
    )
  }

}

ReactDOM.render(
  <Documentation />,
  document.querySelector(`.app`)
)
