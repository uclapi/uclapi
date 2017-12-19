import React from 'react';
import Paper from 'material-ui/Paper';

import App from './App.jsx';


export default class Category extends React.Component {

  render() {
    return (
      <Paper className="category" zDepth={1}>
        <h1 id={this.props.name}>{this.props.name}</h1>
        <h2>{this.props.description}</h2>
        <div className="apps">
          {
            this.props.apps.map((app, i) => {
              return <App {...app} />;
            })
          }
        </div>
      </Paper>
    )
  }

}
