/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

// Standard React components
import 'whatwg-fetch'

import React from 'react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { androidstudio } from 'react-syntax-highlighter/dist/esm/styles/hljs'
// DEPENDENCIES
import { Tab, TabList, TabPanel, Tabs } from 'react-tabs'

// Code Generator
import * as RequestGenerator from 'Layout/data/RequestGenerator.jsx'
// Common Components
import { Column } from 'Layout/Items.jsx'

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
    super(props)

    this.DEBUGGING = false

    const {
      type,
      url,
      params,
    } = this.props
    // Every button view should contain a link and text
    if (typeof type == `undefined`) { console.log(`EXCEPTION: CodeView.constructor: no type defined`) }
    else if (type == `request`) {
      if (typeof url == `undefined`) { console.log(`EXCEPTION: CodeView.constructor: request but no url defined`) }
      if (typeof params == `undefined`) { console.log(`EXCEPTION: CodeView.constructor: request but no params defined`) }
    } else if (type == `raw-examples`) {
      if (typeof this.props.languages == `undefined`) { console.log(`EXCEPTION: CodeView.constructor: raw examples but no examples defined`) }
    } else {
      console.log(`EXCEPTION: CodeView.constructor: Type of code view is not recognized`)
    }

    this.state = {
      languages: this.getLanguages(),
      tabIndex: 0,
    }
  }

  onSelect = tabIndex => this.setState({ tabIndex })

  render() {
    const {
      tabIndex,
      languages,
    } = this.state
    if (this.DEBUGGING) { console.log(`DEBUG: currently selected tab is: ` + tabIndex) }

    return (
      <Column width='1-1'>
        <Tabs selectedIndex={tabIndex} onSelect={this.onSelect}>
          <TabList>
            {languages.map(({ name }, index) => (
              <Tab className={index == tabIndex ? `selected-tab` : `unselected-tab`} key={`tab-${name}`}>
                {name}
              </Tab>
            ))}
          </TabList>
          {languages.map(({ name, code }) => (
            <TabPanel key={`TabPanel-${name}`}>
              <div className='default-transition background-color-transition inner-tab' style={{ 'textAlign': `left` }}>
                <SyntaxHighlighter language={name} style={androidstudio}>{code}</SyntaxHighlighter>
              </div>
            </TabPanel>
          ))}
        </Tabs>
      </Column>
    )
  }

  getResponse = (response) => {
    return [
      {
        'name': `response`,
        'code': response,
      },
    ]
  }

  getLanguages = () => {
    let languages = []

    const {
      type,
      url,
      params,
      response,
    } = this.props
    // type is 'request' - Use request generator to generate what to show
    if (type == `request`) { languages = RequestGenerator.getRequest(url, params, true) }
    // type is 'real-response' - Use the passed response
    if (type == `response`) { languages = this.getResponse(response) }
    // type is raw-examples - Use the passed examples
    if (type == `raw-examples`) { 
      languages = [
        {
          "name": "python",
          "code": this.props.languages['python']
        },
        {
          "name": "javascript",
          "code": this.props.languages['javascript']
        },
        {
          "name": "shell",
          "code": this.props.languages['shell']
        },
      ]
    }

    return languages
  }

}
