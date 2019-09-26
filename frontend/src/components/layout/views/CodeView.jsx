// Standard React components
import React from 'react'; 

// DEPENDENCIES
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';
import 'whatwg-fetch';

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
        <Column width="1-1">
          <Tabs>
            <TabList>
              {languages.map((language, index) => (
                <Tab>{language.name}</Tab>
              ))}
            </TabList>
              {languages.map((language, index) => (
                <TabPanel>
                  <div className="default-transition background-color-transition" style={ {"text-align" : "left"} }>
                    <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                  </div>
                </TabPanel>
              ))}
          </Tabs>
        </Column>
    );
  }

}