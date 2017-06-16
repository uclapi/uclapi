import React from 'react';


export default class Cell extends React.Component {

  constructor(props) {
    super(props);

    if (this.props.required) {
      this.state = {
        requirement: "required"
      }
    }
    else {
      this.state = {
        requirement: "optional"
      }
    }
  }

  render() {
    return (
      <div className="row cell">
        <div className="col attribute">
          <p>{this.props.name}</p>
          <p className={this.state.requirement}>{this.state.requirement}</p>
          <p>{this.props.extra}</p>
        </div>
        <div className="col">
          <code>{this.props.example}</code>
        </div>
        <div className="col">
          {this.props.description}
        </div>
      </div>
    );
  }

}
