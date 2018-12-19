import React from 'react';


export default class Table extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="table">
        <h1>{this.props.name}</h1>
        {this.props.children}
      </div>
    );
  }

}
