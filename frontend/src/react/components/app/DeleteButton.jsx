import React from 'react';
import defaultHeaders from './defaultHeaders.js';


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
      headers: defaultHeaders,
      body: 'app_id=' + this.props.appId
    }).then((res)=>{
      if(res.ok){ return res.json(); }
      throw new Error('Unable to delete app');
    }).then((json)=>{
      if(json.success){ return this.props.remove(this.props.appId); }
      throw new Error(json.message);
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
  setError: React.PropTypes.func.isRequired
};

export default DeleteButton;
