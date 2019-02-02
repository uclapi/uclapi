import React from 'react';
import PropTypes from 'prop-types';

class UserApps extends React.Component {
  render () {
    return <div className="settings-holder">
      <div className="settings-form">

        <div className="settings-title"><h1>Account</h1></div>
        <div className="card-settings">
          <h3>{this.props.fullname}{"\n"}
          {this.props.department}</h3>
        </div>

        <div className="settings-title"><h1>Permissions</h1></div>
        <div className="card-settings">
          <div className="auth-app">
            <div className="app-information">
              Social App {"\n"}
              Harry Liversedge
            </div>
            <div className="app-permission-box">
              Put a button here
            </div>
          </auth-app>
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