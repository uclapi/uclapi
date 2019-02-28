import React from 'react';


export default class StagingBanner extends React.Component {

  render() {
    return (
      <div className="stagingBanner">
        <div className="container">
          <h1>Warning! This is our bleeding-edge staging environment, and therefore performance, accuracy and reliability of the API cannot be guaranteed. For our stable, supported API please go to</h1>
          <a href={"https://uclapi.com"}>
            uclapi.com
          </a>
        </div>
      </div>
    )
  }

}
