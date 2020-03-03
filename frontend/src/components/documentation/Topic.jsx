/* eslint-disable react/prop-types */

import React from 'react'
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter'
import js from 'react-syntax-highlighter/dist/esm/languages/hljs/javascript'
import py from 'react-syntax-highlighter/dist/esm/languages/hljs/python'
import sh from 'react-syntax-highlighter/dist/esm/languages/hljs/shell'

import { CodeView } from 'Layout/Items.jsx'

SyntaxHighlighter.registerLanguage(`javascript`, js)
SyntaxHighlighter.registerLanguage(`python`, py)
SyntaxHighlighter.registerLanguage(`shell`, sh)

/*
  This is the main component that contains content for the documentation.
  The docs page is comprised of multiple Topic components.
  Each Topic component has containing html as child components which are rendered
  on the left side.
  Topic component also takes in a codeExamples prop which are the code examples
  that are show on the right side
*/

/*
  Maybe we can create the sidebar manually?
  by creating and ordering React Components according to the structure of
  the page and we can
  put an href inside each Topic component so that when you click on the
  link in the sidebar, it takes you to the Topic component
*/

export default class Topic extends React.Component {

  render() {

    let codeType = `no-examples`

    const { codeExamples, noExamples, children } = this.props

    if (typeof noExamples == `undefined`) {
      codeType = `raw-examples`

      if (codeExamples.python == codeExamples.javascript) {
        codeType = `response`
      }
    }

    return (
      <div className="row">
        <div className="col text">
          {/*
            I thougth of just running this through a function like
            MarkdownToHTML(this.props.children)
            but then realised that it may break the nesting
            Like if we have:
            Topic1
              SubTopic1
              SubTopic2
            then we can render that in the sidebar
            but converting to markdown will prevent us from doing that
            I guess it depends on how we generate the sidebar
          */}
          {children}
          {codeType == `raw-examples` && (
            <CodeView languages={codeExamples} type={codeType} />
          )}
          {codeType == `response` && (
            <CodeView response={codeExamples.python} type={codeType} />
          )}
        </div>
      </div>
    )
  }

}
