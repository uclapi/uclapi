import React from 'react';

export default class ButtonView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var button_class_name = "uclapi-button default-transition background-color-transition";
    var button_style = [];

    if(!this.props.buttonType) {button_class_name += " default-button";}
    else {button_class_name += " " + this.props.buttonType + "-button";}
    if(this.props.isCircular) {button_class_name += " circular-button"}
    if(this.props.padding) { button_style['padding'] = this.props.padding; }
    if(this.props.margin) { button_style['margin'] = this.props.margin; }
    if(this.props.isCentered) {
      button_style['marginRight'] = "auto";
      button_style['marginLeft'] = "auto";
      button_style['display'] = "flex";
    }

    if(this.props.buttonType == "image") {
      return (
        <a href={this.props.link}>
              <div className={button_class_name} style={button_style}>
                <img src={this.props.src} alt={this.props.text} />
              </div>
         </a>
      );
    } else {
      return (
         <a href={this.props.link}>
              <div className={button_class_name} style={button_style}>
                {this.props.text}
              </div>
         </a>
      );
    }
  }

}