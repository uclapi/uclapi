import React from 'react'; 

/**
REQUIRED ATTRIBUTES:
this.props.width - e.g 8-10 = 80% 

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
    };

    // BINDS FUNCTIONS
    this.getWidth = this.getWidth.bind(this);
    this.getMinWidth = this.getMinWidth.bind(this);
    this.getStyle = this.getStyle.bind(this);
  }

  getWidth() {
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
  render() {
    if(this.DEBUGGING) { console.log("CardView rendered with the following props: " + this.props); }
    
    var card_style = {};

    // REQUIRED ATTRIBUTES
    // STYLE
    var card_class_name = "uclapi-card uclapi-card-"+this.getStyle();
    // WIDTH
    card_style['width'] = this.getWidth();
    // MIN WIDTH
    card_style['minWidth'] = this.getMinWidth();

    // OPTIONAL ATTRIBUTES
    // LINK
    if(this.props.link) { card_class_name += " default-transition background-color-transition clickable uclapi-card-clicked-"+this.getStyle(); }
    // ADD PADDING
    if(this.props.addPadding) { card_style['padding'] = "20px 0"; }

    // RENDER METHOD
    if(this.props.link) {
      return (
          <a href = {this.props.link}>
            <div className={card_class_name} style={card_style}>
              {this.props.children}
            </div>
          </a>
      );
    } else {
      return (
          <div className={card_class_name} style={card_style}>
            {this.props.children}
          </div>
      );
    }
  }

}