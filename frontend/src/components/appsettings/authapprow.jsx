import React from 'react';
import PropTypes from 'prop-types';

import Switch from '@material-ui/core/Switch';

class AuthAppRow extends React.Component {
  render () {
    return <div className="auth-app">
            <div className="app-information">
              <h3>{this.props.app_name}</h3>
              <h3>{this.props.app_created}</h3>
            </div>

            <div className="app-permission-box">
              <Switch checked={this.props.app_is_auth} 
                      onChange={this.handleChange})/>
            </div>
          </div>;
  }

  handleChange (event, checked) {
    if(checked) {
      
    } else {
      
    }
  }
}

AuthAppRow.propTypes = {
  app_name: PropTypes.string,
  app_created: PropTypes.string,
  app_is_auth: PropTypes.bool,
  app_scope_id: PropTypes.string
};

export default AuthAppRow;