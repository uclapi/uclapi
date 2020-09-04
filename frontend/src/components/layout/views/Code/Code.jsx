import * as RequestGenerator from 'Layout/data/RequestGenerator.jsx'
import React, { useCallback, useState } from 'react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { androidstudio } from 'react-syntax-highlighter/dist/esm/styles/hljs'
import { Tab, TabList, TabPanel, Tabs } from 'react-tabs'


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

const getResponse = (response) => {
  return [
    {
      'name': `response`,
      'code': response,
    },
  ]
}

const getLanguages = (languages, type, url, params, response) => {
  let result = []

  // type is 'request' - Use request generator to generate what to show
  if (type == `request`) { result = RequestGenerator.getRequest(url, params, true) }
  // type is 'real-response' - Use the passed response
  if (type == `response`) { result = getResponse(response) }
  // type is raw-examples - Use the passed examples
  if (type == `raw-examples`) {
    result = Object.keys(languages).map((l) => ({
      name: l,
      code: languages[l],
    }))
  }

  return result
}

const Code = ({
  languages,
  type,
  url,
  params,
  response,
}) => {
  const [tabIndex, setTabIndex] = useState(0)
  const onSelect = useCallback((i) => setTabIndex(i))

  const langs = getLanguages(languages, type, url, params, response)

  return (
    <Tabs selectedIndex={tabIndex} onSelect={onSelect}>
      <TabList>
        {langs.map(({ name }, index) => (
          <Tab className={index == tabIndex ? `selected-tab` : `unselected-tab`} key={`tab-${name}`}>
            {name}
          </Tab>
        ))}
      </TabList>
      {langs.map(({ name, code }) => (
        <TabPanel key={`TabPanel-${name}`}>
          <div
            className='default-transition background-color-transition inner-tab'
            style={{ 'textAlign': `left` }}
          >
            <SyntaxHighlighter
              language={name}
              style={androidstudio}
            >
              {code}
            </SyntaxHighlighter>
          </div>
        </TabPanel>
      ))}
    </Tabs>
  )
}

export default Code