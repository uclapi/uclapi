import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


export default class Intro extends React.Component {

  render() {
    return (
      <div className="intro">
        <div className="container">
          <h1>UCL API</h1>
          <h2>UCL API is a <b>student-built</b> platform for <b>student developers</b> to improve the <b>student experience</b> of everyone at UCL.</h2>
          <a href={"/dashboard/"}>
            <RaisedButton label="Start Building" primary={true} />
          </a>
        </div>
      </div>
    )
  }

}
