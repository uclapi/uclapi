import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';


export default class Jumbotron extends React.Component {

  render () {
    return (
      <div className="jumbotron"
        style={{
          "background": this.props.bgcolor,
          "color": this.props.color
        }}>
        <div className="container center">
          { this.props.children }
        </div>
      </div>
    )
  }

}
