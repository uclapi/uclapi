// Standard React components
import React from 'react'; 

// DEPENDENCIES
import {Tabs, Tab} from 'material-ui/Tabs';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';
import 'whatwg-fetch';

// Material UI Styling
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

// Common Components 
import {Column, TextView} from 'Layout/Items.jsx'

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

export default class CodeView extends React.Component {
  constructor(props) {
    super(props);

    this.getResponse = this.getResponse.bind(this);
  }

  getResponse(response) {
    return [
      {
        "name" : "response",
        "code" : response
      }
    ];
  }

  render() {
    var languages = [];
    if(this.props.type == "request") {languages = RequestGenerator.getRequest(this.props.url, this.props.params, true);}
    if(this.props.type == "real-response") {languages = this.getResponse(this.props.response);}

    return (
      <MuiThemeProvider muiTheme={muiTheme}>
          <Column style={"1-1"} color={"code-grey"}>
            <Tabs>
              {languages.map((language, index) => (
                <Tab key={index} label={language.name}>
                  <div>
                    <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                  </div>
                </Tab>
              ))}
            </Tabs>
          </Column>
      </MuiThemeProvider>
    );
  }

}