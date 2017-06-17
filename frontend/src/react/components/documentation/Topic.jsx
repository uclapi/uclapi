import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/styles';


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
          <SyntaxHighlighter language={this.props.activeLanguage} style={dracula}>
            {this.props.codeExamples[
              this.props.activeLanguage
            ]}
          </SyntaxHighlighter>
        </div>
      </div>
    );
  }

}
