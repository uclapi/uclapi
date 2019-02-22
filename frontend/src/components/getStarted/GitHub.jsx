import React from 'react';


export default class GitHub extends React.Component {

  render() {
    return (
      <div className="github">
        <div className="container">
          <h1>We're open source and proud!</h1>
          <h3>Check out our fleshy internals on GitHub!</h3>
          <a href={"https://github.com/uclapi/uclapi"}>
            You know you want to!
          </a>
        </div>
      </div>
    )
  }

}
