/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

// Components
import { TextView } from 'Layout/Items.jsx'

// Styles
import { styles } from 'Layout/data/dashboard_styles.jsx'

/**
REQUIRED ATTRIBUTES:
this.props.onClick (function to be triggered when the checkbox is clicked)
this.props.checked (whether it should be checked by default)
this.props.text (text to display alongside the checkbox)

OPTIONAL ATTRIBUTES:
this.props.style
**/

export default class CheckBox extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false
    
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

    const { text } = this.props
    const { style, isChecked } = this.state

    return (
    <div className="field" style={{...styles.field, marginTop: `12px`}}>
      <span onClick={this.toggleCheck} style={style}>
        <input disabled type="checkbox" checked={isChecked} />
        <span style={{ fontSize : `8px` }}>{isChecked ? `✘` : null}</span>
      </span>

      <TextView text={text} heading={5} align={`left`} style={styles.tokenText} /> 
      
    </div>
    )
  }

  toggleCheck = () => {
    const { isChecked } = this.state
    const { onClick } = this.props

    onClick(!isChecked)
    this.setState({isChecked: !isChecked})
  }

  setStyleKeyValuePair = (key, value) => {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme() {
    
  }

}
