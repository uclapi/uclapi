import React from 'react';
import {CopyField} from './../copyField.jsx';
import OAuthScopesForm from './OAuthScopesForm.jsx';
import OAuthCallbackField from './OAuthCallbackField.jsx';

class OAuth extends React.Component {

  render() {
    return (
      <div>
        <a href="https://uclapi.com/docs">Read about how OAuth works</a>.<br/><br/>
        Client ID
        <CopyField val={this.props.clientId}/>
        Client Secret
        <CopyField val={this.props.clientSecret}/>

        Callback URL
        <OAuthCallbackField
          callbackUrl={this.props.callbackUrl}
          appId={this.props.appId}
          setError={this.setError}
        />
        <h4>OAuth Scope</h4>
        <em>
          <a href="https://uclapi.com/docs#oauth/scopes">Scopes documentation</a>
        </em>
        <OAuthScopesForm
          scopes={this.props.scopes}
          appId={this.props.appId}
          setError={this.setError}
        />
      </div>
    );
  }
}

OAuth.propTypes = {
  appId: React.PropTypes.string.isRequired,
  clientId: React.PropTypes.string.isRequired,
  clientSecret: React.PropTypes.string.isRequired,
  callbackUrl: React.PropTypes.string.isRequired,
  scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired
};

export default OAuth;
