import React from 'react';
/**

REQUIRED ATTRIBUTES:
this.props.width (1-3 => 1/3 width of a row)

OPTIONAL ATTRIBUTES:
this.props.horizontalAlignment (left / center / right)
this.props.verticalALignment (top / center / bottom) => Row Height must be set otherwise weird behaviour
this.props.typeOfInline (default none: block / flex / grid) => `Not sure if useful with addition of transparent cards`

**/
export default class Column extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      UNSET_ERROR_WIDTH: "0px",
      DEBUGGING: false,
      HORIZONTAL_PADDING: 2 + 2,
      style: [],
      class: "column",
      verticalAlignment: "no-vertical-align"
    }

    this.getColumnWidth = this.getColumnWidth.bind(this);
    this.setColumnWidthAndPadding = this.setColumnWidthAndPadding.bind(this);
    this.setHorizontalAlignment = this.setHorizontalAlignment.bind(this);
    this.setVerticalAlignment = this.setVerticalAlignment.bind(this);
    this.setupStyle = this.setupStyle.bind(this);
  }

  render() {
    this.setupStyle()

    return (
      <div className= {this.state.verticalAlignment} >
        <div className={this.state.class} style={this.state.style} >
            {this.props.children}
        </div>
      </div>
    );
  }

  setupStyle() {
    // REQUIRED ATTRIBUTES
    // Set the width and padding of the column
    this.setColumnWidthAndPadding();

    // OPTIONAL ATTRIBUTES
    // Handles horizontal alignment
    if(this.props.horizontalAlignment) { this.setHorizontalAlignment() }
    // Handles vertical alignment
    if(this.props.verticalAlignment) { this.setVerticalAlignment() }
  }

  setVerticalAlignment() {
    switch(this.props.verticalAlignment) {
      case "top":
        // Stub needs implementing 
      break;

      case "center":
        this.state.verticalAlignment = 'vertical-align center-y';
        this.state.style['height'] = '100%';
      break;

      case "middle":
        // Stub needs implementing
      break;
    }
  }

  setHorizontalAlignment() {
   switch(this.props.horizontalAlignment) {
      case "left":
        // Stub needs implementing
      break;

      case "center":
        this.state.style['margin'] = 'auto';
      break;

      case "right":
        // Stub needs implementing
      break;
    } 
  }

  getColumnWidth() {
    if(typeof this.props.width == "undefined") {console.exception("EXCEPTION: no width set for column so setting column width to 0"); return 0;}

    var buffer = this.props.width.split("-")

    var numberOfColumns = buffer[1];
    var fraction = buffer[0] / buffer[1]

    var paddingSpace = 0;
    if(this.props.TypeOfInline) { paddingSpace = this.state.HORIZONTAL_PADDING * numberOfColumns; }

    var spaceForColumns = 100 - paddingSpace

    var percentage = spaceForColumns * fraction;
    return percentage + "%";
  }

  setColumnWidthAndPadding() {
    this.state.style['width'] = this.getColumnWidth();

    if(this.props.TypeOfInline) {
      this.state.style['display'] = "inline-" + this.props.TypeOfInline; 
      this.state.style['padding'] = "2%";
    }
  }

}