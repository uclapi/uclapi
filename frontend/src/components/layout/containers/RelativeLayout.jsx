import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.color OR this.props.src (remember to set a design for the layout)

OPTIONAL ATTRIBUTES:
this.props.fill (will make the layout fill an entire screen)
this.props.isPadded (and variations affect the vertical padding of the layout)
this.props.height (manually set the height over what the contents)

**/
export default class RelativeLayout extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var row_class_name = "row";
    var row_style = {};

    if(this.props.fill) { row_class_name += " full-screen"; }
    if(this.props.color) { row_class_name += " " + this.props.color;}
    if(this.props.isPadded) { row_class_name += " vertical-padding-top vertical-padding-bottom"; }
    if(this.props.isPaddedTop) { row_class_name += " vertical-padding-top"; }
    if(this.props.isPaddedBottom) { row_class_name += " vertical-padding-bottom"; }
    if(this.props.isScrollOverflow) { row_style['overflowX'] = "scroll"; }
    if(this.props.height) { row_style['height'] = this.props.height; }
    if(this.props.src) {
      var img_size = "Cover";
      if(this.props.img_size) { img_size = this.props.img_size; }

       row_style['backgroundImage'] = `url(${this.props.src})`; 
       row_style['backgroundSize'] = img_size;
       row_style['backgroundPosition'] = "50%";
       row_style['backgroundRepeat'] = "no-repeat";
    }

    return (
      <div className={ row_class_name } style={ row_style }>
          {this.props.children}
      </div>
    );
  }

}
