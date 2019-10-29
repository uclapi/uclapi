/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.src (gives the name of the image to be rendered relative to images/)
this.props.description (gives a description of the image being rendered for slow browsers)
this.props.width (need the width of the image)
this.props.height (need the height of the image)

OPTIONAL ATTRIBUTES:
this.props.centred (centers the image inside of its parent)
this.props.style (array containing any extra style tags)
**/

export default class ImageView extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = false

    // Bind functions
    this.setTheme = this.setTheme.bind(this)

    const {
      src,
      description,
      width,
      height,
      style,
    } = this.props

    // Every image view should contain a source, description, width and height
    if (typeof src == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no src defined`) }
    if (typeof description == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no description defined`) }
    if (typeof width == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no width defined`) }
    if (typeof height == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no height defined`) }

    this.class = `image-view`
    this.style = []
    // If custom styling then include
    if (style) { this.style = style }
    // Set up button tags
    this.setTheme()

    // Save class and stylings to the state
    this.state = {
      class: this.class,
      style: this.style,
    }
  }

  render() {
    const { class: className, style } = this.state
    const { src, description, width, height } = this.props
    return (
      <div className={className} style={style}>
        <img src={src} alt={description} width={width} height={height}></img>
      </div>
    )
  }

  setTheme() {
    // 'centred' - Center the button inside of its parent
    const { centred } = this.props
    if (centred) { this.class += ` ` + `center-x` }
  }


}
