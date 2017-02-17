import React from 'react';
import update from 'immutability-helper';
import 'whatwg-fetch';
import Cookies from 'js-cookie';
import moment from 'moment';

class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      editing: false,
      copied: false
    };
    this.changeName = this.changeName.bind(this);
    this.editName = this.editName.bind(this);
    this.regenToken = this.regenToken.bind(this);
    this.regenConfirm = this.regenConfirm.bind(this);
    this.deleteApp = this.deleteApp.bind(this);
    this.deleteConfirm = this.deleteConfirm.bind(this);
    this.stopEditing = this.stopEditing.bind(this);
    this.copyToken = this.copyToken.bind(this);
    this.setCopyText = this.setCopyText.bind(this);

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
          editing: false
        });
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      console.error(err);
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
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      console.error(err);
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
      }
    }).catch((err)=>{
      console.error(err);
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

  copyToken(e){
    e.preventDefault();

    let tokenElement = this.refs.apiToken;
    tokenElement.select();

    try {
      // copy text
      document.execCommand('copy');
      this.setState({
        copied: true
      });
      tokenElement.blur();
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
  }

  setCopyText(){
    this.setState({
      copied: false
    });
  }


  render () {
    return <div className="app pure-u-1 pure-u-xl-1-2">
      <div className="card">
        {this.state.editing ? (
          <form className="pure-form" onSubmit={this.changeName}>
            <fieldset>
              <input type="text" placeholder={this.props.name} ref="name"/>
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
                  onMouseEnter={this.setCopyText}
                  style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
                >
                  <i className="fa fa-clipboard" aria-hidden="true"></i>
                  <span>{this.state.copied?'Copied!':'Click to copy to clipboard'}</span>
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
  remove: React.PropTypes.func.isRequired
};

class AppForm extends React.Component {
  constructor(props){
    super(props);
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
      }
    }).catch((err)=>{
      console.error(err);
    });
  }
  render () {
    return <div className="appForm pure-g">
      <div className="pure-u-xl-1-4"></div>
      <div className="pure-u-1 pure-u-xl-1-2">
        <div className="card">
          <h2>Create App</h2>
          <form className="pure-form pure-form-stacked" onSubmit={this.submitForm}>
            <fieldset>
              <div className="pure-g">
                <div className="pure-u-1">
                  <label htmlFor="name">App Name</label>
                  <input id="name" ref="name" className="pure-u-1" type="text"/>
                </div>
              </div>
              <div className="pure-g">
                <div className="pure-u-1-24"></div>
                <button type="submit" className="pure-button pure-button-primary pure-u-10-24">Submit</button>
                <div className="pure-u-2-24"></div>
                <button className="pure-button button-error pure-u-10-24">Cancel</button>
                <div className="pure-u-1-24>"></div>
              </div>
            </fieldset>
          </form>
        </div>
      </div>
      <div className="pure-u-xl-1-4"></div>
    </div>;
  }
}

AppForm.propTypes = {
  add: React.PropTypes.func.isRequired
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
          />;
        })}
      </div>
      <AppForm add={this.addApp}/>
    </div>;
  }
}

AppList.propTypes = {
  apps: React.PropTypes.array.isRequired
};

export default AppList;
