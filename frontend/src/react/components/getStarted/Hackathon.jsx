import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';

import Jumbotron from './Jumbotron.jsx';


export default class Hackathon extends React.Component {

  render() {
    return (
      <Jumbotron bgcolor={"#0B3954"} color={"#fff"}>
        <h2><b>We're doing a hackathon. You should check it out and get started building the future of UCL !</b></h2>
        <a href={"https://hackathon.uclapi.com/"}>
          <RaisedButton label="UCL API Hackathon" primary={true} />
        </a>
      </Jumbotron>
    )
  }

}
