import React from 'react';
import AndroidIcon from '@material-ui/icons/Android';

import Button from '@material-ui/core/Button';


export default class Left extends React.Component {

  render() {
    let buttons = [];
    if (this.props.app.webLink) {
      buttons.push(
        <Button
          variant="contained"
          key={1}
          className="btn"
          label="Web"
          href={this.props.app.webLink}
          primary={true} />
      )
    }

    if (this.props.app.androidLink) {
      buttons.push(
        <Button
          variant="contained"
          key={2}
          label="Android"
          backgroundColor="#a4c639"
          labelColor={"#ffffff"}
          className="btn"
          href={this.props.app.andoridLink}
          icon={<AndroidIcon />}
        />
      )
    }

    if (this.props.app.iosLink) {
      buttons.push(
        <Button
          variant="contained"
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
        <img className="logo" src={this.props.app.logo} />
        {buttons}
        <br />
        <p>Contact Developer at <a href={this.props.app.developerContact}>{this.props.app.developerContact}</a></p>
      </div>
    )
  }

}
