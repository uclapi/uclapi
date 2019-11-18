import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';

import Button from '@material-ui/core/Button';

class AuthAppRow extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      app: props.app,
      isVisible: true
    };
    this.handleChange = this.handleChange.bind(this);
    this.deauthoriseApp = this.deauthoriseApp.bind(this);
  }

  render () {
    this.button_text = "Revoke Permissions"
    if(!this.state.isVisible) {this.button_text="App Disabled"}

    return <div className="auth-app">
            <div className="app-information">
              <h3>{this.props.app_name}</h3>
              <h3>{this.props.app_created}</h3>
            </div>

            <div className="app-permission-box">
              <Button disabled={!this.state.isVisible}
                      size="medium" 
                      color="primary"
                      onClick={this.handleChange}>
                {this.button_text}
              </Button>
            </div>
          </div>;
  }

  handleChange (event, checked) {
      // Add toast to confirm deauthorisation
      if(confirm('Are you sure you want to deauthorise this app?')){
        this.deauthoriseApp();
      }
  }

  deauthoriseApp() {
      // Call function in back end to delete scope
      axios.get('/oauth/deauthorise', {
        params: {
          client_id: this.props.app_client_id
        },
        xsrfHeaderName: "X-CSRFToken",
      }).then(response => {
          // Log success in console
          console.log("Successfully de-authorised app: ")
          console.log(response)

          this.setState({
            isVisible: false,
          })
      }).catch(error => {
          // Handle error
          console.log(error);
      })
  }

}

AuthAppRow.propTypes = {
  app_name: PropTypes.string,
  app_created: PropTypes.string,
  app_is_auth: PropTypes.bool,
  app_id: PropTypes.string
};

export default AuthAppRow;
