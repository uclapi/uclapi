import React from 'react';
import { EditableTextField } from './editableTextField.jsx';
import Cookies from 'js-cookie';

const defaultHeaders = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-CSRFToken': Cookies.get('csrftoken')
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
      throw new Error('Unable to change name.');
    }).then((json)=>{
      if(json.success){
        return this.updateName(json);
      }
      throw new Error(json.message);
    }).catch((err)=>{
      this.props.setError(err.message);
    });
  }
}

AppNameField.propTypes = {
  scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
  appId: React.PropTypes.string.isRequired,
  setError: React.PropTypes.func
};
