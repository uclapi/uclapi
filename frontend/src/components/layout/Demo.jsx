import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import AutoComplete from 'material-ui/AutoComplete';
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
import {Column, Row, TextView, CodeView} from 'Layout/Items.jsx';

export default class Demo extends React.Component {

  constructor(props) {
    super(props);

    let rootURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
    let now = new Date();

    this.state = {
      response: "",
      params: {
        "token": window.initialData.temp_token,
        "date": now.toISOString().substring(0, 10).replace(/-/g, ""),
        "results_per_page": "1"
      },
      rootURL: rootURL
    };

    this.makeRequest = this.makeRequest.bind(this);
  }

  makeRequest(roomName) {
    let now = new Date();

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

  render() {
    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Row color={"ucl-orange"} height={"fit-content"} isPaddedBottom={true}>
          <Column style="2-3" isCentered={true} padding={"0 0 50px 0"}>
            <TextView text={"Try out the API"} heading={1} align={"center"} />
            <AutoComplete fullWidth={true} floatingLabelText="Room Name" filter={AutoComplete.caseInsensitiveFilter} openOnFocus={true}
             dataSource={rooms} onNewRequest={this.makeRequest}/>
          </Column>
          
          <Column style={"2-3"} isCentered={true}>
            <TextView text={"The request being made:"} heading={3} align={"left"}/>
          </Column>
          <Column style={"2-3"} color={"code-grey"} isCentered={true}>
            <CodeView url={`${this.state.rootURL}/roombookings/bookings`} params={this.state.params} type={"request"}/>
          </Column>

          {this.state.response ? (
            <div className="demo-response">
              <Column style={"2-3"} isCentered={true}>
                <TextView text={"The response from the API:"} heading={3} align={"left"}/>
              </Column>
              <Column style={"2-3"} isCentered={true} color={code-grey}>
                <CodeView response={this.state.response} type={"real-response"}/>
              </Column>
            </div>
          ) : (
            <Column style={"2-3"} isCentered={true} padding={"50px 0 0 0"}>
              <TextView text={"select a room above to query for room bookings"} heading={5} align={"center"} fontStyle={"italic"}/>
            </Column>
          )}
        </Row>
      </MuiThemeProvider>
    )
  }

}
