import React from 'react';


export default class Blog extends React.Component {

  render() {
    return (
      <div className="blog">
        <div className="container">
          <h1>Check out our <a href="https://medium.com/ucl-api">blog</a> for tutorials.</h1>
          <a href="https://medium.com/ucl-api/5-steps-to-getting-started-with-webhooks-on-ucl-api-481b2a81ac4f">
            5 Steps to Getting Started with Webhooks on UCL API
          </a>
          <a href={"https://medium.com/ucl-api/welcome-to-the-ucl-api-e8fb7a664322"}>
            Welcome to the UCL API
          </a>
          <a href="https://medium.com/ucl-api/the-launch-of-ucl-api-e835d7c80925">
            The Launch of UCL API
          </a>
        </div>
      </div>
    )
  }

}
