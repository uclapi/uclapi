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
      containerWidth: -1,
    }
  }

  render() {
    this.updateStyle()

    const { class: className, style } = this
    const {
      type,
      stateClass,
    } = this.state
    const {
      link,
      fakeLink,
      children,
    } = this.props

    if (this.DEBUGGING) {
      console.log(
        `DEBUG: CardView rendered with the following styles: `
        + type
        + ` and class: `
        + stateClass
      )
    }

    const doesLinkRoute = (
      (typeof link != `undefined`) &&
      (typeof fakeLink == `undefined`)
    )

    // RENDER METHOD
    if (doesLinkRoute) {
      return (
        <>
          <div className={`invisible-marker`}
            style={{
              "position": `absolute`,
              "visibility": `hidden`,
              "width": `inherit`,
            }}
            ref={this.cardRef}
          ></div>
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
          <div className={`invisible-marker`}
            style={{
              "position": `absolute`,
              "visibility": `hidden`,
              "width": `inherit`,
            }}
            ref={this.cardRef}
          ></div>
          <div className={className} style={style}>
            {children}
          </div>
        </>
      )
    }
  }

  updateStyle = () => {
    let minWidth = this.getMinWidth()
    let shouldResize = false

    const { containerWidth } = this.state
    const { width } = this.props

    if (minWidth != `unset` && containerWidth != -1) {
      minWidth = minWidth.substring(0, minWidth.length - 2)
      const fraction = width.split(`-`)
      const minTotalWidth = minWidth * fraction[1] / fraction[0]

      shouldResize = containerWidth <= minTotalWidth
    }

    this.class = `uclapi-card`
    this.style = {}

    const { style } = this.props
    if (style) { this.style = { ...style } }

    this.setTheme()

    if (shouldResize) {
      this.setStyleKeyValuePair(`marginLeft`, `auto`)
      this.setStyleKeyValuePair(`marginRight`, `auto`)
      this.setStyleKeyValuePair(`display`, `block`)
      this.setStyleKeyValuePair(`float`, `unset`)
    }
  }

  componentDidMount() {
    const { snapAlign } = this.props
    if (snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentDidMount`) }
      window.addEventListener(`resize`, this.setMargin)
      // SET MARGIN IN CASE TOO SMALL
      this.setMargin()
    }
  }
  componentWillUnmount() {
    const { snapAlign } = this.props
    if (snapAlign) {
      if (this.DEBUGGING) { console.log(`CardView.componentWillUnmount`) }
      window.removeEventListener(`resize`, this.setMargin)
    }
  }

  setMargin = () => {
    const { width } = this.props
    const fraction = width.split(`-`)
    const adaption = 100 - (4 * fraction[1])

    const currentWidth = this.cardRef.current.clientWidth * adaption / 100

    this.setState({ containerWidth: currentWidth })
  }

  setTheme = () => {
    // REQUIRED ATTRIBUTES
    // STYLE
    this.class += ` uclapi-card-` + this.getStyle()
    // WIDTH
    this.setStyleKeyValuePair(`width`, this.getWidth())
    // MIN WIDTH
    this.setStyleKeyValuePair(`minWidth`, this.getMinWidth())

    const { link, fakeLink, noShadow } = this.props

    // OPTIONAL ATTRIBUTES
    // LINK
    if (link || fakeLink) {
      this.class += ` default-transition background-color-transition`
        + `clickable uclapi-card-clicked-`
        + this.getStyle()
    }
    // ADD SHADOW AS DEFAULT
    if (typeof noShadow === `undefined` && this.getStyle() != `no-bg`) {
      this.class += ` uclapi-card-shadow`
    }
  }

  setStyleKeyValuePair = (key, value) => {
    if (this.DEBUGGING) {
      console.log(`DEBUG: ` + key + ` updated to ` + value)
    }
    this.style[key] = value
    if (this.DEBUGGING) {
      console.log(`DEBUG: style updated to: ` + this.style)
    }
  }

  getWidth = () => {
    const { width, noPadding } = this.props
    if (typeof width == `undefined`) {
      console.exception(
        `EXCEPTION: no width set for card view so setting card view width to `
        + this.DEFAULT_WIDTH
      )
      return this.DEFAULT_WIDTH
    }

    if (width == `fit-content`) { return `fit-content` }

    const fraction = width.split(`-`)
    let adaptation = 100 - (4 * fraction[1])

    if (noPadding) {
      adaptation = 100
      this.setStyleKeyValuePair(`marginLeft`, `0`)
      this.setStyleKeyValuePair(`marginRight`, `0`)
    }

    const percentage = fraction[0] / fraction[1] * adaptation
    return percentage + `%`
  }

  getMinWidth = () => {
    const { minWidth } = this.props
    return minWidth ? minWidth : `unset`
  }

  getMaxWidth = () => {
    const { maxWidth } = this.props
    return maxWidth ? maxWidth : `unset`
  }

  getStyle = () => {
    const { type } = this.props
    return type ? type : `default`
  }

}
