import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.heading (what heading the text is)

OPTIONAL ATTRIBUTES:
this.props.align (the alignment of the text as in the css tag text-align)
this.props.link (add a link to the text, this is the url to link to)
**/

export default class TextView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var text_style = [];

    var heading_size = "6";
    if(this.props.heading) { heading_size = this.props.heading; }

    var CustomTag = `h${heading_size}`;
    if(this.props.align) {text_style['textAlign'] = this.props.align; }
    if(this.props.color) {text_style['color'] = this.props.color; text_style['textDecorationColor'] = this.props.color;}
    if(this.props.isInline) {text_style['display'] = "inline-block"; }

    var isLink = false;
    if(this.props.link) {isLink = true;}

    return (
        <CustomTag style={text_style}>
          {isLink ? ( 
            <a className="default-transition color-transition" href = {this.props.link}>
              <div style={text_style}>
                {this.props.text}
              </div>
            </a> 
          ) : (
            <div style={text_style}>
              {this.props.text}
            </div>
          )}
        </CustomTag>
    );
  }

}