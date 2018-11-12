import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


export default class Marketplace extends React.Component {

  render() {
    return (
      <div className="marketplace">
        <div className="container">
          <h1>UCL Marketplace</h1>
          <h2>Check out UCL Marketplace to find apps built using UCL API</h2>
          <a href={"/marketplace/"}>
            <RaisedButton label="UCL Marketplace" />
          </a>
        </div>
      </div>
    )
  }

}
