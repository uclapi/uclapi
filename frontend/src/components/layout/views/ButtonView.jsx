/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.link (A string that gives internal (/docs) or external (https://www.uclapi.com) link)
this.props.text (A string to describe the link, usually ALL CAPS)

OPTIONAL ATTRIBUTES:
this.props.style (An array of styles to add to the component)
this.props.type (changes the styling of the button: Can take default (grey), alternate (white))
this.props.centred (if added will center the button inside its parent)
this.props.onClick (Called in place of a link)
**/

export default class ButtonView extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false

    // Bind functions
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this)
    this.getClassName = this.getClassName.bind(this)
    this.setTheme = this.setTheme.bind(this)

    // Every button view should contain a link and text
    if (typeof this.props.link == `undefined`) { console.log(`EXCEPTION: ButtonView.constructor: no link defined`) }
    if (typeof this.props.text == `undefined`) { console.log(`EXCEPTION: ButtonView.constructor: no text defined`) }

    // Set type of button
    this.class = this.getClassName()
    this.style = []
    // If custom styling then include
    if (this.props.style) { this.style = this.props.style }
    // Set up button tags
    this.setTheme()

    // Save class and stylings to the state
    this.state = {
      class: this.class,
      style: this.style,
    }
  }

  render() {
    if(this.props.link) {
      return (
        <a href={this.props.link}>
          <div className={this.state.class} style={this.state.style}>
            {this.props.text}
          </div>
        </a>
      )
    } else {
      return (
        <div className={this.state.class} style={this.state.style} onClick={this.props.onClick}>
            {this.props.text}
        </div>
        
      )
    }
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  getClassName() {
    let buttonType = `default`
    const className = `uclapi-button default-transition background-color-transition`
    if (this.props.type) { buttonType = this.props.type }
    return className + ` ` + buttonType + `-button`
  }

  setTheme() {
    // 'centred' - Center the button inside of its parent
    if (this.props.centred) { this.class += ` ` + `center-x` }
  }

}
