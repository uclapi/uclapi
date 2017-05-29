import React from 'react';
import update from 'immutability-helper';
import 'whatwg-fetch';
import Cookies from 'js-cookie';
import moment from 'moment';
import Modal from 'react-modal';
import Collapse, { Panel } from 'rc-collapse';

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
      callbackUrl: this.props.callbackUrl == null ? '' : this.props.callbackUrl
    };
    this.changeName = this.changeName.bind(this);
    this.editName = this.editName.bind(this);
    this.regenToken = this.regenToken.bind(this);
    this.regenConfirm = this.regenConfirm.bind(this);
    this.deleteApp = this.deleteApp.bind(this);
    this.deleteConfirm = this.deleteConfirm.bind(this);
    this.stopEditing = this.stopEditing.bind(this);
    this.copyToken = this.copyToken.bind(this);
    this.copyClientId = this.copyClientId.bind(this);
    this.copyClientSecret = this.copyClientSecret.bind(this);
    this.setCopyTextToken = this.setCopyTextToken.bind(this);
    this.setCopyTextClientId = this.setCopyTextClientId.bind(this);
    this.setCopyTextClientSecret = this.setCopyTextClientSecret.bind(this);
    this.setSaveCallbackUrl = this.setSaveCallbackUrl.bind(this);
    this.updateCallbackUrl = this.updateCallbackUrl.bind(this);
    this.saveCallbackUrl = this.saveCallbackUrl.bind(this);
    this.updateRoomBookingsScope = this.updateRoomBookingsScope.bind(this);
    this.updateTimetableScope = this.updateTimetableScope.bind(this);
    this.updateUcluScope = this.updateUcluScope.bind(this);

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
        let newApp = {
          name: that.refs.name.value,
          id: that.props.appId,
          token: that.props.appKey,
          created: that.props.created,
          updated: json.date
        };
        that.props.update(that.props.appId, newApp);
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
        let newApp = {
          name: that.props.name,
          id: that.props.appId,
          token: json.app.token,
          created: that.props.created,
          updated: json.app.date
        };
        that.props.update(that.props.appId, newApp);
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
        that.props.remove(that.props.appId);
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  deleteConfirm(e){
    e.preventDefault();
    if(confirm('Are you sure you want to delete this app?')){
      this.deleteApp();
    }
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

  copyToken(e){
    e.preventDefault();

    let tokenElement = this.refs.apiToken;
    tokenElement.select();

    try {
      // copy text
      document.execCommand('copy');
      this.setState({
        tokenCopied: true
      });
      tokenElement.blur();
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
  }

  copyClientId(e){
    e.preventDefault();

    let clientIdElement = this.refs.clientId;
    clientIdElement.select();

    try {
      // copy text
      document.execCommand('copy');
      this.setState({
        clientIdCopied: true
      });
      clientIdElement.blur();
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
  }

  copyClientSecret(e){
    e.preventDefault();

    let clientSecretElement = this.refs.clientSecret;
    clientSecretElement.select();

    try {
      // copy text
      document.execCommand('copy');
      this.setState({
        clientSecretCopied: true
      });
      clientSecretElement.blur();
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
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
          callbackUrlSaved: true
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

  setCopyTextToken(){
    this.setState({
      tokenCopied: false
    });
  }

  setCopyTextClientId(){
    this.setState({
      clientIdCopied: false
    });
  }

  setCopyTextClientSecret(){
    this.setState({
      clientSecret: false
    });
  }

  setSaveCallbackUrl() {
    this.setState({
      callbackUrlSaved: false
    })
  }

  updateRoomBookingsScope(e){
    let that = this;

    fetch('/dashboard/api/setscope/roombookings/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId + '&scope_status=' + e.target.checked
    }).then((res)=>{
      if(res.ok){
        return res.json();
      }else{
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        // State Set OK
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  updateTimetableScope(e){
    let that = this;

    fetch('/dashboard/api/setscope/timetable/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId + '&scope_status=' + e.target.checked
    }).then((res)=>{
      if(res.ok){
        return res.json();
      }else{
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        // State Set OK
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      that.setState({
        error: err.message
      });
    });
  }

  updateUcluScope(e){
    let that = this;

    fetch('/dashboard/api/setscope/uclu/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: 'app_id=' + this.props.appId + '&scope_status=' + e.target.checked
    }).then((res)=>{
      if(res.ok){
        return res.json();
      }else{
        throw new Error('An error occured');
      }
    }).then((json)=>{
      if(json.success){
        // State Set OK
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
    return <div className="app pure-u-1 pure-u-xl-1-2">
      <div className="card">
        {this.state.editing ? (
          <form className="pure-form" onSubmit={this.changeName}>
            <fieldset>
              <input type="text" autoFocus placeholder={this.props.name} ref="name"/>
              <button type="submit" className="pure-button pure-button-primary padded" onClick={this.changeName}>Submit</button>
              <button className="pure-button button-error padded" onClick={this.stopEditing}>Cancel</button>
            </fieldset>
          </form> 
        ):(
          <div className="pure-g">
            <div className="pure-u-1-2">
              <h2>{this.props.name}</h2>
            </div>
            <div className="pure-u-1-2 flexTopRight">
              <button className="pure-button pure-button-primary padded" onClick={this.editName}>
                <i className="fa fa-pencil" aria-hidden="true"></i>
              </button>
              <button className="pure-button button-error padded" onClick={this.deleteConfirm}>
                <i className="fa fa-trash-o" aria-hidden="true"></i>
              </button>
            </div>
          </div>
        )}
        <div className="pure-g">
          <div className="pure-u-1">
            API Token
            <form className="pure-form pure-g">
              <div className="pure-u-2-3">
                <input 
                  type="text"
                  ref="apiToken"
                  className="pure-input-1"
                  value={this.props.appKey}
                  readOnly
                  style={{ 'borderRadius': '4px 0px 0px 4px'}}
                />
              </div>
              <div className="pure-u-1-6">
                <button 
                  className="pure-button pure-button-primary pure-input-1 tooltip"
                  onClick={this.copyToken}
                  onMouseEnter={this.setCopyTextToken}
                  style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
                >
                  <i className="fa fa-clipboard" aria-hidden="true"></i>
                  <span>{this.state.tokenCopied?'Copied!':'Click to copy to clipboard'}</span>
                </button>
              </div>
              <div className="pure-u-1-6">
                <button 
                  className="pure-button pure-button-primary pure-input-1" 
                  onClick={this.regenConfirm}
                  style={{ 'border': '1px solid #ccc', 'borderRadius': '0px 4px 4px 0px'}}
                >
                  <i className="fa fa-refresh" aria-hidden="true"></i>
                </button>
              </div>
            </form>
          </div>
        </div>
        <p title={moment(this.props.created).format('dddd, Do MMMM YYYY, h:mm:ss a')}>Created: {moment(this.props.created).fromNowOrNow()}</p>
        <p title={moment(this.props.updated).format('dddd, Do MMMM YYYY, h:mm:ss a')}>Updated: {moment(this.props.updated).fromNowOrNow()}</p>
        <Collapse>
          <Panel header="OAuth Settings"
                 showArrow={true}>
            <div>
              OAuth allows you to create apps that provide users with personal data.
              More information can be found in the <a href="https://docs.uclapi.com">docs</a>.<br/><br/>
              Client ID
              <form className="pure-form pure-g">
                <div className="pure-u-3-4">
                  <input 
                    type="text"
                    ref="clientId"
                    className="pure-input-1"
                    value={this.props.clientId}
                    readOnly
                    style={{ 'borderRadius': '4px 0px 0px 4px'}}
                  />
                </div>
                <div className="pure-u-1-4">
                  <button 
                    className="pure-button pure-button-primary pure-input-1 tooltip"
                    onClick={this.copyClientId}
                    onMouseEnter={this.setCopyTextClientId}
                    style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
                  >
                    <i className="fa fa-clipboard" aria-hidden="true"></i>
                    <span>{this.state.clientIdCopied?'Copied!':'Click to copy to clipboard'}</span>
                  </button>
                </div>
              </form>

              Client Secret
              <form className="pure-form pure-g">
                <div className="pure-u-3-4">
                  <input 
                    type="text"
                    ref="clientSecret"
                    className="pure-input-1"
                    value={this.props.clientSecret}
                    readOnly
                    style={{ 'borderRadius': '4px 0px 0px 4px'}}
                  />
                </div>
                <div className="pure-u-1-4">
                  <button 
                    className="pure-button pure-button-primary pure-input-1 tooltip"
                    onClick={this.copyClientSecret}
                    onMouseEnter={this.setCopyTextClientSecret}
                    style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
                  >
                    <i className="fa fa-clipboard" aria-hidden="true"></i>
                    <span>{this.state.clientSecretCopied?'Copied!':'Click to copy to clipboard'}</span>
                  </button>
                </div>
              </form>

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
              <input type="checkbox" onChange={this.updateRoomBookingsScope} defaultChecked={this.props.privateRoomBookings} /> Personal Room Bookings<br/>
              <input type="checkbox" onChange={this.updateTimetableScope} defaultChecked={this.props.privateTimetable} /> Personal Timetable<br/>
              <input type="checkbox" onChange={this.updateUcluScope} defaultChecked={this.props.privateUclu} /> Personal UCLU Data<br/>
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
  privateRoomBookings: React.PropTypes.bool.isRequired,
  privateTimetable: React.PropTypes.bool.isRequired,
  privateUclu: React.PropTypes.bool.isRequired
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
    this.setState( (state) => 
      update(state, {apps: {$push: [app]}})
    );
  }

  updateApp(id, app){
    this.setState( (state) => {
      let appIndex = this.getAppIndex(id);
      if(appIndex !== undefined){
        return update(state, {apps: {[appIndex]: {$set: app}}});          
      }
    });
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
            privateRoomBookings={app.oauth.scope.private_roombookings}
            privateTimetable={app.oauth.scope.private_timetable}
            privateUclu={app.oauth.scope.private_uclu}
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
