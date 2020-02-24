import 'whatwg-fetch'

import {
  grey,
  pink,
} from '@material-ui/core/colors'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import React from 'react'

const {
  100: grey100,
} = grey
const {
  A200: pinkA200,
} = pink
const white = `#ffffff`

const muiTheme = createMuiTheme({
  fontFamily: `Roboto, sans-serif`,
  palette: {
    primary1Color: `#434343`,
    primary3Color: grey100,
    accent1Color: pinkA200,
    textColor: white,
    alternateTextColor: white,
    canvasColor: `#434343`,
  },
})

// Required components
import rooms from 'Layout/data/room_names.jsx'
import {
  AutoCompleteView, CodeView, Column, Row, TextView,
} from 'Layout/Items.jsx'

export default class Demo extends React.Component {
  constructor(props) {
    super(props)

    const rootURL = (
      location.protocol
      + `//` + location.hostname
      + (location.port ? `:` + location.port : ``)
    )
    const now = new Date()

    this.DEBUGGING = false

    this.state = {
      response: ``,
      params: {
        'token': window.initialData.temp_token,
        'date': now.toISOString().substring(0, 10).replace(/-/g, ``),
        'results_per_page': `1`,
      },
      rootURL,
    }
  }

  render() {
    const {
      rootURL,
      params,
      response,
    } = this.state
    return (
      <MuiThemeProvider theme={muiTheme}>
        <Row styling={`secondary`} height={`fit-content`} isPaddedBottom>
          <Column width='2-3' horizontalAlignment='center'>
            <TextView text={`Try out the API`} heading={1} align={`center`} />
            <AutoCompleteView suggestions={rooms} onSubmit={this.makeRequest} />
          </Column>

          <Row height='20px' noPadding />

          <Column width='2-3' horizontalAlignment='center'>
            <CodeView
              url={`${rootURL}/roombookings/bookings`}
              params={params}
              type={`request`}
            />
          </Column>

          {response ? (
            <Column width='2-3' horizontalAlignment='center'>
              <CodeView response={response} type={`response`} />
            </Column>
          ) : null}
        </Row>
      </MuiThemeProvider>
    )
  }

  makeRequest = (roomName) => {
    const now = new Date()
    const { rootURL } = this.state

    if (this.DEBUGGING) {
      console.log(`DEBUG: Looking for room bookings in the room: ` + roomName)
    }

    this.setState({
      params: {
        'token': window.initialData.temp_token,
        'date': now.toISOString().substring(0, 10).replace(/-/g, ``),
        'results_per_page': `1`,
        'roomName': roomName,
      },
    })

    // TODO:
    // Need to create development environment in package.json
    const url = `${rootURL}/roombookings/bookings?token=` + window.initialData.temp_token
      + `&roomname=` + roomName + `&date=` + now.toISOString().substring(0, 10).replace(/-/g, ``)

    fetch(url).then(response => {
      return response.json()
    }).then((data) => {
      this.setState({
        response: JSON.stringify(data, null, 4),
      })
    })
  }

}
