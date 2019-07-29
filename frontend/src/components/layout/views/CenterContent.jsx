import React from 'react';

export default class CenterContent extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      WIDTH_OF_CONTENT: "500px"
    }
  }

  render() {
    var content_class_name = "content center-x";
    var content_style = {};
    if(this.props.isJustified) { content_class_name += " justified-text"; }
    content_style['width'] = this.state.WIDTH_OF_CONTENT;

    return (
      <div className="vertical-align-buddy">
        <div className={ content_class_name } style={ content_style }>
          {this.props.content}
        </div>
      </div>
    )
  }

}