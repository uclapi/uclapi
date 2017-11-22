import React from 'react';

import {Card, CardActions, CardHeader,
  CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


export default class App extends React.Component {

  render() {
    return (
      <div className="featuredApp">
        <img src={this.props.logo} />
        <h1>{this.props.name}</h1>
        <p>{this.props.description}</p>
      </div>
    )
  }

}
