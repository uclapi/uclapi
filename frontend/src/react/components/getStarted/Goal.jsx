import React from 'react';


export default class Goal extends React.Component {

  render() {
    return (
      <div className="goal">
        <div className="container">
          <h1>Our Goal</h1>
          <h3>Create a ridiculously simple, documentation first, and comprehensive API around UCL's digital services and establish an ecosystem of third party UCL apps and services that use the API.</h3>
          <a href={"https://trello.com/b/mimLkk3c/ucl-api-roadmap"}>
            The UCL API Roadmap is public. Check it out and vote ✅
          </a>
        </div>
      </div>
    )
  }

}
