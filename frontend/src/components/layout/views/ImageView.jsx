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
this.props.margin (add a margin to the image box)
**/

export default class ImageView extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = false

    const {
      src,
      description,
      width,
      height,
    } = this.props

    // Every image view should contain a source, description, width and height
    if (typeof src == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no src defined`) }
    if (typeof description == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no description defined`) }
    if (typeof width == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no width defined`) }
    if (typeof height == `undefined`) { console.log(`EXCEPTION: ImageView.constructor: no height defined`) }

    this.state = {
      style: {},
      className: `image-view`,
    }
  }

  render() {
    const { className, style, containerStyle } = this.state

    const { src, description, width, height } = this.props

    return (
      <div className={className} style={containerStyle}>
        <img src={src} alt={description} width={width} height={height} style={style}></img>
      </div>
    )
  }

  componentDidMount() {
    this.refresh()
  }

  refresh = () => {
    const className = `image-view`
    let classStyle = {}
    let containerStyle = {}

    // If custom styling then include
    const { style, width, height } = this.props
    if (style) { classStyle = { ...style } }

    containerStyle = {
      width: width,
      height: height,
    }

    const { centred, margin } = this.props
    // 'margin' - Add a margin to the image
    if (margin) { 
      containerStyle = { 
        ...containerStyle, 
        margin: margin,
      }
    }
    // 'centred' - Center the button inside of its parent
    if (centred) { 
      containerStyle = { 
        ...containerStyle, 
        marginLeft: `auto`,
        marginRight: `auto`,
      }
    }

    this.setState({
      style: classStyle,
      containerStyle: containerStyle,
      className: className,
    })
  }

}
