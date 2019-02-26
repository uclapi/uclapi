import React from 'react';


export default class StagingBanner extends React.Component {

  render() {
    return (
      <div className="stagingBanner">
        <div className="container">
          <h1>Warning! This is our testing domain, for our stable API please go to</h1>
          <a href={"https://uclapi.com"}>
            uclapi.com
          </a>
        </div>
      </div>
    )
  }

}
