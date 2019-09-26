import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import Autosuggest from 'react-autosuggest';
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
import {Column, Row, TextView, CodeView, CardView} from 'Layout/Items.jsx';

// Teach Autosuggest how to calculate suggestions for any given input value.
const getSuggestions = (value) => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  var suggestions = inputLength === 0 ? [] : rooms.filter(room =>
    room.toLowerCase().slice(0, inputLength) === inputValue
  );

  if(suggestions.length > 10) { suggestions.splice(10); }

  console.log("DEBUG: New suggestions found: " + suggestions);

  return suggestions;
};

// When suggestion is clicked, Autosuggest needs to populate the input
// based on the clicked suggestion. Teach Autosuggest how to calculate the
// input value for every given suggestion.
const getSuggestionValue = suggestion => suggestion.name;

const row_size = 40;
// Use your imagination to render suggestions.
const renderSuggestion = suggestion => (
   <Row color="secondary" height={row_size + "px"} noPadding>         
    <Column width="9-10" horizontalAlignment="center" verticalAlignment="center">
      <CardView width="9-10" style="default-no-shadow" link="no-action">
        <Row height = {(row_size-12) + "px"} noPadding>
          <Column width="1-1" horizontalAlignment="center" verticalAlignment="center">
              <TextView align="center" text={suggestion} heading={6}/>
          </Column>
        </Row>
      </CardView>
    </Column>
  </Row>
);

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
      __value: '',
      __suggestions: [],
      rootURL: rootURL,
      DEBUGGING: true
    };

    this.makeRequest = this.makeRequest.bind(this);
    this.onChange = this.onChange.bind(this);
    this.onSuggestionsFetchRequested = this.onSuggestionsFetchRequested.bind(this);
    this.onSuggestionsClearRequested = this.onSuggestionsClearRequested.bind(this);
  }

  render() {
    const { __value, __suggestions } = this.state;

    // Autosuggest will pass through all these props to the input.
    const inputProps = {
      placeholder: 'Type a room at UCL',
      value: __value,
      onChange: this.onChange
    };

    return (
      <MuiThemeProvider muiTheme={muiTheme}>
        <Row color={"secondary"} height={"fit-content"} isPaddedBottom={true}>
          <Column width="2-3" horizontalAlignment="center">
            <TextView text={"Try out the API"} heading={1} align={"center"} />
            <Autosuggest
              suggestions={__suggestions}
              onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
              
              getSuggestionValue={getSuggestionValue}
              renderSuggestion={renderSuggestion}
              inputProps={inputProps}
            />
          </Column>
          
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

  onChange = (event, { newValue }) => {
    if(this.state.DEBUGGING) { console.log("DEBUG: Autocomplete form changed input to: " + newValue); }

    this.setState({
      __value: newValue
    });
  };

  // Autosuggest will call this function every time you need to update suggestions.
  // You already implemented this logic above, so just use it.
  onSuggestionsFetchRequested = ({ value }) => {
    if(this.state.DEBUGGING) { console.log("DEBUG: Fetch suggestions for value of: " + value); }

    this.setState({
      __suggestions: getSuggestions(value)
    });
  };

  // Autosuggest will call this function every time you need to clear suggestions.
  onSuggestionsClearRequested = () => {
    if(this.state.DEBUGGING) { console.log("DEBUG: Cleared suggestions for Autocomplete"); }

    if(!this.state.DEBUGGING) {
      this.setState({
        __suggestions: []
      });
    }
  };

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

}
