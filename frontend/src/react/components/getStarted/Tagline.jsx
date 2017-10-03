import React from 'react';

import Jumbotron from './Jumbotron.jsx';


export default class Tagline extends React.Component {

  render() {
    return (
      <div className="tagline">
        <div className="container">
          <h2>UCL API is a <b>student-built</b> platform for <b>student developers</b> to improve the <b>student experience</b> of everyone at UCL.</h2>
        </div>
      </div>
    )
  }

}
