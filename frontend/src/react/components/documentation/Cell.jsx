import React from 'react';


export default class Cell extends React.Component {

  render() {
    return (
      <div className="row cell">
        <div className="col4 attribute">
          <p>{this.props.name}</p>
          <p className={this.props.requirement}>{this.props.requirement}</p>
          <p className="extra">{this.props.extra}</p>
        </div>
        <div className="col8">
          <p>{this.props.description}</p>
          <code>{this.props.example}</code>
        </div>
      </div>
    );
  }

}
