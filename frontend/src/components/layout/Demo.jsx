import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';
import RaisedButton from 'material-ui/RaisedButton';
import 'whatwg-fetch';

import {cyan500, cyan700,
  pinkA200,
  grey100, grey300, grey400, grey500,
  white, darkBlack, fullBlack,
} from 'material-ui/styles/colors';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

const muiTheme = getMuiTheme({
  fontFamily: 'Roboto, sans-serif',
  palette: {
    primary1Color: "#434343",
    primary3Color: grey100,
    accent1Color: pinkA200,
    textColor: white,
    alternateTextColor: white,
    canvasColor: "#434343",
  },
});

// Required components
import rooms from 'Layout/data/room_names.jsx';
import {Column, Row, TextView, CodeView, CardView, AutoCompleteView} from 'Layout/Items.jsx';

export default class Demo extends React.Component {
  constructor(props) {
    super(props);

    let rootURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    let now = new Date();

    this.DEBUGGING = true;

    this.state = {
      response: "",
      params: {
        "token": window.initialData.temp_token,
        "date": now.toISOString().substring(0, 10).replace(/-/g, ""),
        "results_per_page": "1"
      },
      rootURL: rootURL,
    };

    this.makeRequest = this.makeRequest.bind(this);
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Row color={"secondary"} height={"fit-content"} isPaddedBottom={true}>
          <Column width="2-3" horizontalAlignment="center">
            <TextView text={"Try out the API"} heading={1} align={"center"} />
            <AutoCompleteView suggestions={rooms} onSubmit={this.makeRequest}/>
          </Column>
          
          <Row height="20px" noPadding/>

          <Column width="2-3" horizontalAlignment="center">
            <CodeView url={`${this.state.rootURL}/roombookings/bookings`} params={this.state.params} type={"request"}/>
          </Column>

          {this.state.response ? (
            <div className="demo-response">
              <Column width="2-3" horizontalAlignment="center">
                <TextView text={"The response from the API:"} heading={3} align={"left"}/>
              </Column>
              <Column width="2-3" horizontalAlignment="center">
                <CodeView response={this.state.response} type={"real-response"}/>
              </Column>
            </div>
          ) : null }
        </Row>
      </MuiThemeProvider>
    );
  }

  makeRequest(roomName) {
    let now = new Date();

    if(this.DEBUGGING) { console.log("DEBUG: Looking for room bookings in the room: " + roomName)}

    this.setState({
      params: {
        "token": window.initialData.temp_token,
        "date": now.toISOString().substring(0, 10).replace(/-/g, ""),
        "results_per_page": "1",
        "roomName": roomName
      }
    });

    // TODO:
    // Need to create development environment in package.json
    let url = `${this.state.rootURL}/roombookings/bookings?token=` + window.initialData.temp_token 
      + "&roomname=" + roomName + "&date=" + now.toISOString().substring(0, 10).replace(/-/g, "");

    fetch(url).then(response => {
      return response.json();
    }).then((data) => {
      this.setState({
        response: JSON.stringify(data, null, 4)
      });
    });
  }

}
