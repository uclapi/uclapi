import React from 'react';
import PropTypes from 'prop-types';

import RaisedButton from 'material-ui/RaisedButton';

class LogInLayout extends React.Component {
  render () {
    return <div className="log-in-layout">
        <div className="container">
          <h1>Sign in to manage app settings</h1>
          <a href={this.props.url}>
            <RaisedButton label="Log in" primary={true} />
          </a>
        </div>
      </div>
  }
}

LogInLayout.propTypes = {
  url: PropTypes.string
};

export default LogInLayout;