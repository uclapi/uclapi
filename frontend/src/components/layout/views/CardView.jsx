import React from 'react'; 

/**
REQUIRED ATTRIBUTES:
this.props.width - e.g 8-10 = 80% (Also can take fit-content)

OPTIONAL ATTRIBUTES:
this.props.type - e.g default (dark grey) / default-no-shadow (dark grey no shadow) / alternate (light grey) / emphasis (orange) / fit-content (no padding or margin for inner content)
this.props.style (An array of styles to add to the component)

this.props.link (default is not clickable) => 'no-action' enables hover but does not reroute
this.props.fakeLink - same behaviour as a link

this.props.minWidth - e.g 300px a minimum width (default is unset)
this.props.noShadow - disables box shadow
**/

export default class CardView extends React.Component {

  constructor(props) {
    super(props);

    this.DEFAULT_WIDTH = 0;
    this.DEBUGGING = true;

    this.getWidth = this.getWidth.bind(this);
    this.getMinWidth = this.getMinWidth.bind(this);
    this.getStyle = this.getStyle.bind(this);
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this);
    this.setTheme = this.setTheme.bind(this);

    this.class = 'uclapi-card';
    this.style = [];

    if(this.props.style) { this.style = this.props.style; }

    this.setTheme();

    this.state = {
      style: this.style,
      class: this.class
    };
  }

  render() {
    if(this.DEBUGGING) { console.log('DEBUG: CardView rendered with the following styles: ' + this.state.type + ' and class: ' + this.state.class); }

    var doesLinkRoute = (typeof this.props.link != 'undefined') && (typeof this.props.fakeLink == 'undefined');

    // RENDER METHOD
    if(doesLinkRoute) {
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

  setTheme() {
    // REQUIRED ATTRIBUTES
    // STYLE
    this.class += ' uclapi-card-'+this.getStyle();
    // WIDTH
    this.setStyleKeyValuePair('width', this.getWidth());
    // MIN WIDTH
    this.setStyleKeyValuePair('minWidth', this.getMinWidth());
    
    // OPTIONAL ATTRIBUTES
    // LINK
    if(this.props.link || this.props.fakeLink) { this.class += ' default-transition background-color-transition clickable uclapi-card-clicked-'+this.getStyle(); }
    // ADD SHADOW AS DEFAULT
    if(typeof this.props.noShadow === 'undefined' && this.getStyle() != 'no-bg') { this.class += ' uclapi-card-shadow'}
  }

  setStyleKeyValuePair(key, value) {
    if(this.DEBUGGING) { console.log('DEBUG: ' + key + ' updated to ' + value); }
    this.style[key] = value;
    if(this.DEBUGGING) { console.log('DEBUG: style updated to: ' + this.style); }
  }

  getWidth() {
    if(typeof this.props.width == 'undefined') {console.exception('EXCEPTION: no width set for card view so setting card view width to ' + DEFAULT_WIDTH); return DEFAULT_WIDTHz;}

    if(this.props.width == 'fit-content') { return 'fit-content'; }

    var fraction = this.props.width.split('-');
    var adaptation = 100 - ( 4 * fraction[1] );
    var percentage = fraction[0] / fraction[1] * adaptation;
    return percentage + '%';
  }

  getMinWidth() {
    var minWidth = 'unset';
    if(this.props.minWidth) {minWidth=this.props.minWidth;}
    return minWidth;
  }

  getMaxWidth() {
    var maxWidth = "unset";
    if(this.props.maxWidth) {maxWidth=this.props.maxWidth;}
    return maxWidth;
  }

  getStyle() {
    var style = 'default';
    if(this.props.type) {style=this.props.type;}
    return style;
  }

}
