import React from 'react';
import PropTypes from 'prop-types';

class LogInButton extends React.Component {
  render () {
    return <div class="sign-in-form">
      <div class="pure-u-1">
        <div class="card flexCentre">
          <form class="pure-form pure-form-stacked" action={this.props.url} method="post">
          <h1>Log in to handle app settings</h1>{"\n"}
            <pure-g>
            <div class="pure-u-md-1-4"></div>
            <div class="pure-u-1 pure-u-md-1-2 centered">
              <fieldset>
                <button type="submit" class="pure-button pure-button-primary">Log In</button>
              </fieldset>
            </div>
            <div class="pure-u-md-1-4"></div>
            </pure-g>
          </form>
        </div>
      </div>
  </div>;
  }
}

LogInButton.propTypes = {
  url: PropTypes.string
};

export default LogInButton;