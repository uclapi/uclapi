import React from 'react';


export default class Blog extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      url1: window.initialData.url1,
      url2: window.initialData.url2,
      url3: window.initialData.url3,
      title1: window.initialData.title1,
      title2: window.initialData.title2,
      title3: window.initialData.title3
    };
  }

  render() {
    return (
      <div className="blog">
        <div className="container">
          <h1>Check out our <a href="https://medium.com/ucl-api">blog</a> for tutorials.</h1>
          <a href={this.state.url1}>
            {this.state.title1}
          </a>
          <a href={this.state.url2}>
            {this.state.title2}
          </a>
          <a href={this.state.url3}>
            {this.state.title3}
          </a>
        </div>
      </div>
    )
  }

}
