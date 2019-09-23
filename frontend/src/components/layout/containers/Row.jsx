import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.color OR this.props.src (remember to set a design for the layout)

OPTIONAL ATTRIBUTES:
this.props.height (manually set the height over what the contents)

**/
export default class Row extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      DEBUGGING: false,
      DEFAULT_COLOR: 'transparent',
      style: [],
      class: 'row'
    }

    this.setupStyle = this.setupStyle.bind(this);
    this.setupBackground = this.setupBackground.bind(this);
  }

  render() {
    this.setupStyle();

    return (
      <div className={ this.state.class } style={ this.state.style }>
          {this.props.children}
      </div>
    );
  }

  setupStyle() {
    // REQUIRED ATTRIBUTES
    // Either given a color or src
    this.setupBackground();

    // OPTIONAL ATTRIBUTES
    // Height of container
    if(this.props.height) { this.state.style['height'] = this.props.height; }
  }

  setupBackground() {
    if(this.state.DEBUGGING) { console.log("DEBUG: Background color / src is : " + this.props.color + " / " + this.props.src); }

    if(this.props.color) { 
      this.state.class += " " + this.props.color;
    }

    if(this.props.src) {
      var img_size = "Cover";
      if(this.props.img_size) { img_size = this.props.img_size; }

      if(this.props.src == "url_not_found") {
        this.state.style['backgroundImage'] = `url(${placeholder})`; 
      } else {
        this.state.style['backgroundImage'] = `url(${this.props.src})`; 
      }
      this.state.style['backgroundSize'] = img_size;
      this.state.style['backgroundPosition'] = "50%";
      this.state.style['backgroundRepeat'] = "no-repeat";
    }

    if(typeof this.props.color == "undefined" && typeof this.props.src == "undefined") {
      console.log("EXCEPTION: No color or source set for background so resorting to a " + this.state.DEFAULT_COLOR + " background");
      this.state.class += " " + this.state.DEFAULT_COLOR;
    }
  }

}
