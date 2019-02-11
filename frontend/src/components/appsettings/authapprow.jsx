import React from 'react';
import PropTypes from 'prop-types';

import Button from '@material-ui/core/Button';

class AuthAppRow extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      apps: props.apps,
      showCreate: false
    };
  }

  render () {
    return <div className="auth-app">
            <div className="app-information">
              <h3>{this.props.app_name}</h3>
              <h3>{this.props.app_created}</h3>
            </div>

            <div className="app-permission-box">
              <Button disabled={this.props.app_is_auth} 
                      size="medium" color="primary"
                      onClick={this.handleChange}>
                Revoke permissions
              </Button>
            </div>
          </div>;
  }

  handleChange (event, checked) {
      this.setState((state) => {
        if(this.props.app_id !== undefined){
          return update(state, {apps: {$splice: [[this.props.app_id, 1]]}});
        }
      });
  }

}

AuthAppRow.propTypes = {
  app_name: PropTypes.string,
  app_created: PropTypes.string,
  app_is_auth: PropTypes.bool,
  app_scope_id: PropTypes.string,
  app_id: PropTypes.string
};

export default AuthAppRow;