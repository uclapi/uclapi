import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/styles';


export default class Topic extends React.Component {

  constructor(props) {
    super(props);

    // Need to change this depending on the selected tab
    // this will have to be passed down as prop from the parents
    this.state = {
      activeLanguage: "python"
    }
  }

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
          <SyntaxHighlighter language={this.state.activeLanguage} style={dracula}>
            {this.props.codeExamples[
              this.state.activeLanguage
            ]}
          </SyntaxHighlighter>
        </div>
      </div>
    );
  }

}
