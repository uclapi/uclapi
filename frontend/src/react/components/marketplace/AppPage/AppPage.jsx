import React from 'react';
import Paper from 'material-ui/Paper';

import allApps from './../allApps.jsx';
import Header from './Header.jsx';
import Left from './Left.jsx';
import Right from './Right.jsx';
import NotFound from './NotFound.jsx';


export default class AppPageComponent extends React.Component {

  constructor(props) {
    super(props);

    if (this.props.appId in allApps) {
      this.state = {
        found: true,
        app: allApps[this.props.appId],
      }
    }
    else {
      this.state = {
        found: false,
      }
    }

  }

  render() {
    return (
      (this.state.found) ? (
        <div className="appPage">
          <div className="container">
            <Header app={this.state.app} />

            <Paper className="paper" zDepth={1}>
              <div className="row">
                <div className="col3">
                  <Left app={this.state.app} />
                </div>
                <div className="col9">
                  <Right app={this.state.app} />
                </div>
              </div>
            </Paper>
          </div>
        </div>
      ): (
        <NotFound />
      )
    )
  }

}
