import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';

export default class SingleCentralColumn extends React.Component {

  var STATIC_WIDTH = "66%";

  constructor(props) {
    super(props);
  }

  render() {
    var row_class_name = "row";

    if(this.props.isFullScreen) { row_class_name += " full-screen"; }

    return (
      <div className={row_class_name}>
        <div className="1-column x-center">
          {props.content}
        </div>
      </div>
    )
  }

}
