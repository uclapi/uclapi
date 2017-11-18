import React from 'react';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


export default class App extends React.Component {

  render() {
    return (
      <div className="app">
        <Card>
          <CardMedia>
            <img src={this.props.logo} alt="" />
          </CardMedia>
          <CardTitle title={this.props.name} subtitle={this.props.description}/>
          <CardActions>
            <FlatButton label="Get It" />
          </CardActions>
        </Card>
      </div>
    )
  }

}
