import React from 'react';
import PropTypes from 'prop-types';

import Switch from '@material-ui/core/Switch';

class AuthAppRow extends React.Component {
  render () {
    return <div className="settings-title"><h2>Permissions</h2></div>
        <div className="card-settings">
          <div className="auth-app">
            <div className="app-information">
              <h3>{this.props.app_name}</h3>
              <h3>{this.props.app_created}</h3>
            </div>
            <div className="app-permission-box">
              <Switch checked={this.props.app_is_auth} />
            </div>
          </div>
        </div>;
  }
}

UserApps.propTypes = {
  app_name: PropTypes.string,
  app_created: PropTypes.string,
  app_is_auth: PropTypes.bool
};

export default AuthAppRow;