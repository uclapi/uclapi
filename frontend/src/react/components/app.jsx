import React from 'react';
import update from 'immutability-helper';
import 'whatwg-fetch';
import Cookies from 'js-cookie';
import {EditableTextField} from './editableTextField.jsx';
import {CopyField, CopyActionField} from './copyField.jsx';
import {RelativeDate} from './relativeDate.jsx';
import Collapse, { Panel } from 'rc-collapse';

const defaultHeaders = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-CSRFToken':Cookies.get('csrftoken') 
};

class AppNameField extends EditableTextField {
  constructor(props){
    super(props);

    this.handleSubmit = this.handleSubmit.bind(this);
    this.updateName = this.updateName.bind(this);
  }

  updateName(data){
    let values = {
      name: this.state.value,
      updated: data.date
    };
    this.props.update(this.props.appId, values);
    this.setState({
      value:'',
      editing: false,
    });
  }

  handleSubmit(e){
    e.preventDefault();
    fetch('/dashboard/api/rename/', {
      method: 'POST',
      credentials: 'include',
      headers: defaultHeaders,
      body: 'new_name=' + this.state.value +
        '&app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){return res.json();} 
      throw new Error('An error occured');
    }).then((json)=>{
      if(json.success){
        this.updateName(json);
        return;
      }
      throw new Error(json.message);
    }).catch((err)=>{
      this.props.setError(err.message);
    });
  }
}

class DeleteButton extends React.Component {
  constructor(props){
    super(props);
    this.deleteConfirm = this.deleteConfirm.bind(this);
  }

  deleteConfirm(e){
    e.preventDefault();
    if(confirm('Are you sure you want to delete this app?')){
      this.deleteApp();
    }
  }

  deleteApp(){
    fetch('/dashboard/api/delete/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){
        return res.json();
      }else{
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        this.props.remove(this.props.appId);
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      this.props.setError(err.message);
    });
  }

  render(){
    return(
      <button className="pure-button button-error padded" onClick={this.deleteConfirm}>
        <i className="fa fa-trash-o" aria-hidden="true"></i>
      </button>
    );
  }
}

DeleteButton.propTypes = {
  appId: React.PropTypes.string.isRequired,
  remove: React.PropTypes.func.isRequired,
  setError: React.PropTypes.func
};

class OAuthCallbackField extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      callbackUrl: this.props.callbackUrl ? this.props.callbackUrl: '',
      saved: false
    };

    this.updateCallbackUrl = this.updateCallbackUrl.bind(this);
    this.saveCallbackUrl = this.saveCallbackUrl.bind(this);
  }

  updateCallbackUrl(e){
    this.setState({
      callbackUrl: e.target.value
    });
  }

  saveCallbackUrl(e){
    e.preventDefault();

    fetch('/dashboard/api/setcallbackurl/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId + '&callback_url=' + encodeURIComponent(this.state.callbackUrl)
    }).then((res)=>{
      if(res.ok){
        return res.json();
      }else{
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        this.setState({
          saved: true,
        });
        setTimeout(()=>{this.setState({saved:false});}, 5000);
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      this.props.setError(err.message);
    });
  }

  render(){
    return(
      <form className="pure-form pure-g">
        <div className="pure-u-3-4">
          <input 
            type="text"
            ref="callbackUrl"
            className="pure-input-1"
            value={this.state.callbackUrl}
            style={{ 'borderRadius': '4px 0px 0px 4px'}}
            onChange={this.updateCallbackUrl}
          />
        </div>
        <div className="pure-u-1-4">
          <button 
            className="pure-button pure-button-primary pure-input-1 tooltip"
            onClick={this.saveCallbackUrl}
            style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
          >
            <i className="fa fa-save" aria-hidden="true"></i>
            <span>{this.state.saved?'Saved!':'Click to save the Callback URL'}</span>
          </button>
        </div>
      </form>
    );
  }
}

OAuthCallbackField.propTypes = {
  callbackUrl: React.PropTypes.string,
  appId: React.PropTypes.string.isRequired,
  setError: React.PropTypes.func
};

class OAuthScopesForm extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      scopes: this.props.scopes,
      scopesSaved: false
    };
    this.handleScopeChange = this.handleScopeChange.bind(this);
    this.submitScopes = this.submitScopes.bind(this);
  }

  handleScopeChange(e){
    e.persist();
    this.setState((state)=>{
      return update(state, {scopes:{[e.target.name]:{enabled: {$set: e.target.checked}}}});
    });
  }

  submitScopes(e){
    e.preventDefault();

    var scopesData = [];

    for (const scope of this.state.scopes) {
      scopesData.push(
        {
          'name': scope.name,
          'checked': scope.enabled
        }
      );
    }

    var json = JSON.stringify(scopesData);

    fetch('/dashboard/api/updatescopes/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId + '&scopes=' + encodeURIComponent(json)
    }).then((res)=>{
      if (res.ok) {
        return res.json();
      }
      throw new Error('An error occured');
    }).then((json)=> {
      if (!json.success) {
        throw new Error(json.message);
      }
      this.setState({
        scopesSaved: true
      });
      setTimeout(()=>{this.setState({scopesSaved: false});}, 5000);
    }).catch((err)=>{
      this.props.setError(err.message);
    });
  }

  render(){
    return(
      <form onSubmit={this.submitScopes} className="pure-for">
        {this.state.scopes.map((scope, index)=>{
          return <div key={index}>
              <input 
                type="checkbox"
                onChange={this.handleScopeChange}
                defaultChecked={scope.enabled} 
                name={index} 
                className="scope-checkbox"
              />
              {scope.description}
            </div>;
        })}
        <button
          type="submit"
          className="pure-button pure-button-primary pure-input-1 tooltip"
          onMouseEnter={this.setSaveScopes}
          style={{ 'border': '1px solid #ccc', 'borderRadius': '0px' }}
        >
          <i className="fa fa-save" aria-hidden="true"></i>
          <span>{this.state.scopesSaved?'Saved!':'Click to save changes to the requested permissions.'}</span>
        </button>
      </form>

    );
  }

}

OAuthScopesForm.propTypes = {
  scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
  appId: React.PropTypes.string.isRequired,
  setError: React.PropTypes.func
};

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
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken':Cookies.get('csrftoken') 
      },
      body: 'app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){
        return res.json();
      } else {
        throw new Error('Unable to regen token');
      }
    }).then((json)=>{
      if(json.success){
        let values = {
          token: json.app.token,
          updated: json.app.date
        };
        this.props.update(that.props.appId, values);
        this.setState({
          error:''
        });
      }else{
        throw new Error(json.message);
      }
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
        <RelativeDate date={this.props.created} label={"Created: "} />
        <RelativeDate date={this.props.updated} label={"Updated: "} />
        <Collapse>
          <Panel header="OAuth Settings" showArrow={true}>
            <div>
              OAuth allows you to create apps that provide users with personal data.
              More information can be found in the <a href="https://docs.uclapi.com">docs</a>.<br/><br/>
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
                The scope defines which personal data your application will be able to access.
                For more information, please consult the <a href="https://uclapi.com/docs">docs</a>
                for more details on scope.
              </em>
              <OAuthScopesForm
                scopes={this.props.scopes}
                appId={this.props.appId}
                setError={this.setError}
              />
            </div>
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
  update: React.PropTypes.func.isRequired,
  remove: React.PropTypes.func.isRequired,
  clientId: React.PropTypes.string.isRequired,
  clientSecret: React.PropTypes.string.isRequired,
  callbackUrl: React.PropTypes.string.isRequired,
  scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired
};

export {App};
