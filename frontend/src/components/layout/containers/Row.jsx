import React from 'react';

import placeholder from 'Images/home-page/splash_screen.png';

/**
REQUIRED ATTRIBUTES:
this.props.styling ( styling types 'warning red' - red, 'splash-parallex' - primary color background, 'secondary' - dark grey, 'team-parallax' - hackathon scroll bg )
                OR / AND
this.props.src (pass an image to overlay in the backgorund of the row)

OPTIONAL ATTRIBUTES:
this.props.height (manually set the height over what the contents)
this.props.style (An array of styles to add to the component)
this.props.noPadding (Removes the default padding of 50px)

**/
export default class Row extends React.Component {

  constructor(props) {
    super(props);

    this.DEBUGGING = false;
    this.DEFAULT_COLOR ='transparent';

    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this);
    this.setupBackground = this.setupBackground.bind(this);
    this.setTheme = this.setTheme.bind(this);

    this.class = 'row';
    this.style = [];

    if(this.props.style) { this.style = this.props.style; }

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
    if(this.DEBUGGING) { console.log('DEBUG: ' + key + ' updated to: ' + value); }
  }

  setTheme() {
    // REQUIRED ATTRIBUTES
    // Either given a color or src
    this.setupBackground();
    // Override for padding
    if(!this.props.noPadding) {this.class += ' vertical-padding'}

    // OPTIONAL ATTRIBUTES
    // Height of container
    if(this.props.height) { this.setStyleKeyValuePair('height', this.props.height); }
  }

  setupBackground() {
    if(this.DEBUGGING) { console.log('Row.setupBackground: DEBUG Background color / src is : ' + this.props.styling + ' / ' + this.props.src); }

    if(this.props.styling) { this.class += ' ' + this.props.styling; }

    if(this.props.src) {
      if(this.props.src == 'url_not_found') {
        this.setStyleKeyValuePair('backgroundImage', `url(${placeholder})`);
      } else {
        this.setStyleKeyValuePair('backgroundImage',`url(${this.props.src})`);
      }
      this.setStyleKeyValuePair('backgroundPosition', '50%');
      this.setStyleKeyValuePair('backgroundRepeat', 'no-repeat');
    }

    if(typeof this.props.styling == 'undefined' && typeof this.props.src == 'undefined') {
      console.log('Row.setupBackground: EXCEPTION No color or source set for background so resorting to a ' + this.DEFAULT_COLOR + ' background');
      this.class += ' ' + this.DEFAULT_COLOR;
    }
  }

}
