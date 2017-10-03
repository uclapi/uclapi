import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';

import Jumbotron from './Jumbotron.jsx';


export default class Intro extends React.Component {

  render() {
    return (
      <Jumbotron>
        <h1>UCL API</h1>
        <h3>Getting Started Guide</h3>
        <a href={"/dashboard/"}>
          <RaisedButton label="Start Building" primary={true} />
        </a>
      </Jumbotron>
    )
  }

}
