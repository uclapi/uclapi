import React from 'react';


export default class Header extends React.Component {

  render() {
    return (
      <div className="header">
        <h2><a href="/marketplace">UCL Marketplace</a> / {this.props.app.name}</h2>
      </div>
    )
  }

}
