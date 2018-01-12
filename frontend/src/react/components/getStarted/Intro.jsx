import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';


export default class Intro extends React.Component {

  constructor(props) {
    super(props);
    let loggedIn = false;

    if (window.initialData.logged_in === "True") {
      loggedIn = true;
    }

    this.state = {
      loggedIn: loggedIn
    };
  }

  render() {
    let startLabel = "Start Building";

    if (this.state.loggedIn) {
      startLabel = "Dashboard";
    }

    return (
      <div className="intro">
        <div className="container">
          <h1>UCL API</h1>
          <h2>UCL API is a <b>student-built</b> platform for <b>student developers</b> to improve the <b>student experience</b> of everyone at UCL.</h2>
          <a href={"/dashboard/"}>
            <RaisedButton label={startLabel} primary={true} />
          </a>
          <a href={"/docs/"}>
            <RaisedButton label="Docs" />
          </a>
        </div>
      </div>
    )
  }

}
