import React from 'react';
/**

REQUIRED ATTRIBUTES:
this.props.width (1-3 => 1/3 width of a row)

OPTIONAL ATTRIBUTES:
this.props.horizontalAlignment (left / center / right)
this.props.verticalALignment (top / center / bottom) => Row Height must be set otherwise weird behaviour
this.props.typeOfInline (default none: block / flex / grid) => `Not sure if useful with addition of transparent cards`
this.props.textAlign (like the normal inline tag)

**/
export default class Column extends React.Component {

  constructor(props) {
    super(props);

    this.UNSET_ERROR_WIDTH = "0px";
    this.DEBUGGING = true;
    this.HORIZONTAL_PADDING = 2 + 2;

    this.getColumnWidth = this.getColumnWidth.bind(this);
    this.setColumnWidthAndPadding = this.setColumnWidthAndPadding.bind(this);
    this.setHorizontalAlignment = this.setHorizontalAlignment.bind(this);
    this.setVerticalAlignment = this.setVerticalAlignment.bind(this);
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this);
    this.setTheme = this.setTheme.bind(this);

    this.class = "column";
    this.style = [];
    this.verticalAlignment = "no-vertical-align";

    this.setTheme();

    this.state = {
      class: this.class,
      style: this.style,
      verticalAlignment: this.verticalAlignment
    };
  }

  render() {
    return (
      <div className={this.state.verticalAlignment} >
        <div className={this.state.class} style={this.state.style} >
            {this.props.children}
        </div>
      </div>
    );
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value;
    if(this.DEBUGGING) { console.log("DEBUG: " + key + " updated to: " + value); }
  }

  setTheme() {
    // REQUIRED ATTRIBUTES
    // Set the width and padding of the column
    this.setColumnWidthAndPadding();

    // OPTIONAL ATTRIBUTES
    // Handles horizontal alignment
    if(this.props.horizontalAlignment) { this.setHorizontalAlignment() }
    // Handles vertical alignment
    if(this.props.verticalAlignment) { this.setVerticalAlignment() }
    // Handles the text alignment
    if(this.props.textAlign) { this.setStyleKeyValuePair('textAlign', this.props.textAlign); }

  }

  setVerticalAlignment() {
    switch(this.props.verticalAlignment) {
      case "top":
        // Stub needs implementing
      break;

      case "center":
        this.verticalAlignment = 'vertical-align center-y';
        this.setStyleKeyValuePair("height", '100%');
      break;

      case "bottom":
        this.verticalAlignment = 'vertical-align bottom-y';
      break;
    }
  }

  setHorizontalAlignment() {
   switch(this.props.horizontalAlignment) {
      case "left":
        this.setStyleKeyValuePair("float", 'left');
      break;

      case "center":
        this.setStyleKeyValuePair("margin", 'auto');
      break;

      case "right":
        this.setStyleKeyValuePair("float", 'right');
      break;
    } 
  }

  getColumnWidth() {
    if(typeof this.props.width == "undefined") {console.log("EXCEPTION: no width set for column so setting column width to 0"); return 0;}

    var buffer = this.props.width.split("-")

    var numberOfColumns = buffer[1];
    var fraction = buffer[0] / buffer[1];

    var paddingSpace = 0;
    if(this.props.typeOfInline) { paddingSpace = this.HORIZONTAL_PADDING * numberOfColumns; }

    var spaceForColumns = 100 - paddingSpace

    var percentage = spaceForColumns * fraction;
    return percentage + "%";
  }

  setColumnWidthAndPadding() {
    this.setStyleKeyValuePair("width", this.getColumnWidth());

    if(this.props.typeOfInline) {
      this.setStyleKeyValuePair("display", "inline-" + this.props.typeOfInline);
      this.setStyleKeyValuePair("padding", "2%");
    }
  }

}