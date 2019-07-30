import React from 'react';

// Button is taken straight out of material-ui
import RaisedButton from 'material-ui/RaisedButton';

export default class ButtonView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var button_class_name = "uclapi-button default-transition background-color-transition";
    if(!this.props.buttonType) {button_class_name += " default-button"}
    else {button_class_name += " " + this.props.buttonType + "-button"}

    return (
       <a href={this.props.link}>
            <div className={button_class_name}>
              {this.props.text}
            </div>
       </a>
    );
  }

}