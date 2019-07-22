import React from 'react';


export default class Blog extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      articles: window.initialData.medium_articles
    };
  }

  render() {
    return (
      <div className="blog dark">
        <div className="container">
          <h2>Check out our <a href="https://medium.com/ucl-api">blog</a> for tutorials.</h2>
          <br />
          <br />
          {this.state.articles.map(item => (
          <div className="blog-link-container">
            <a href={item.url}>
              {item.title}
            </a>
            <br />
            <br />
            <br />
            <br />
          </div>
          ))}
        </div>
      </div>
    )
  }

}
