import React from 'react';


export default class Blog extends React.Component {

  render() {
    return (
      <div className="blog">
        <div className="container">
          <h1>Check out our <a href="https://medium.com/ucl-api">blog</a> for tutorials.</h1>
          <a href="https://medium.com/ucl-api/the-magic-behind-ucl-library-seating-4fb1f494c789?source=rss----451d1abf42ea---4">
            The Magic Behind UCL Library Seating
          </a>
          <a href="https://medium.com/ucl-api/building-a-university-api-why-and-how-f455cdbc9ce2?source=rss----451d1abf42ea---4">
            Building a University API: Why and How
          </a>
          <a href="https://medium.com/ucl-api/resources-api-desktop-availability-af382a958721?source=rss----451d1abf42ea---4">
            Resources API: Desktop Availability
          </a>
        </div>
      </div>
    )
  }

}
