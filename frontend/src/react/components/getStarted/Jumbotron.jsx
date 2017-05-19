import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


export default class Jumbotron extends React.Component {

  render () {
    return (
      <div className="container center pad">
        <h1>Room Bookings API</h1>
        <p>Getting Started Guide</p>
        <RaisedButton label="Start Building" primary={true} />
      </div>
    )
  }

}
