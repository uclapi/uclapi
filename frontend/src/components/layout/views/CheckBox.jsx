/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.onClick (function to be triggered when the checkbox is clicked)
this.props.checked (whether it should be checked by default)

OPTIONAL ATTRIBUTES:
**/

export default class CheckBox extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false

    // Bind functions
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this)
    this.toggleCheck = this.toggleCheck.bind(this)
    
    // Every CheckBox needs an on click event and also an initial state
    if (typeof this.props.onClick == `undefined`) { console.log(`EXCEPTION: CheckBox.constructor: no click function defined`) }
    if (typeof this.props.isChecked == `undefined`) { console.log(`EXCEPTION: CheckBox.constructor: no initial state defined`) }
    
    // Set type of button
    this.class = `uclapi-checkbox`
    this.style = []
    // If custom styling then include
    if (this.props.style) { this.style = this.props.style }
    // Set up button tags
    this.setTheme()

    // Save class and stylings to the state
    this.state = {
      class: this.class,
      style: this.style,
      isChecked: this.props.isChecked,
    }
  }

  render() {

    const { style } = this.state

    return (
      <span onClick={this.toggleCheck} style={style}>
        <input type="checkbox" checked={this.state.isChecked} />
        <span style={{ fontSize : `8px` }}>{this.state.isChecked ? `✘` : null}</span>
      </span>
    )
  }

  toggleCheck() {
    this.props.onClick(!this.state.isChecked)
    this.setState({isChecked: !this.state.isChecked})
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme() {
    
  }

}
