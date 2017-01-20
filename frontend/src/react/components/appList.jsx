import React from 'react';
import update from 'immutability-helper';

class App extends React.Component {
  render () {
    return <div className="app card pure-u-1 pure-u-md-1-2">
      <h2>{this.props.name}</h2>
      <p>API Token: {this.props.appKey}</p>
      <p>Created: {this.props.created}</p>
    </div>;
  }
}

App.propTypes = {
  name: React.PropTypes.string.isRequired,
  appKey: React.PropTypes.string.isRequired,
  created: React.PropTypes.string.isRequired
};

class AppForm extends React.Component {
  render () {
    return <div className="appForm card pure-u-1 pure-u-md-1-2">
      <form className="pure-form pure-form-stacked">
        <fieldset>
          <div className="pure-g">
            <div className="pure-u-1">
              <label htmlFor="name">App Name</label>
              <input id="name" className="pure-u-1" type="text"/>
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
    </div>;
  }
}

class AppList extends React.Component {
  constructor (props) {
    super(props);
    this.state = {apps: props.apps};
  }

  addApp(app){
    this.setState( (state) => 
      update(state, {apps: {$push: [app]}})
    );
  }

  getAppIndex(appName){
    for(let app of this.state.apps){
      if(app.name === appName){
        return this.state.apps.indexOf(app);
      }
    }
  }

  render () {
    return <div className="appList pure-g">
      {this.state.apps.map((app, i) => {
        return <App name={app.name} appKey={app.api_token} created={app.created} key={i} />;
      })}
      <AppForm />
    </div>;
  }
}

AppList.propTypes = {
  apps: React.PropTypes.array.isRequired
};

export default AppList;
