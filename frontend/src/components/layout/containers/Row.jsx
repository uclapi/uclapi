/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.styling ( styling types 'warning red' - red, 'splash-parallex' - primary color background, 'secondary' - dark grey, 'team-parallax' - hackathon scroll bg )
                OR / AND
this.props.src (pass an image to overlay in the backgorund of the row)

OPTIONAL ATTRIBUTES:
this.props.height (manually set the height over what the contents)
this.props.style (An array of styles to add to the component)
this.props.noPadding (Removes the default padding of 50px)

**/
export default class Row extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = false
    this.DEFAULT_COLOR = `transparent`

    this.updateStyling = this.updateStyling.bind(this)
  }

  updateStyling() {
    this.class = `row`
    this.style = {}

    const { style } = this.props

    if (style) { 
      this.style = { ...style } 
      if(this.DEBUGGING) {console.log(style) }
    }

    this.setTheme()
  }

  render() {
    this.updateStyling()

    const className = this.class
    const style = this.style

    const { children } = this.props

    return (
      <div className={className} style={style}>
        {children}
      </div>
    )
  }

  setStyleKeyValuePair = (key, value) => {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme = () => {
    // REQUIRED ATTRIBUTES
    // Either given a color or src
    this.setupBackground()

    const { noPadding, height } = this.props

    // Override for padding
    if (!noPadding) { this.class += ` vertical-padding` }

    // OPTIONAL ATTRIBUTES
    // Height of container
    if (height) { this.setStyleKeyValuePair(`height`, height) }
  }

  setupBackground = () => {
    if (this.DEBUGGING) { console.log(`Row.setupBackground: DEBUG Background color / src is : ` + this.props.styling + ` / ` + this.props.src) }

    const { styling, src } = this.props
    if (styling) { this.class += ` ` + styling }

    if (src) {
      this.setStyleKeyValuePair(`backgroundImage`, `url(${src})`)
      
      this.setStyleKeyValuePair(`backgroundPosition`, `50%`)
      this.setStyleKeyValuePair(`backgroundRepeat`, `no-repeat`)
    }

    if (typeof styling == `undefined` && typeof src == `undefined`) {
      console.log(`Row.setupBackground: EXCEPTION No color or source set for background so resorting to a ` + this.DEFAULT_COLOR + ` background`)
      this.class += ` ` + this.DEFAULT_COLOR
    }
  }

}
