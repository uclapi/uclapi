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

export default class CodeView extends React.Component {
  constructor(props) {
    super(props);

    this.getTextFromParameters = this.getTextFromParameters.bind(this);
    this.getRequest = this.getRequest.bind(this);
    this.getResponse = this.getResponse.bind(this);
  }

  getTextFromParameters() {
    let now = new Date();
    var params = this.props.params;

    // Setup the python code segment
    var python = `import requests\n`+`\n`+`params = {\n`;
    for(var key in params) {
      python += `\t "${key}": "${params[key]}",\n`;
    }
    python += `}\n` + `r = requests.get("${this.props.url}", params=params)\n` + `print(r.json())`;

    // Setup the javascript code segment
    var javascript = `fetch("${this.props.url}?`;
    var isFirst=true;
    for(var key in params) {
      if(isFirst) {javascript += `${key}=${params[key]}`; isFirst=false;}
      else {javascript += `&${key}=${params[key]}`;}
    }
    javascript += `")\n` + `.then((response) => {\n` + `\t return response.json() \n` + `})\n` + `.then((json) => {\n`;
    javascript += `\t console.log(json);\n` + `})`;

    // Setup the shell code segment
    var shell = `curl -G $(this.props.url) \ \n`
    for(var key in params) {
      shell += `\t -d ${key}=${params[key]}\n`;
    }

    return this.getRequest(python, javascript, shell);
  }

  getRequest(python, javascript, shell) {
    return [
      {
        "name" : "python",
        "code" : python
      },
      {
        "name" : "javascript",
        "code" : javascript
      },
      {
        "name" : "shell",
        "code" : shell
      },
    ];
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
    if(this.props.type == "request") {languages = this.getTextFromParameters();}
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