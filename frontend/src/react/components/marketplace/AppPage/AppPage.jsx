import React from 'react';

import allApps from './../allApps.jsx';
import Left from './Left.jsx';
import Right from './Right.jsx';


export default class AppPageComponent extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      app: allApps[this.props.appId]
    }

    console.log(this.props);
    console.log("app", this.state.app);
  }

  render() {
    return (
      <div className="appPage">
        <div className="container">
          <div className="row">
            <div className="col3">
              <Left app={this.state.app} />
            </div>
            <div className="col9">
              <Right app={this.state.app} />
            </div>
          </div>
        </div>
        <h1>App Page for {this.props.appId}</h1>
      </div>
    )
  }

}
