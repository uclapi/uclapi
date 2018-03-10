import React from 'react';
import {CopyField} from './../dashboard/copyField.jsx';
import OAuthScopesForm from './OAuthScopesForm.jsx';
import OAuthCallbackField from './OAuthCallbackField.jsx';

class OAuth extends React.Component {

  render() {
    return (
      <div>
        <a href="/docs">Read about how OAuth works</a>.<br/><br/>
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
          <a href="/docs#oauth/scopes">Scopes documentation</a>
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

export default OAuth;
