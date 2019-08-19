import React from 'react';
/**

REQUIRED ATTRIBUTES:
this.props.style (1-3 => 1/3 width)

OPTIONAL ATTRIBUTES:
this.props.isCentered (centers the column within the parent)
this.props.isCenteredText (centers any text within the column)
this.props.isJustifiedText (justifies any text within the column)
this.props.minWidth (Minimum width of the column)
this.props.isVerticalAlign (Aligns the column vertically inside of a pre-set height layout)
this.props.isInline (Are there multiple columns in a line on a row)

**/
export default class Column extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      UNSET_ERROR_WIDTH: "0px"
    }

    this.getWidth = this.getWidth.bind(this);
  }

  getWidth(style) {
    var fraction = style.split("-")
    var adaptation = 100;
    if(this.props.isInline) { var adaptation = 100 - ( 4 * fraction[1] ); }
    var percentage = fraction[0] / fraction[1] * adaptation;
    return percentage + "%";
  }

  render() {
    var content_class_name = "content";
    var content_style = [];

    content_style['width'] = this.getWidth(this.props.style);
    if(this.props.isInline) { 
      content_style['display'] = "inline-" + this.props.isInline; 
      content_style['padding'] = "2%"; 
    }

    if(this.props.isMobileFriendly) {content_class_name += " mobile-friendly"}
    if(this.props.isCentered) {content_class_name += " center-x"; }
    if(this.props.isCenteredText) { content_class_name += " centered-text"; }
    if(this.props.isCenteredItems) {content_class_name += " center-items"; }
    if(this.props.isJustifiedText) { content_class_name += " justified-text"; }
    if(this.props.size) { content_class_name += " " + this.props.size + "-size"; }
    if(this.props.color) { content_class_name +=  " " + this.props.color;}

    if(this.props.padding) { content_style['padding'] = this.props.padding;}
    if(this.props.margin) { content_style['margin'] = this.props.margin;}
    if(this.props.position) { content_style['position'] = this.props.position;}
    if(this.props.float) { content_style['float'] = this.props.float;}

    var isVerticalAlign = this.props.isVerticalAlign;

    if(isVerticalAlign) {
      content_style['height'] = "100%";
      content_style['width'] = this.getWidth(this.props.style);

      return (
        <div style={content_style}>
          <div className="vertical-align-buddy">
            <div className={ content_class_name }>
              {this.props.children}
            </div>
          </div>
        </div>
      );
    } else {
      return (
          <div className={ content_class_name } style={ content_style }>
              {this.props.children}
          </div>
      );
    }
  }

}