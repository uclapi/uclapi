import React from 'react';

import App from './App.jsx';


export default class Category extends React.Component {

  render() {
    return (
      <div className="category">
        <div className="container">
          <h1>{this.props.name}</h1>
          <h2>{this.props.description}</h2>
          <div className="apps">
            {
              this.props.apps.map((app) => {
                return <App name={app.name} logo={app.logo} description={app.description} />;
              })
            }
          </div>
        </div>
      </div>
    )
  }

}
