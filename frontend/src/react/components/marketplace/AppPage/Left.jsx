import React from 'react';

import RaisedButton from 'material-ui/RaisedButton';


export default class Left extends React.Component {

  render() {
    return (
      <div className="left">
        <img className="logo" src={this.props.app.logo} />
        <RaisedButton className="btn" label="Get It" primary={true} />
      </div>
    )
  }

}
