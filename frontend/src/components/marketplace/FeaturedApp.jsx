import React from 'react';
import Paper from '@material-ui/core/Paper';


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
      <a href={"/marketplace/" + this.props.id}>
        <Paper
          className="featuredApp"
          zDepth={this.state.shadow}
          onMouseOver={this.onMouseOver}
          onMouseOut={this.onMouseOut}
          style={{
            "borderRadius": "10px"
          }}>
          <img src={this.props.logo} />
          <h1>{this.props.name}</h1>
          <p>{this.props.description}</p>
        </Paper>
      </a>
    )
  }

}
