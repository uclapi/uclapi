import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.color OR this.props.src (remember to set a design for the layout)

OPTIONAL ATTRIBUTES:
this.props.fill (will make the layout fill an entire screen)
this.props.isPadded (and variations affect the vertical padding of the layout)
this.props.height (manually set the height over what the contents)

**/
export default class Row extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      DEBUGGING: false,
      DEFAULT_COLOR: 'dark-grey',
      style: [],
      class: 'row'
    }

    this.setupStyle = this.setupStyle.bind(this);
    this.setupBackground = this.setupBackground.bind(this);
  }

  setupStyle() {
    this.setupBackground();
  }

  setupBackground() {
    if(this.props.color) { 
      row_class_name += " " + this.props.color;
      return;
    }

    if(this.props.src) {
      var img_size = "Cover";
      if(this.props.img_size) { img_size = this.props.img_size; }

      if(this.props.src == "url_not_found") {
        row_style['backgroundImage'] = `url(${placeholder})`; 
      } else {
        row_style['backgroundImage'] = `url(${this.props.src})`; 
      }
      row_style['backgroundSize'] = img_size;
      row_style['backgroundPosition'] = "50%";
      row_style['backgroundRepeat'] = "no-repeat";
    }

    console.exception("EXCEPTION: No color or source set for background so resorting to a " + DEFAULT_COLOR + " background");
    row_class_name += " " + DEFAULT_COLOR;
  }

  render() {
    var row_class_name = "row";
    var row_style = {};

    row_class_name += " vertical-padding-top vertical-padding-bottom";

    if(this.props.fill) { row_class_name += " full-screen"; }
    if(this.props.isScrollOverflow) { row_style['overflowX'] = "scroll"; }
    if(this.props.height) { row_style['height'] = this.props.height; }

    return (
      <div className={ row_class_name } style={ row_style }>
          {this.props.children}
      </div>
    );
  }

}
