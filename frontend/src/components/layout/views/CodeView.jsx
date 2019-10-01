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
import * as RequestGenerator from 'Layout/data/RequestGenerator.jsx';

export default class CodeView extends React.Component {
  constructor(props) {
    super(props);

    this.DEBUGGING = true;

    this.state = {
      tabIndex: 0,
    }

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

    if(this.DEBUGGING) { console.log("DEBUG: currently selected tab is: " + this.state.tabIndex); }

    return (
        <Column width="1-1">
          <Tabs selectedIndex={this.state.tabIndex} onSelect={tabIndex => this.setState({ tabIndex })}>
            <TabList>
              {languages.map((language, index) => (
                <Tab className={index==this.state.tabIndex ? 'selected-tab' : 'unselected-tab'}>
                  {language.name}
                </Tab>
              ))}
            </TabList>
              {languages.map((language, index) => (
                <TabPanel>
                  <div className="default-transition background-color-transition" style={ {"textAlign" : "left"} }>
                    <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                  </div>
                </TabPanel>
              ))}
          </Tabs>
        </Column>
    );
  }

}