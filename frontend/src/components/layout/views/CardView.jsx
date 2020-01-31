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

    this.getWidth = this.getWidth.bind(this)
    this.getMinWidth = this.getMinWidth.bind(this)
    this.getStyle = this.getStyle.bind(this)
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this)
    this.setTheme = this.setTheme.bind(this)
    this.setMargin = this.setMargin.bind(this)
    this.updateStyle = this.updateStyle.bind(this)
    
    this.cardRef = React.createRef()

    this.state = {
      containerWidth : -1,
    }
  }

  render() {
    this.updateStyle()

    const className = this.class
    const style = this.style

    if (this.DEBUGGING) { console.log(`DEBUG: CardView rendered with the following styles: ` + this.state.type + ` and class: ` + this.state.class) }

    const doesLinkRoute = (typeof this.props.link != `undefined`) && (typeof this.props.fakeLink == `undefined`)

    // RENDER METHOD
    if (doesLinkRoute) {
      return (
        <>
          <div className={`invisible-marker`}
            style={{
              "position": `fixed`,
              "visibility": `hidden`,
              "width": `inherit`,
            }}
            ref={this.cardRef}
          ></div>
          <a href={this.props.link}>
            <div className={className} style={style}>
              {this.props.children}
            </div>
          </a>
        </>
      )
    } else {
      return (
        <>
          <div className={`invisible-marker`}
            style={{
              "position": `fixed`,
              "visibility": `hidden`,
              "width": `inherit`,
            }}
            ref={this.cardRef}
          ></div>
          <div className={className} style={style}>
            {this.props.children}
          </div>
        </>
      )
    }
  }

  updateStyle() {
    let minWidth = this.getMinWidth()
    let shouldResize = false

    if (minWidth != `unset` && this.state.containerWidth != -1) { 
      minWidth = minWidth.substring(0, minWidth.length - 2)
      const fraction = this.props.width.split(`-`)
      const minTotalWidth = minWidth * fraction[1] / fraction[0]

      shouldResize = this.state.containerWidth <= minTotalWidth
    }

    this.class = `uclapi-card`
    this.style = {}

    const { style } = this.props
    if (style) { this.style = {...style} }

    this.setTheme()

    if (shouldResize) {
      this.setStyleKeyValuePair(`marginLeft`, `auto`)
      this.setStyleKeyValuePair(`marginRight`, `auto`)
      this.setStyleKeyValuePair(`display`, `block`)
      this.setStyleKeyValuePair(`float`, `unset`)
    }
  }

  componentDidMount() {
    if (this.props.snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentDidMount`) }
      window.addEventListener(`resize`, this.setMargin)
      // SET MARGIN IN CASE TOO SMALL
      this.setMargin()
    }
  }
  componentWillUnmount() {
    if (this.props.snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentWillUnmount`) }
      window.removeEventListener(`resize`, this.setMargin)
    }
  }

  setMargin() {
    const fraction = this.props.width.split(`-`)
    const adaption = 100 - (4 * fraction[1])

    const currentWidth = this.cardRef.current.clientWidth * adaption / 100

    this.setState({containerWidth : currentWidth})
  }

  setTheme() {
    // REQUIRED ATTRIBUTES
    // STYLE
    this.class += ` uclapi-card-` + this.getStyle()
    // WIDTH
    this.setStyleKeyValuePair(`width`, this.getWidth())
    // MIN WIDTH
    this.setStyleKeyValuePair(`minWidth`, this.getMinWidth())

    // OPTIONAL ATTRIBUTES
    // LINK
    if (this.props.link || this.props.fakeLink) { this.class += ` default-transition background-color-transition clickable uclapi-card-clicked-` + this.getStyle() }
    // ADD SHADOW AS DEFAULT
    if (typeof this.props.noShadow === `undefined` && this.getStyle() != `no-bg`) { this.class += ` uclapi-card-shadow` }
  }

  setStyleKeyValuePair(key, value) {
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to ` + value) }
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: style updated to: ` + this.style) }
  }

  getWidth() {
    if (typeof this.props.width == `undefined`) { console.exception(`EXCEPTION: no width set for card view so setting card view width to ` + this.DEFAULT_WIDTH); return this.DEFAULT_WIDTH }

    if (this.props.width == `fit-content`) { return `fit-content` }

    const fraction = this.props.width.split(`-`)
    let adaptation = 100 - (4 * fraction[1])

    if(this.props.noPadding) { adaptation = 100 }

    const percentage = fraction[0] / fraction[1] * adaptation
    return percentage + `%`
  }

  getMinWidth() {
    let minWidth = `unset`
    if (this.props.minWidth) { minWidth = this.props.minWidth }
    return minWidth
  }

  getMaxWidth() {
    let maxWidth = `unset`
    if (this.props.maxWidth) { maxWidth = this.props.maxWidth }
    return maxWidth
  }

  getStyle() {
    let style = `default`
    if (this.props.type) { style = this.props.type }
    return style
  }

}
