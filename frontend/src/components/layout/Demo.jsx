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
import {Column, Row, TextView} from 'Layout/Items.jsx';

export default class Demo extends React.Component {

  constructor(props) {
    super(props);
    // let rootURL = 'http://localhost:8000';

    // if (process.env.NODE_ENV === 'production') {
    //   rootURL = 'https://uclapi.com';
    // }

    let rootURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

    this.state = {
      schedule: "",
      roomNameMap: {
        'python': ``,
        'javascript': ``,
        'bash': ``
      },
      rootURL: rootURL
    };

    this.getLanguages = this.getLanguages.bind(this);
    this.getSchedule = this.getSchedule.bind(this);
  }

  getLanguages() {
    let now = new Date();

    return [
      {
        "name": "python",
        "code": `import requests

                params = {
                  "token": "${window.initialData.temp_token}",
                  "results_per_page": 1,
                  "date": ${now.toISOString().substring(0, 10).replace(/-/g, "")}, ${this.state.roomNameMap.python}
                }

                r = requests.get("https://uclapi.com/roombookings/bookings", params=params)
                print(r.json())`
      }, 
      {
        "name": "javascript",
        "code": `const token = "${window.initialData.temp_token}";

                fetch(
                  "https://uclapi.com/roombookings/bookings?token="
                  + token
                  + "&results_per_page=1" ${this.state.roomNameMap.javascript}
                  + "&date=" + "${now.toISOString().substring(0, 10).replace(/-/g, "")}"
                ).then((response) => {
                  return response.json()
                })
                .then((json) => {
                  console.log(json);
                })`
      }, 
      {
        "name": "bash",
        "code": `curl https://uclapi.com/roombookings/bookings \\
                -d token=${window.initialData.temp_token} \\
                -d results_per_page=1 ${this.state.roomNameMap.bash} \\
                -d date='${now.toISOString().substring(0, 10).replace(/-/g, "")}'`
      }
    ]
  }

  getSchedule(roomName) {
    this.state.roomNameMap = {
      'python': `\n  "roomname": "${roomName}",`,
      'javascript': `\n  + "&roomname=${roomName}"`,
      'bash': `\\ \n-d roomname='${roomName}'`
    }

    let now = new Date();

    // TODO:
    // Need to create development environment in package.json
    let url = `${this.state.rootURL}/roombookings/bookings?token=` + window.initialData.temp_token + "&roomname=" + roomName + "&date=" + now.toISOString().substring(0, 10).replace(/-/g, "");

    fetch(url).then(response => {
      return response.json();
    }).then((data) => {
      this.setState({
        schedule: JSON.stringify(data, null, 4)
      });
    })
  }

  render() {
    let response = <div></div>;

    if (this.state.schedule) {
      response = <div>
        <hr/>
        <SyntaxHighlighter language={"javascript"} style={androidstudio}>
          {this.state.schedule}
        </SyntaxHighlighter>
      </div>;
    }

    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Row color={"ucl-orange"} height={"fit-content"} isPaddedBottom={true}>
          <Column style="2-3" isCentered={true} padding={"50px 0"}>
            <TextView text={"Try out the API"} heading={1} align={"center"} />
            <AutoComplete fullWidth={true} floatingLabelText="Room Name" filter={AutoComplete.caseInsensitiveFilter} openOnFocus={true}
             dataSource={rooms} onNewRequest={this.getSchedule}/>
          </Column>

          <Column style={"2-3"} color={"code-grey"} isCentered={true}>
            <Tabs>
              {this.getLanguages().map((language, index) => (
                <Tab key={index} label={language.name}>
                  <div>
                    <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                  </div>
                </Tab>
              ))}
            </Tabs>
            {response}
          </Column>
        </Row>
      </MuiThemeProvider>
    )
  }

}
