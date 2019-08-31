import React from 'react';
import Button from '@material-ui/core/Button';


export default class Marketplace extends React.Component {

  render() {
    return (
      <div className="marketplace">
        <div className="container">
          <h1>UCL Marketplace</h1>
          <h2>Check out UCL Marketplace to find apps built using UCL API</h2>
          <a href={"/marketplace/"}>
            <Button variant="contained" label="UCL Marketplace" />
          </a>
        </div>
      </div>
    )
  }

}
