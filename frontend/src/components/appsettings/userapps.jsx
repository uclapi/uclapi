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
          {this.props.authorised_apps.map((app, i) => {
              return <AuthAppRow app_name={app.app.name}
                app_created={app.app.creator.name}
                app_is_auth={app.active}
                app_id={app.app.id}
                app_client_id={app.app.client_id}
                key={i}
              />;
          })}
        </div>
      </div>
    </div>;
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string,
  department: PropTypes.string,
  authorised_apps: PropTypes.array
};

export default UserApps;
