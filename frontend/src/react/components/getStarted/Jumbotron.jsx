import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


export default class Jumbotron extends React.Component {

  render () {
    return (
      <div className="jumbotron">
        <div className="container center">
          <h1>Room Bookings API</h1>
          <h3>Getting Started Guide</h3>
          <RaisedButton label="Start Building" primary={true} />
        </div>
      </div>
    )
  }

}
