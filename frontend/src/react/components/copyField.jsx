import React from 'react';

class CopyField extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      copied: false
    };
    this.copyToClipBoard = this.copyToClipBoard.bind(this);
  }

  copyToClipBoard(e){
    e.preventDefault();

    let element = this.refs.copyField;
    element.select();

    try {
      // copy text
      document.execCommand('copy');
      this.setState({
        copied: true
      });
      setTimeout(()=>{
        this.setState({
          copied: false
        });
      },5000);
      element.blur();
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
  }

  render(){
    return(
      <form className="pure-form pure-g">
        <div className="pure-u-3-4">
          <input
            type="text"
            ref="copyField"
            className="pure-input-1"
            value={this.props.val}
            readOnly
            style={{ 'borderRadius': '4px 0px 0px 4px'}}
          />
        </div>
        <div className="pure-u-1-4">
          <button
            className="pure-button pure-button-primary pure-input-1 tooltip"
            onClick={this.copyToClipBoard}
            style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
          >
            <i className="fa fa-clipboard" aria-hidden="true"></i>
            <span>{this.state.copied?'Copied!':'Click to copy to clipboard'}</span>
          </button>
        </div>
      </form>
    );
  }
}

CopyField.propTypes = {
  val: React.PropTypes.string.isRequired
};

class CopyActionField extends CopyField {

  render(){
    return(
      <form className="pure-form pure-g">
        <div className="pure-u-2-3">
          <input
            type="text"
            ref="copyField"
            className="pure-input-1"
            value={this.props.val}
            readOnly
            style={{ 'borderRadius': '4px 0px 0px 4px'}}
          />
        </div>
        <div className="pure-u-1-6">
          <button
            className="pure-button pure-button-primary pure-input-1 tooltip"
            onClick={this.copyToClipBoard}
            style={{ 'border': '1px solid #ccc', 'borderRadius': '0px'}}
          >
            <i className="fa fa-clipboard" aria-hidden="true"></i>
            <span>{this.state.copied?'Copied!':'Click to copy to clipboard'}</span>
          </button>
        </div>
        <div className="pure-u-1-6">
          <button
            className="pure-button pure-button-primary pure-input-1"
            onClick={this.props.action}
            style={{ 'border': '1px solid #ccc', 'borderRadius': '0px 4px 4px 0px'}}
          >
            <i className={this.props.icon} aria-hidden="true"></i>
          </button>
        </div>
      </form>
    );
  }
}

CopyActionField.propTypes = {
  action: React.PropTypes.func.isRequired,
  icon: React.PropTypes.string.isRequired
};

export {
  CopyField,
  CopyActionField
};
