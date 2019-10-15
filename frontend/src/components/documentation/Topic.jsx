import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import {androidstudio} from 'react-syntax-highlighter/dist/esm/styles/hljs';


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

let customStyle = {
  'background': "#272B2D",
  'borderRadius': "8px",
  'padding': "12px"
}

export default class Topic extends React.Component {

  render() {
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
          { this.props.children }
        </div>
        <div className="col code">
          {
            (!this.props.noExamples) ? (
              <SyntaxHighlighter
                language={this.props.activeLanguage}
                style={androidstudio}
                customStyle={customStyle}>
                {this.props.codeExamples[
                  this.props.activeLanguage
                ]}
              </SyntaxHighlighter>
            ) : <div></div>
          }
        </div>
      </div>
    );
  }

}
