/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

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
this.props.noPadding - disables the padding 

this.props.snapAlign - snaps the cards to be in a vertical row when they get too small to display in a horizontal row 
**/

export default class CardView extends React.Component {

  constructor(props) {
    super(props)

    this.DEFAULT_WIDTH = 0
    this.DEBUGGING = false
    
    this.cardRef = React.createRef()

    this.state = {
      containerWidth : -1,
      className: '',
      style: {},
    }
  }

  render() {
    const { className, style } = this.state
    const { children, link, fakeLink, type } = this.props

    if (this.DEBUGGING) { console.log(`DEBUG: CardView rendered with the following styles: ` + type + ` and class: ` + className) }

    const doesLinkRoute = (typeof link != `undefined`) && (typeof fakeLink == `undefined`)

    // RENDER METHOD
    if (doesLinkRoute) {
      return (
        <>
          <div className={`invisible-marker`} ref={this.cardRef}></div>
          <a href={link}>
            <div className={className} style={style}>
              {children}
            </div>
          </a>
        </>
      )
    } else {
      return (
        <>
          <div className={`invisible-marker`}ref={this.cardRef}></div>
          <div className={className} style={style}>
            {children}
          </div>
        </>
      )
    }
  }

  refresh = () => {
    const { style: propsStyle, link, fakeLink, noShadow, type, minWidth, noPadding } = this.props
    var styling = typeof type==="undefined" ? "default" : type

    var className = "uclapi-card uclapi-card-"+styling
    var style = {...propsStyle, width: this.getWidth()}

    // OPTIONAL ATTRIBUTES
    // MIN WIDTH
    if(minWidth) {
      style = {...style, minWidth, minWidth}
    }
    // SNAP ALIGN
    if(this.shouldResize()) {
      className += " uclapi-card-full-width"
    }
    // LINK
    if (link || fakeLink) { 
      className += ` default-transition background-color-transition clickable uclapi-card-clicked-` + styling
    }
    // ADD SHADOW AS DEFAULT
    if (typeof noShadow === `undefined` && styling != `no-bg`) { 
      className += ` uclapi-card-shadow` 
    }
    // NO PADDING
    if(noPadding) {
      style = {...style, marginLeft: 0, marginRight: 0}
    }

    // Set the stylings and class
    this.setState({
      className: className,
      style: style,
    })
  }

  getWidth = () => {
    const { width, noPadding } = this.props

    if (typeof width == `undefined`) { console.exception(`EXCEPTION: no width set for card view so setting card view width to ` + this.DEFAULT_WIDTH); return this.DEFAULT_WIDTH }

    if (width == `fit-content`) { return `fit-content` }

    const fraction = width.split(`-`)
    let adaptation = noPadding ? 100 : 100 - (4 * fraction[1])

    const percentage = fraction[0] / fraction[1] * adaptation
    return percentage + `%`
  }

  shouldResize = () => {
    const { minWidth, width } = this.props
    const { containerWidth } = this.state

    const fractionOfTotalWidth = width.split('-')[0] / width.split('-')[1]
    const totalMinWidth = minWidth * (1 / fractionOfTotalWidth)

    return containerWidth <= totalMinWidth
  }

  componentDidMount() {
    if (this.props.snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentDidMount`) }
      this.cardRef.current.addEventListener(`resize`, this.setMargin)
      // SET MARGIN IN CASE TOO SMALL
      this.setMargin()
    } else {
      this.refresh()
    }
  }
  componentWillUnmount() {
    if (this.props.snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentWillUnmount`) }
      this.cardRef.current.removeEventListener(`resize`, this.setMargin)
    }
  }

  setMargin = () => {
    const fraction = this.props.width.split(`-`)
    const adaption = 100 - (4 * fraction[1])

    const currentWidth = this.cardRef.current.clientWidth * adaption / 100

    console.log("Checking margin + width: " + this.cardRef.current.clientWidth + " width array: " + fraction 
      + " width: "  + currentWidth)

    this.setState({containerWidth : currentWidth})
    this.refresh()
  }
}
