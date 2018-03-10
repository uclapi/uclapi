import React from 'react';
import ActionAndroid from 'material-ui/svg-icons/action/android';

import RaisedButton from 'material-ui/RaisedButton';


export default class Left extends React.Component {

  render() {
    let buttons = [];
    if (this.props.app.webLink) {
      buttons.push(
        <RaisedButton
          key={1}
          className="btn"
          label="Web"
          href={this.props.app.webLink}
          primary={true} />
      )
    }

    if (this.props.app.androidLink) {
      buttons.push(
        <RaisedButton
          key={2}
          label="Android"
          backgroundColor="#a4c639"
          labelColor={"#ffffff"}
          className="btn"
          href={this.props.app.andoridLink}
          icon={<ActionAndroid />}
        />
      )
    }

    if (this.props.app.iosLink) {
      buttons.push(
        <RaisedButton
          key={3}
          label="iOS"
          backgroundColor="#537DB0"
          labelColor={"#ffffff"}
          className="btn"
          href={this.props.app.iosLink}
        />
      )
    }
    return (
      <div className="left">
        <img className="logo" src={window.staticURL + this.props.app.logo} />
        { buttons }
        <br />
        <p>Contact Developer at <a href={this.props.app.developerContact}>{this.props.app.developerContact}</a></p>
      </div>
    )
  }

}
