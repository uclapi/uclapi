import React from 'react';
import PropTypes from 'prop-types';
import Cookies from 'js-cookie';

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
        throw new Error('Unable to create a new app');
      }
    }).then((json)=>{
      if(json.success){
        let newApp = json.app;
        newApp['name'] = this.refs.name.value;
        this.refs.name.value = '';
        this.props.add(newApp);
        this.props.close();
      }else{
        throw new Error(json.message);
      }
    }).catch((err)=>{
      this.setState({
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
            <button type="button" className="pure-button button-error pure-u-10-24" onClick={this.props.close}>Cancel</button>
            <div className="pure-u-2-24"></div>
            <button type="submit" className="pure-button pure-button-primary pure-u-10-24">Create</button>
            <div className="pure-u-1-24>"></div>
          </div>
          <label className="error">{this.state.error}</label>
        </fieldset>
      </form>
    </div>;
  }
}

AppForm.propTypes = {
  add: PropTypes.func.isRequired,
  close: PropTypes.func.isRequired
};


export {AppForm};
