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

    constructor(props) {
      super(props)

      this.state = {
        sizing: `default`,
      }
    }

  render() {
    const { sizing } = this.state

    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <DocumentationComponent sizing={sizing} />
      </MuiThemeProvider>
    )
  }

  updateDimensions = () => {
    if (typeof (window) === `undefined`) {
      return null
    }
    const w = window,
      d = document,
      documentElement = d.documentElement,
      body = d.getElementsByTagName(`body`)[0],
      width = w.innerWidth || documentElement.clientWidth || body.clientWidth
    // height = w.innerHeight || documentElement.clientHeight || body.clientHeight

    const mobileCutOff = 700
    const tabletCutOff = 1130

    const { sizing } = this.state

    if (width > tabletCutOff) {
      if (sizing != `default`) { this.setState({ sizing: `default` }) }
    } else if (width > mobileCutOff) {
      if (sizing != `tablet`) { this.setState({ sizing: `tablet` }) }
    } else {
      if (sizing != `mobile`) { this.setState({ sizing: `mobile` }) }
    }

    console.log(sizing)
  }

  UNSAFE_componentWillMount() {
    setTimeout(this.updateDimensions, 50)
  }
  componentDidMount() {
    window.addEventListener(`resize`, this.updateDimensions)
  }
  componentWillUnmount() {
    window.removeEventListener(`resize`, this.updateDimensions)
  }

}

ReactDOM.render(
  <Documentation />,
  document.querySelector(`.app`)
)
