import React from 'react';
import PropTypes from 'prop-types';

import Switch from '@material-ui/core/Switch';

class UserApps extends React.Component {
  render () {
    return <div className="settings-holder">
      <div className="settings-form">

        <div className="settings-title"><h2>Account</h2></div>
        <div className="card-settings">
          <h3>{this.props.fullname}</h3>
          <h3>{this.props.department}</h3>
        </div>

        <div className="settings-title"><h2>Permissions</h2></div>
        <div className="card-settings">
          <div className="auth-app">
            <div className="app-information">
              <h3> Social App </h3>
              <h3> Harry Liversedge </h3>
            </div>
            <div className="app-permission-box">
              <Switch />
            </div>
          </div>
        </div>
      </div>
    </div>;
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string,
  department: PropTypes.string
};

export default UserApps;