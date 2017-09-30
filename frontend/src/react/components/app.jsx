import React from 'react';
import 'whatwg-fetch';
import Collapse, { Panel } from 'rc-collapse';

import {CopyActionField} from './copyField.jsx';
import RelativeDate from './relativeDate.jsx';
import AppNameField from './app/AppNameField.jsx';
import DeleteButton from './app/DeleteButton.jsx';
import defaultHeaders from './app/defaultHeaders.js';
import OAuth from './app/OAuth.jsx';
import Webhook from './app/Webhook.jsx';

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      error: '',
    };
    this.regenToken = this.regenToken.bind(this);
    this.regenConfirm = this.regenConfirm.bind(this);
    this.setError = this.setError.bind(this);
  }

  setError(msg){
    this.setState({
      error: msg
    });
    setTimeout(()=>{this.setState({error:''});}, 5000);
  }

  regenToken(){
    let that = this;
    fetch('/dashboard/api/regen/', {
      method: 'POST',
      credentials: 'include',
      headers: defaultHeaders,
      body: 'app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){ return res.json(); }
      throw new Error('Unable to regen token.');
    }).then((json)=>{
      if(json.success){
        let values = {
          token: json.app.token,
          updated: json.app.date
        };
        this.props.update(that.props.appId, values);
        return;
      }
      throw new Error(json.message);
    }).catch((err)=>{
      this.setError(err.message);
    });
  }

  regenConfirm(e){
    e.preventDefault();
    if(confirm('Are you sure you want to regenerate your api token?')){
      this.regenToken();
    }
  }

  render () {
    return <div className="app pure-u-1 pure-u-xl-1-2">
      <div className="card">
        <div className="pure-g">
          <div className="pure-u-1-2">
            <AppNameField
              origValue={this.props.name}
              update={this.props.update}
              appId={this.props.appId}
              setError={this.setError}
            />
          </div>
          <div className="pure-u-1-2">
            <div style={{float: 'right'}}>
              <DeleteButton
                appId={this.props.appId}
                remove={this.props.remove}
                setError={this.setError}
              />
            </div>
          </div>
        </div>
        <div className="pure-g">
          <div className="pure-u-1">
            API Token
            <CopyActionField
              setError={this.setError}
              val={this.props.appKey}
              action={this.regenConfirm}
              icon="fa fa-refresh"
            />
          </div>
        </div>
        <div>
          <RelativeDate date={this.props.created} label={'Created: '} />
          <RelativeDate date={this.props.updated} label={'Last Updated: '} />
        </div>
        <Collapse>
          <Panel header="OAuth Settings" showArrow>
            <OAuth
              appId={this.props.appId}
              clientId={this.props.oauth.clientId}
              clientSecret={this.props.oauth.clientSecret}
              callbackUrl={this.props.oauth.callbackUrl}
              scopes={this.props.oauth.scopes}
            />
          </Panel>
          <Panel header="Webhook Settings" showArrow>
            <Webhook
              url={this.props.webhook.url}
              siteid={this.props.webhook.siteid}
              roomid={this.props.webhook.roomid}
              contact={this.props.webhook.contact}
              verification_secret={this.props.webhook.verification_secret}
              appId={this.props.appId}
            />
          </Panel>
        </Collapse>
        <label className="error">{this.state.error}</label>
        </div>
    </div>;
  }
}

App.propTypes = {
  name: React.PropTypes.string.isRequired,
  appId: React.PropTypes.string.isRequired,
  appKey: React.PropTypes.string.isRequired,
  created: React.PropTypes.string.isRequired,
  updated: React.PropTypes.string.isRequired,
  webhook: React.PropTypes.shape({
    verification_secret: React.PropTypes.string.isRequired,
    url: React.PropTypes.string.isRequired,
    siteid: React.PropTypes.string.isRequired,
    roomid: React.PropTypes.string.isRequired,
    contact: React.PropTypes.string.isRequired,
  }),
  oauth: React.PropTypes.shape({
    clientId: React.PropTypes.string.isRequired,
    clientSecret: React.PropTypes.string.isRequired,
    callbackUrl: React.PropTypes.string.isRequired,
    scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired
  }),
  update: React.PropTypes.func.isRequired,
  remove: React.PropTypes.func.isRequired,
};

export {App};
