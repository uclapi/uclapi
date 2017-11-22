import React from 'react';

import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';


export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { shadow: 1 }

    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
  }

  onMouseOver() {
    this.setState({ shadow: 3 });
  }

  onMouseOut() {
    this.setState({ shadow: 1 });
  }

  render() {
    return (
      <div className="app">
        <Card
          zDepth={this.state.shadow}
          onMouseOver={this.onMouseOver}
          onMouseOut={this.onMouseOut}>
          <CardHeader
            title={this.props.name}
            subtitle={this.props.description}
            avatar={
              <Avatar
                src={this.props.logo}
                size={60}
              />
            }

            titleStyle={{
              "fontSize": "16px",
              "color": "#143C55",
              "fontWeight": 500
            }}
            subtitleStyle={{
              "fontSize": "14px",
              "fontWeight": 400
            }}
          />
        </Card>
      </div>
    )
  }

}
