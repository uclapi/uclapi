import React from 'react';
import PropTypes from 'prop-types';

import Button from '@material-ui/core/Button';

class AuthAppRow extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      app: props.app,
      showCreate: false
    };
    this.handleChange = this.handleChange.bind(this);
  }

  render () {
    return <div className="auth-app">
            <div className="app-information">
              <h3>{this.props.app_name}</h3>
              <h3>{this.props.app_created}</h3>
            </div>

            <div className="app-permission-box">
              <Button disabled={!this.props.app_is_auth} 
                      size="medium" color="primary"
                      onClick={this.handleChange}>
                Revoke permissions
              </Button>
            </div>
          </div>;
  }

  handleChange (event, checked) {
      // Call function in back end to delete scope
  }

}

AuthAppRow.propTypes = {
  app_name: PropTypes.string,
  app_created: PropTypes.string,
  app_is_auth: PropTypes.bool,
  app_id: PropTypes.string
};

export default AuthAppRow;