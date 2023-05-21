import rooms from './data/room_names.jsx'
import { CardView, Code, Container, Row } from './Items.jsx'
import React from "react";
import { AutoComplete } from 'rsuite';


class Demo extends React.Component {
  constructor(props) {
    super(props);
    const now = new Date();
    this.DEBUGGING = false;
    this.state = {
      response: ``,
      params: {
        token: props.tempToken,
        date: now.toISOString().substring(0, 10).replace(/-/g, ``),
        results_per_page: `1`,
      },
      rootURL: '',
    };
  }

  async componentDidMount() {
    const token = await fetch(`/dashboard/api/temptoken`, {
      headers: { Authorization: process.env.TEMP_TOKEN_SECRET }
    }).then(res => res.json()).then(res => res.token);
    console.log('mount', token)

    this.setState((old) => ({
      params: { ...old.params, token },
      rootURL:
        window.location.protocol +
        "//" +
        window.location.hostname +
        (window.location.port ? ":" + window.location.port : ""),
    }));
  }

  render() {
    const { rootURL, params, response } = this.state;
    return (
      <Container
        styling={`secondary`}
        height={`fit-content`}
        isPaddedBottom
        heading="Try out the API"
      >
        <Row width="2-3" horizontalAlignment="center">
          <AutoComplete
            style={{ width: "100%" }}
            size="lg"
            block
            data={rooms}
            onChange={this.makeRequest}
            placeholder='e.g., Darwin Building B05'
            renderMenuItem={(text) => {
              return (
                <CardView
                  width="1-1"
                  type="emphasis"
                  fakeLink
                  noShadow
                  style={{width: "100%"}}
                >
                  <p style={{margin: `0`,padding: 0,}}>
                    {text}
                  </p>
                </CardView>
              );
            }}
          />
        </Row>

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
    );
  }

  makeRequest = (roomName) => {
    const now = new Date();
    const { rootURL } = this.state;

    if (this.DEBUGGING) {
      console.log(`DEBUG: Looking for room bookings in the room: ` + roomName);
    }

    this.setState(old => ({
      params: {
        ...old.params,
        date: now.toISOString().substring(0, 10).replace(/-/g, ``),
        roomName,
      },
    }));

    // TODO:
    // Need to create development environment in package.json
    const url =
      `${rootURL}/roombookings/bookings?token=` +
      this.state.params.token +
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
