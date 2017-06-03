import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';

import Jumbotron from './Jumbotron.jsx';


export default class Intro extends React.Component {

  render() {
    return (
      <Jumbotron>
        <h1>Room Bookings API</h1>
        <h3>Getting Started Guide</h3>
        <RaisedButton label="Start Building" primary={true} />
      </Jumbotron>
    )
  }

}
