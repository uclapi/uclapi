import React from 'react';
import PropTypes from 'prop-types';

class LogInButton extends React.Component {
  render () {
    return
    <div class="pure-u-md-1-4"></div>
      <div class="pure-u-1 pure-u-md-1-2 centered">
        <h1>Log in to handle app settings</h1>
        <div class="card flexCentre">
          <form class="pure-form pure-form-stacked" action="/oauth/appsettings" method="post">
            <fieldset>
              <div class="well left">
              </div>
              //<input id="remember" name="agreement" value="True" hidden></input>
              <button type="submit" class="pure-button pure-button-primary">Log In</button>
            </fieldset>
          </form>
        </div>
      </div>
    <div class="pure-u-md-1-4"></div>;
  }
}

LogInButton.propTypes = {
  status: PropTypes.string,
};

export default LogInButton;