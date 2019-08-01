import React from 'react'; 

export default class CardView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var card_class_name = "uclapi-card uclapi-card-";
    var card_style = {};

    if(!this.props.cardType) {card_class_name+="default";}
    if(this.props.cardType) {card_class_name+=this.props.cardType;}

    var isLink = false;

    if(this.props.link) { card_class_name += " default-transition background-color-transition clickable"; isLink = true;}
    if(this.props.isJustifiedText) { card_class_name += " justified-text";}

    card_style['minWidth'] = this.props.minWidth;
    card_style['width'] = this.props.width;

    if(isLink) {
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