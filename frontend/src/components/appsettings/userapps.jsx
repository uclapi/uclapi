import React from 'react';
import PropTypes from 'prop-types';
import AuthAppRow from './authapprow.jsx';

class UserApps extends React.Component {
  render () {
    return <div className="settings-holder">
      <div className="settings-form">

        <div className="settings-title"><h2>Account</h2></div>
        <div className="card-settings">
          <div className="profile-card">
            <h3>{this.props.fullname}</h3>
            <h3>{this.props.department}</h3>
          </div>
        </div>

        <div className="settings-title"><h2>Permissions</h2></div>
        <div className="card-settings">
          {this.props.apps.map((app, i) => {
            app['scopes'][1]['enabled']=="true" || app['scopes'][2]['enabled']=="true" ? (
              <AuthAppRow app_name={app.name}
                app_created={app.created}
                app_is_auth="true" />
            ) : (
              <AuthAppRow app_name={app.name}
                app_created={app.created}
                app_is_auth="false" />
            )
          })}
        </div>
      </div>
    </div>;
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string,
  department: PropTypes.string,
  apps: PropTypes.array
};

export default UserApps;