import React from 'react';


import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from '@material-ui/core';
import Avatar from '@material-ui/core/Avatar';


export default class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = { shadow: 0 }

    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
  }

  onMouseOver() {
    this.setState({ shadow: 2 });
  }

  onMouseOut() {
    this.setState({ shadow: 0 });
  }

  render() {
    return (
      <div className="app">
        <a href={"/marketplace/" + this.props.id}>
          <Card
            zDepth={this.state.shadow}
            onMouseOver={this.onMouseOver}
            onMouseOut={this.onMouseOut}
            style={{
              "borderRadius": "10px",
              "border": "1px solid #e4e4e4"
            }}>
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
                "fontSize": "18px",
                "fontWeight": 700
              }}
              subtitleStyle={{
                "fontSize": "14px",
                "fontWeight": 400
              }}
            />
          </Card>
        </a>
      </div>
    )
  }

}
