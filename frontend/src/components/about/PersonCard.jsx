import React from 'react';

import Paper from 'material-ui/Paper';


export default class PersonCard extends React.Component {

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
      <div className="personCard">
        <a href={this.props.github}>
          <Paper
            className="paper"
            zDepth={this.state.shadow}
            onMouseOver={this.onMouseOver}
            onMouseOut={this.onMouseOut}
            style={{
              "borderRadius": "1px"
            }}>
            <img src={this.props.image} />
            <h1>{this.props.name}</h1>
            <h2>{this.props.title}</h2>
            <p>{this.props.email}</p>
            <h3>{`${this.props.startYear} - ${this.props.endYear}`}</h3>
          </Paper>
        </a>
      </div>
    )
  }

}
