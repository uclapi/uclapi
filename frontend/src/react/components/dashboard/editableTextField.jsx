import React from 'react';
import PropTypes from 'prop-types';

class EditableTextField extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      value: '',
      editing: false
    };

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
              className="padded pure-button pure-button-primary"
              onClick={this.handleSubmit}
            >
              Submit
            </button>
            <button
              type="button"
              className="padded pure-button button-error"
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

EditableTextField.propTypes = {
  origValue: PropTypes.string
};

export {EditableTextField};
