import React from 'react';

/**
REQUIRED ATTRIBUTES:
this.props.src (gives the name of the image to be rendered relative to images/)
this.props.description (gives a description of the image being rendered for slow browsers)
this.props.width (need the width of the image)
this.props.height (need the height of the image)

OPTIONAL ATTRIBUTES:
this.props.isCentered (centers the image inside of its parent)
this.props.isPadded (and variations affect the vertical padding of the layout)
**/

export default class ImageView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var image_class_name = "image-view"

    if(this.props.isCentered) { image_class_name += " center-x"; }
    if(this.props.isPadded) { image_class_name += " vertical-padding-top vertical-padding-bottom"; }
    if(this.props.isPaddedTop) { image_class_name += " vertical-padding-top"; }
    if(this.props.isPaddedBottom) { image_class_name += " vertical-padding-bottom"; }

    var img = require('../../../images/' + this.props.src);

    return (
       <div className={image_class_name}>
        <img src={img} alt={this.props.description} width={this.props.width} height={this.props.height}></img>
       </div>
    );
  }

}