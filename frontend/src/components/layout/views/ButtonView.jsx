import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.link (A string that gives internal (/docs) or external (https://www.uclapi.com) link)
this.props.text (A string to describe the link, usually ALL CAPS)

OPTIONAL ATTRIBUTES:
this.props.style (An array of styles to add to the component)
this.props.type (changes the styling of the button: Can take default (grey), alternate (white))
this.props.centred (if added will center the button inside its parent)
**/

export default class ButtonView extends React.Component {

  constructor(props) {
    super(props);

    // To enable verbose output
    this.DEBUGGING = false;

    // Bind functions
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this);
    this.getClassName = this.getClassName.bind(this);
    this.setTheme = this.setTheme.bind(this);

    // Every button view should contain a link and text
    if(typeof this.props.link == 'undefined') {console.log('EXCEPTION: ButtonView.constructor: no link defined');}
    if(typeof this.props.text == 'undefined') {console.log('EXCEPTION: ButtonView.constructor: no text defined');}

    // Set type of button
    this.class = this.getClassName();
    this.style = [];
    // If custom styling then include
    if(this.props.style) {this.style = this.props.style;}
    // Set up button tags
    this.setTheme();

    // Save class and stylings to the state
    this.state = {
      class: this.class,
      style: this.style
    };
  }

  render() {
    return (
         <a href={this.props.link}>
              <div className={this.state.class} style={this.state.style}>
                {this.props.text}
              </div>
         </a>
       );
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value;
    if(this.DEBUGGING) { console.log('DEBUG: ' + key + ' updated to: ' + value); }
  }

  getClassName() {
    var buttonType = 'default';
    var className = 'uclapi-button default-transition background-color-transition';
    if(this.props.type) { buttonType = this.props.type; }
    return className + ' ' + buttonType + '-button';
  }

  setTheme() {
    // 'centred' - Center the button inside of its parent
    if(this.props.centred) {this.class += ' ' + 'center-x';}
  }

}
