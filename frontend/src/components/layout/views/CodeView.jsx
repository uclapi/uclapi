// Standard React components
import React from 'react'; 

// DEPENDENCIES
import {Tabs, Tab} from 'material-ui/Tabs';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';
import 'whatwg-fetch';

// Common Components 
import {Column} from 'Layout/Items.jsx'

export default class CodeView extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className={"code-segment"}>
        <Column style="1-1">
          <Tabs>
            {this.props.languages.map((language, index) => (
              <Tab key={index} label={language.name}>
                <div>
                  <SyntaxHighlighter language={language.name} style={androidstudio}>{language.code}</SyntaxHighlighter>
                </div>
              </Tab>
            ))}
          </Tabs>
        </Column>
      </div>
    );
  }

}