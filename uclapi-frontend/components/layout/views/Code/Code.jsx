import * as RequestGenerator from '@/data/RequestGenerator'
import React, { useState } from 'react'
import SyntaxHighlighter from 'react-syntax-highlighter'
import { androidstudio } from 'react-syntax-highlighter/dist/cjs/styles/hljs'
import { Nav } from 'rsuite';
import styles from './Code.module.scss'

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
  const langs = getLanguages(languages, type, url, params, response)

  return (
    <>
      <Nav
        className={styles.languageTabsWrapper}
        style={{ width: "100%" }}
        activeKey={tabIndex}
        onSelect={setTabIndex}
      >
        {langs.map(({ name }) => (
          <Nav.Item
            className={`${styles.languageTab} ${
              tabIndex === name ? styles.selected : ""
            }`}
            eventKey={name}
          >
            {name}
          </Nav.Item>
        ))}
      </Nav>
      {langs.map(
        ({ name, code }) =>
          tabIndex === name && (
            <div
              className="default-transition background-color-transition inner-tab"
              style={{ textAlign: `left`, width: "100%" }}
            >
              <SyntaxHighlighter language={name} style={androidstudio}>
                {code}
              </SyntaxHighlighter>
            </div>
          )
      )}
    </>
  );
}

export default Code
