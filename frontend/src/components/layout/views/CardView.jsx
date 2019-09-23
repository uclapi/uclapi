import React from 'react'; 

/**
REQUIRED ATTRIBUTES:
this.props.width - e.g 8-10 = 80% (Also can take fit-content)

OPTIONAL ATTRIBUTES:
this,props.style - e.g default (dark grey) / alternate (light grey) / emphasis (orange) / fit-content (no padding or margin for inner content)
this.props.link (default is not clickable)
this.props.minWidth - e.g 300px a minimum width (default is unset)
this.props.addPadding - if true adds a 20px padding (default is false)
**/
export default class CardView extends React.Component {

  constructor(props) {
    super(props);

    // ALLOWS FOR ANY DEBUGGING
    this.state = {
      DEBUGGING : false,
      DEFAULT_WIDTH: 0,
      style: [],
      class: 'uclapi-card uclapi-card-default'
    };

    // BINDS FUNCTIONS
    this.getWidth = this.getWidth.bind(this);
    this.getMinWidth = this.getMinWidth.bind(this);
    this.getStyle = this.getStyle.bind(this);
    this.setupStyle = this.setupStyle.bind(this);
  }

  setupStyle() {
    // REQUIRED ATTRIBUTES
    // STYLE
    this.state.class = "uclapi-card uclapi-card-"+this.getStyle();
    // WIDTH
    this.state.style['width'] = this.getWidth();
    // MIN WIDTH
    this.state.style['minWidth'] = this.getMinWidth();

    // OPTIONAL ATTRIBUTES
    // LINK
    if(this.props.link) { this.state.class += " default-transition background-color-transition clickable uclapi-card-clicked-"+this.getStyle(); }
    // ADD PADDING
    if(this.props.addPadding) { this.state.style['padding'] = "20px 0"; }
  }

  render() {
    if(this.DEBUGGING) { console.log("DEBUG: CardView rendered with the following styles: " + this.state.style + " and class: " + this.state.class); }

    this.setupStyle();

    // RENDER METHOD
    if(this.props.link) {
      return (
          <a href = {this.props.link}>
            <div className={this.state.class} style={this.state.style}>
              {this.props.children}
            </div>
          </a>
      );
    } else {
      return (
          <div className={this.state.class} style={this.state.style}>
            {this.props.children}
          </div>
      );
    }
  }

  getWidth() {
    if(typeof this.props.width == "undefined") {console.exception("EXCEPTION: no width set for card view so setting card view width to " + DEFAULT_WIDTH); return DEFAULT_WIDTHz;}

    if(this.props.width == "fit-content") { return "fit-content"; }

    var fraction = this.props.width.split("-");
    var adaptation = 100 - ( 4 * fraction[1] ); 
    var percentage = fraction[0] / fraction[1] * adaptation;
    return percentage + "%";
  }

  getMinWidth() {
    var minWidth = "unset";
    if(this.props.minWidth) {minWidth=this.props.minWidth;}
    return minWidth;
  }

  getStyle() {
    var style = "default";
    if(this.props.style) {style=this.props.style;}
    return style;
  }

}