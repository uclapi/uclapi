import React from 'react';

import placeholder from 'Images/home-page/splash_screen.png';

/**
REQUIRED ATTRIBUTES:
this.props.color OR this.props.src (remember to set a design for the layout)

OPTIONAL ATTRIBUTES:
this.props.height (manually set the height over what the contents)

**/
export default class Row extends React.Component {

  constructor(props) {
    super(props);

    this.DEBUGGING = true;
    this.DEFAULT_COLOR ='transparent';

    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this);
    this.setupBackground = this.setupBackground.bind(this);
    this.setTheme = this.setTheme.bind(this);

    this.class = "row";
    this.style = [];

    this.setTheme();

    this.state = {
      class: this.class,
      style: this.style
    };
  }

  render() {
    return (
      <div className={ this.state.class } style={ this.state.style }>
          {this.props.children}
      </div>
    );
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value;
    if(this.DEBUGGING) { console.log("DEBUG: " + key + " updated to: " + value); }
  }

  setTheme() {
    // REQUIRED ATTRIBUTES
    // Either given a color or src
    this.setupBackground();
    // Override for padding
    if(!this.props.noPadding) {this.class += " vertical-padding"}

    // OPTIONAL ATTRIBUTES
    // Height of container
    if(this.props.height) { this.setStyleKeyValuePair("height", this.props.height); }
  }

  setupBackground() {
    if(this.DEBUGGING) { console.log("DEBUG: Background color / src is : " + this.props.color + " / " + this.props.src); }

    if(this.props.color) { this.class += " " + this.props.color; }

    if(this.props.src) {
      var img_size = "Cover";
      if(this.props.img_size) { img_size = this.props.img_size; }

      if(this.props.src == "url_not_found") {
        this.setStyleKeyValuePair("backgroundImage", `url(${placeholder})`); 
      } else {
        this.setStyleKeyValuePair("backgroundImage",`url(${this.props.src})`); 
      }
      this.setStyleKeyValuePair("backgroundSize", img_size);
      this.setStyleKeyValuePair("backgroundPosition", "50%");
      this.setStyleKeyValuePair("backgroundRepeat", "no-repeat");
    }

    if(typeof this.props.color == "undefined" && typeof this.props.src == "undefined") {
      console.log("EXCEPTION: No color or source set for background so resorting to a " + this.DEFAULT_COLOR + " background");
      this.class += " " + this.DEFAULT_COLOR; 
    }
  }

}
