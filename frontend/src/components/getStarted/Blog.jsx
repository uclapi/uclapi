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
      <div className="blog">
        <div className="container">
          <h1>Check out our <a href="https://medium.com/ucl-api">blog</a> for tutorials.</h1>
          {this.state.articles.map(item => (
          <a href={item.url}>
            {item.title}
          </a>
          ))}
        </div>
      </div>
    )
  }

}
