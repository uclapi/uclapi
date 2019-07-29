import React from 'react';

export default class SingleColumn extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      STATIC_WIDTH: "66%"
    };
  }

  render() {
    var COLUMN_STYLE = { "width" : this.state.STATIC_WIDTH };

    var row_class_name = "row";
    var row_style = {};

    if(this.props.fill) { row_class_name += " full-screen"; }
    if(this.props.color) { row_class_name += " " + this.props.color;}
    if(this.props.isPadded) { row_class_name += " vertical-padding"; }
    if(this.props.height) { row_style['height'] = this.props.height; }
    if(this.props.src) {
      var img = require('../../../images/' + this.props.src + '.png');

       row_style['backgroundImage'] = `url(${img})`; 
       row_style['backgroundSize'] = "Cover";
       row_style['backgroundPosition'] = "50%";
    }

    return (
      <div className={ row_class_name } style={ row_style }>
        <div className="1-column center-x full-screen" style={ COLUMN_STYLE }>
          {this.props.content}
        </div>
      </div>
    );
  }

}
