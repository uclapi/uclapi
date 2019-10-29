// Standard React components
import React from 'react';

// DEPENDENCIES
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';
import 'whatwg-fetch';

// Common Components
import {Column, TextView, Row} from 'Layout/Items.jsx'

// Code Generator
import * as RequestGenerator from 'Layout/data/RequestGenerator.jsx';

/**
REQUIRED ATTRIBUTES:
this.props.type ( The type of code to be generated or outputted )
  'request':
    this.props.url
    this.props.params

  'response'
    this.props.response

OPTIONAL ATTRIBUTES:
**/

export default class CodeView extends React.Component {
  constructor(props) {
    super(props);

    this.DEBUGGING = false;

    // Every button view should contain a link and text
    if(typeof this.props.type == 'undefined') {console.log('EXCEPTION: CodeView.constructor: no type defined');}
    else if (this.props.type == 'request') {
      if(typeof this.props.url == 'undefined') {console.log('EXCEPTION: CodeView.constructor: request but no url defined');}
      if(typeof this.props.params == 'undefined') {console.log('EXCEPTION: CodeView.constructor: request but no params defined');}
    } else if (this.props.type == 'request') {
      if(typeof this.props.response == 'undefined') {console.log('EXCEPTION: CodeView.constructor: response but no response defined');}
    } else {
      console.log('EXCEPTION: CodeView.constructor: Type of code view is not recognized');
    }

    this.getLanguages = this.getLanguages.bind(this);
    this.getResponse = this.getResponse.bind(this);

    this.state = {
      languages: this.getLanguages(),
      tabIndex: 0
    }
  }

  render() {
    if(this.DEBUGGING) { console.log('DEBUG: currently selected tab is: ' + this.state.tabIndex); }

    return (
        <Column width='1-1'>
          <Tabs selectedIndex={this.state.tabIndex} onSelect={tabIndex => this.setState({ tabIndex })}>
            <TabList>
              {this.state.languages.map((language, index) => (
                <Tab className={index==this.state.tabIndex ? 'selected-tab' : 'unselected-tab'}>
                  {language.name}
                </Tab>
              ))}
            </TabList>
              {this.state.languages.map((language, index) => (
                <TabPanel>
                  <div className='default-transition background-color-transition inner-tab' style={ {'textAlign' : 'left'} }>
                    <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                  </div>
                </TabPanel>
              ))}
          </Tabs>
        </Column>
    );
  }

  getResponse(response) {
    return [
      {
        'name' : 'response',
        'code' : response
      }
    ];
  }

  getLanguages() {
    var languages = [];

    // type is 'request' - Use request generator to generate what to show
    if(this.props.type == 'request') {languages = RequestGenerator.getRequest(this.props.url, this.props.params, true);}
    // type is 'real-response' - Use the passed response
    if(this.props.type == 'response') {languages = this.getResponse(this.props.response);}

    return languages;
  }

}
