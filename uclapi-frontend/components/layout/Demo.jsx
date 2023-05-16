import {
  grey,
  pink,
} from '@material-ui/core/colors'
import { createTheme, MuiThemeProvider } from '@material-ui/core/styles'
// Required components
import rooms from './data/room_names.jsx'
import { AutoCompleteView, Code, Container, Row } from './Items.jsx'
import React from "react";

const {
  100: grey100,
} = grey
const {
  A200: pinkA200,
} = pink
const white = `#ffffff`

const muiTheme = createTheme({
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

class Demo extends React.Component {
  constructor(props) {
    super(props);
    const now = new Date();
    this.DEBUGGING = false;
    this.state = {
      response: ``,
      params: {
        // 'token': window.initialData.temp_token,
        date: now.toISOString().substring(0, 10).replace(/-/g, ``),
        results_per_page: `1`,
      },
      rootURL: '',
    };
  }

  componentDidMount() {
    this.setState({
      rootURL:
        window.location.protocol +
        "//" +
        window.location.hostname +
        (window.location.port ? ":" + window.location.port : "")
    });
  }

  render() {
    const { rootURL, params, response } = this.state;
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Container
          styling={`secondary`}
          height={`fit-content`}
          isPaddedBottom
          heading="Try out the API"
        >
          <Row width="2-3" horizontalAlignment="center">
            <AutoCompleteView suggestions={rooms} onSubmit={this.makeRequest} />
          </Row>

          <Container height="20px" noPadding />

          <Row width="2-3" horizontalAlignment="center">
            <Code
              url={`${rootURL}/roombookings/bookings`}
              params={params}
              type={`request`}
            />
          </Row>

          {response ? (
            <Row width="2-3" horizontalAlignment="center">
              <Code response={response} type={`response`} />
            </Row>
          ) : null}
        </Container>
      </MuiThemeProvider>
    );
  }

  makeRequest = (roomName) => {
    const now = new Date();
    const { rootURL } = this.state;

    if (this.DEBUGGING) {
      console.log(`DEBUG: Looking for room bookings in the room: ` + roomName);
    }

    this.setState({
      params: {
        token: window.initialData.temp_token,
        date: now.toISOString().substring(0, 10).replace(/-/g, ``),
        results_per_page: `1`,
        roomName: roomName,
      },
    });

    // TODO:
    // Need to create development environment in package.json
    const url =
      `${rootURL}/roombookings/bookings?token=` +
      window.initialData.temp_token +
      `&roomname=` +
      roomName +
      `&date=` +
      now.toISOString().substring(0, 10).replace(/-/g, ``);

    fetch(url)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.setState({
          response: JSON.stringify(data, null, 4),
        });
      });
  };
}

export default Demo
