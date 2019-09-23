import React from 'react';
import PropTypes from 'prop-types';

import defaultHeaders from './defaultHeaders.js';

class OAuthCallbackField extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      callbackUrl: this.props.callbackUrl ? this.props.callbackUrl: '',
      saved: false,
      error_msg: '',
      error: false
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
      headers: defaultHeaders,
      body: 'app_id=' + this.props.appId + '&callback_url=' + encodeURIComponent(this.state.callbackUrl)
    }).then((res)=>{
      return res.json()
    }).then((json)=>{
      if(json.success){
        this.setState({saved: true});
        this.setState({error: false});
        setTimeout(()=>{this.setState({saved:false});}, 5000);
        return;
      }
      throw new Error(json.message);
    }).catch((err)=>{
      this.setState({error_msg:err.message});
      this.setState({error: true});
      this.props.setError(err.message);
    });
  }

  render(){
    return(
      <div>
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
        {this.state.error &&
          <label>Error: {this.state.error_msg}</label>
        }
      </div>
    );
  }
}

OAuthCallbackField.propTypes = {
  callbackUrl: PropTypes.string,
  appId: PropTypes.string,
  setError: PropTypes.func
};

export default OAuthCallbackField;
