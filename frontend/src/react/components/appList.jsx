import React from 'react';
import update from 'immutability-helper';
import 'whatwg-fetch';
import Cookies from 'js-cookie';
import moment from 'moment';
import Modal from 'react-modal';
import Collapse, { Panel } from 'rc-collapse';
import {CopyField, CopyActionField} from './copyField.jsx';

const defaultHeaders = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-CSRFToken':Cookies.get('csrftoken') 
}

class EditableTextField extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: '',
      editing: false
    }

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(e){
    e.preventDefault();
    this.setState({value: e.target.value});
  }

  render(){
    return(<div>
      {this.state.editing ? (
        <form className="pure-form" onSubmit={this.handleSubmit}>
          <fieldset>
            <input 
              type="text"
              autoFocus
              placeholder={this.props.origValue}
              value={this.state.value}
              onChange={this.handleChange}
            />
            <button 
              type="submit" 
              className="pure-button pure-button-primary padded" 
              onClick={this.handleSubmit}
            >
              Submit
            </button>
            <button 
              className="pure-button button-error padded"
              onClick={()=>this.setState({editing:false})}
            >
              Cancel
            </button>
          </fieldset>
        </form> 
      ):(
        <div>
          <h2 style={{display:'inline', verticalAlign: 'middle'}}>{this.props.origValue}</h2>
          <button
            className="pure-button button-primary-inverted"
            onClick={()=>this.setState({editing:true})}
          >
            <i className="fa fa-pencil" aria-hidden="true"></i>
          </button>
        </div>
      )}
    </div>);
  }

}

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
    let that = this;
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
      that.setState({
        error: err.message
      });
    });
  }
}

class OAuthCallbackField extends EditableTextField {

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
    let that = this;
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
      that.setState({
        error: err.message
      });
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

class RelativeDate extends React.Component {
  constructor(props){
    super(props);

    /*
      Make moment.js say 'just now' if the time difference is less
      than five seconds either way to get round non-sync'd server and
      client time.
      This may make 'a few seconds ago' somewhat redundant, but it's
      worth it.
    */
    moment.fn.fromNowOrNow = function(a) {
      if (Math.abs(moment().diff(this)) < 5000) {
        return 'just now';
      }
      return this.fromNow(a);
    };
  }

  render(){
    return(
      <div 
        title={moment.utc(this.props.date).local().format('dddd, Do MMMM YYYY, h:mm:ss a')}
      >
        {this.props.label} {moment.utc(this.props.date).local().fromNowOrNow()}
      </div>
    )
  }
}

class OAuthScopesForm extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      scopes: this.props.scopes
    }
  }

  handleScopeChange(e){
    e.preventDefault();
    
    this.setState((state)=>{
      return update(state, {scopes:{[e.target.key]:{$set: e.target.checked}}});
    });
  }

  submitScopes(e){
    e.preventDefault();

    let that = this;

    var scopesData = [];

    for (var i = 0; i < this.state.scopes.length; i++) {
      scopesData.push(
        {
          "name": this.state.scopes[i].name,
          "checked": this.state.scopes[i].enabled
        }
      )
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
        return res.json()
      } else {
        throw new Error('An error occured');
      }
    }).then((json)=> {
      if (!json.success) {
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  render(){
    return(
      <form onSubmit={this.submitScopes} className="pure-for">
        {this.state.scopes.map((scope, index)=>{
          return <input 
                   key={index}
                   type="checkbox"
                   onChange={this.handleScopeChange}
                   ref={"scope"+index}
                   defaultChecked={scope.enabled} 
                   name={"scope~" + scope.name} 
                   className="scope-checkbox"
                 >
                   {scope.description}
                 </input>;
        })}
      </form>

    );
  }

}

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      editing: false,
      tokenCopied: false,
      clientIdCopied: false,
      clientSecretCopied: false,
      callbackUrlSaved: false,
      error: '',
      callbackUrl: this.props.callbackUrl == null ? '' : this.props.callbackUrl,
      scopes: this.props.scopes,
      scopesSaved: false
    };
    this.changeName = this.changeName.bind(this);
    this.editName = this.editName.bind(this);
    this.regenToken = this.regenToken.bind(this);
    this.regenConfirm = this.regenConfirm.bind(this);
    this.stopEditing = this.stopEditing.bind(this);
    this.setSaveCallbackUrl = this.setSaveCallbackUrl.bind(this);
    this.updateCallbackUrl = this.updateCallbackUrl.bind(this);
    this.saveCallbackUrl = this.saveCallbackUrl.bind(this);
    this.setSaveScopes = this.setSaveScopes.bind(this);
    this.handleScopeCheckChange = this.handleScopeCheckChange.bind(this);
    this.saveScopes = this.saveScopes.bind(this);


  }

  changeName(e){
    e.preventDefault();
    let that = this;
    fetch('/dashboard/api/rename/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken':Cookies.get('csrftoken') 
      },
      body: 'new_name=' + this.refs.name.value +
        '&app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){
        return res.json();
      } else {
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        let values = {
          name: that.refs.name.value,
          updated: json.date
        };
        that.props.update(that.props.appId, values);
        that.refs.name.value = '';
        that.setState({
          editing: false,
          error: ''
        });
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
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
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        let values = {
          token: json.app.token,
          updated: json.app.date
        };
        that.props.update(that.props.appId, values);
        that.setState({
          error:''
        });
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }


  regenConfirm(e){
    e.preventDefault();
    if(confirm('Are you sure you want to regenerate your api token?')){
      this.regenToken();
    }
  }

  editName(e){
    e.preventDefault();
    this.setState({
      editing: true
    });
  }

  stopEditing(e){
    e.preventDefault();
    this.setState({
      editing: false
    });
  }

  updateCallbackUrl(e){
    this.setState({
      callbackUrl: e.target.value
    });
  }

  saveCallbackUrl(e){
    e.preventDefault();

    let that = this;

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
        that.setState({
          callbackUrlSaved: true,
          error:''
        })
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  setSaveCallbackUrl() {
    this.setState({
      callbackUrlSaved: false
    })
  }

  setSaveScopes() {
    this.setState({
      scopesSaved: false
    })
  }

  saveScopes(e) {
    let that = this;

    var scopesData = [];

    for (var i = 0; i < this.state.scopes.length; i++) {
      scopesData.push(
        {
          "name": this.state.scopes[i].name,
          "checked": this.state.scopes[i].enabled
        }
      )
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
        return res.json()
      } else {
        throw new Error('An error occured');
      }
    }).then((json)=> {
      if (json.success) {
        this.setState({
          scopesSaved: true,
          error: ''
        })
      } else {
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  handleScopeCheckChange(e) {
    let that = this;

    var s = e.target.name.split('~')[1];
    var index = -1;
    for (var i = 0; i < this.state.scopes.length; i++) {
      if (this.state.scopes[i].name == s) {
        index = i;
        break;
      }
    }
    this.state.scopes[i].enabled = e.target.checked;
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
            />
          </div>
          <div className="pure-u-1-2">
            <div style={{float: 'right'}}>
              <DeleteButton
                appId={this.props.appId}
                remove={this.props.remove}
              />
            </div>
          </div>
        </div>
        <div className="pure-g">
          <div className="pure-u-1">
            API Token
            <CopyActionField val={this.props.appKey} action={this.regenConfirm} icon="fa fa-refresh" />
          </div>
        </div>
        <RelativeDate date={this.props.created} label={"Created: "} />
        <RelativeDate date={this.props.updated} label={"Updated: "} />
        <Collapse>
          <Panel header="OAuth Settings"
                 showArrow={true}>
            <div>
              OAuth allows you to create apps that provide users with personal data.
              More information can be found in the <a href="https://docs.uclapi.com">docs</a>.<br/><br/>
              Client ID
              <CopyField val={this.props.clientId}/>
              Client Secret
              <CopyField val={this.props.clientSecret}/>

              Callback URL
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
                    onMouseEnter={this.setSaveCallbackUrl}
                    style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
                  >
                    <i className="fa fa-save" aria-hidden="true"></i>
                    <span>{this.state.callbackUrlSaved?'Saved!':'Click to save the Callback URL'}</span>
                  </button>
                </div>
              </form>
              <br/>
              <br/>
              <h4>OAuth Scope</h4>
              <em>
                The scope defines which personal data your application will be able to access.
                For more information, please consult the <a href="https://uclapi.com/docs">docs</a> for more details on scope.
              </em><br/><br/>
              <div>
                {
                  this.state.scopes.map((scope, index) => {
                    return <div key={index}><input 
                                  type="checkbox"
                                  onChange={this.handleScopeCheckChange}
                                  ref={"scope"+index}
                                  defaultChecked={scope.enabled} 
                                  name={"scope~" + scope.name} 
                                  className="scope-checkbox"
                                />
                                  {scope.description}
                                </div>;
                  })
                }
              </div>
              <button
                className="pure-button pure-button-primary pure-input-1 tooltip"
                onClick={this.saveScopes}
                onMouseEnter={this.setSaveScopes}
                style={{ 'border': '1px solid #ccc', 'borderRadius': '0px' }}
              >
                <i className="fa fa-save" aria-hidden="true"></i>
                <span>{this.state.scopesSaved?'Saved!':'Click to save changes to the requested permissions.'}</span>
              </button>
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

class AppForm extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      error: ''
    };
    this.submitForm = this.submitForm.bind(this);
  }

  submitForm(e){
    e.preventDefault();
    let that = this;
    fetch('/dashboard/api/create/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken':Cookies.get('csrftoken') 
      },
      body: 'name=' + this.refs.name.value
    }).then((res)=>{
      if(res.ok){
        return res.json();
      } else {
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        let newApp = json.app;
        newApp['name'] = that.refs.name.value;
        that.refs.name.value = '';
        that.props.add(newApp);
        that.props.close();
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }
  render () {
    return <div className="appForm">
      <h2>Create App</h2>
      <form className="pure-form pure-form-stacked" onSubmit={this.submitForm}>
        <fieldset>
          <div className="pure-g">
            <div className="pure-u-1">
              <label htmlFor="name">App Name</label>
              <input autoFocus id="name" ref="name" className="pure-u-1" type="text"/>
            </div>
          </div>
          <div className="pure-g">
            <div className="pure-u-1-24"></div>
            <button type="submit" className="pure-button pure-button-primary pure-u-10-24">Create</button>
            <div className="pure-u-2-24"></div>
            <button type="button" className="pure-button button-error pure-u-10-24" onClick={this.props.close}>Cancel</button>
            <div className="pure-u-1-24>"></div>
          </div>
          <label className="error">{this.state.error}</label>
        </fieldset>
      </form>
    </div>;
  }
}

AppForm.propTypes = {
  add: React.PropTypes.func.isRequired,
  close: React.PropTypes.func.isRequired
};

class AppList extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      apps: props.apps,
      showCreate: false
    };
    this.addApp = this.addApp.bind(this);
    this.updateApp = this.updateApp.bind(this);
    this.getAppIndex = this.getAppIndex.bind(this);
    this.clickHandler = this.clickHandler.bind(this);
    this.deleteApp = this.deleteApp.bind(this);

    this.showForm = this.showForm.bind(this);
    this.hideForm = this.hideForm.bind(this);
  }

  addApp(app){
    this.setState((state) => update(state, {apps: {$push: [app]}}));
  }

  updateApp(id, values){
    let appIndex = this.getAppIndex(id);
    if(appIndex !== undefined){
      Object.keys(values).forEach((key)=>{
        this.setState((state) => {
          return update(state, {apps: {[appIndex]: {[key]:{$set: values[key]}}}});          
        });
      });
    }
  }

  deleteApp(appId){
    this.setState((state) => {
      let appIndex = this.getAppIndex(appId);
      if(appIndex !== undefined){
        return update(state, {apps: {$splice: [[appIndex, 1]]}});
      }
    });
  }

  getAppIndex(appId){
    for(let app of this.state.apps){
      if(app.id === appId){
        return this.state.apps.indexOf(app);
      }
    }
  }

  clickHandler(e){
    e.preventDefault();
    this.deleteApp('My Cool App');
  }

  showForm(){
    this.setState({showCreate: true});
  }

  hideForm(){
    this.setState({showCreate: false});
  }

  render () {
    return <div className="appList pure-u-1">
      <div className="pure-g">
        {this.state.apps.map((app, i) => {
          return <App name={app.name}
            appId={app.id}
            appKey={app.token}
            created={app.created}
            updated={app.updated}
            key={i}
            update={this.updateApp}
            remove={this.deleteApp}
            clientId={app.oauth.client_id}
            clientSecret={app.oauth.client_secret}
            callbackUrl={app.oauth.callback_url}
            scopes={app.oauth.scopes}
          />;
        })}
      </div>
      <Modal
        isOpen={this.state.showCreate}
        contentLabel="Create app form"
        onRequestClose={this.hideForm}
				className="Modal"
				overlayClassName="Overlay"
      >
        <AppForm add={this.addApp} close={this.hideForm}/>
      </Modal>
      <div className="flexCentre">
        <button className="roundButton" onClick={this.showForm}>+</button>
      </div>
    </div>;
  }
}

AppList.propTypes = {
  apps: React.PropTypes.array.isRequired
};

export default AppList;
