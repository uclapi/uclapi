import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';

export default class SingleCentralColumn extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      STATIC_WIDTH: "66%"
    };
  }

  render() {
    var row_class_name = "row";
    var column_style = {
      "width" : this.state.STATIC_WIDTH
    };

    if(this.props.isFullScreen) { row_class_name += " full-screen"; }

    return (
      <div className={row_class_name}>
        <div className="1-column x-center" style={ column_style }>
          {props.content}
        </div>
      </div>
    )
  }

}
