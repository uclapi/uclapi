/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import { checkedIcon, uncheckedIcon } from 'Layout/Icons.jsx'
// Components
import { Container } from 'Layout/Items.jsx'
import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.onClick (function to be triggered when the checkbox is clicked)
this.props.checked (whether it should be checked by default)
this.props.text (text to display alongside the checkbox)

OPTIONAL ATTRIBUTES:
this.props.style
**/

// const styles = {
//   tokenText: {
//     float: `left`,
//     margin: `6px 10px 0 0`,
//     color: `white`,
//     fontWeight: `300`,
//   },
//   field: {
//     backgroundColor: `#3498db`,
//     height: `50px`,
//     float: `left`,
//     paddingRight: `10px`,
//     width: `100%`,
//     transition: `background-color 0.2s`,
//   },
// }

export default class CheckBox extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false
    
    const { onClick, isChecked } = this.props
    // Every CheckBox needs an on click event and also an initial state
    if (typeof onClick == `undefined`) {
      console.log(`EXCEPTION: CheckBox.constructor: no click function defined`)
    }
    if (typeof isChecked == `undefined`) {
      console.log(`EXCEPTION: CheckBox.constructor: no initial state defined`)
    }
    
    // Set type of button
    this.class = `uclapi-checkbox`
    this.style = []
    // If custom styling then include
    const { style } = this.props
    if (style) { this.style = style }
    // Set up button tags
    this.setTheme()

    // Save class and stylings to the state
    this.state = {
      class: this.class,
      style: this.style,
      isChecked: isChecked,
    }
  }

  render() {

    const { text } = this.props
    const { isChecked } = this.state

    const fieldClass = `field-container-not-editing`
    const fieldInputClass = `field-input-not-editing`
		const fieldHeight = `55px`

    return (
      <Container 
        className={fieldClass}
        height={fieldHeight} 
        onClick={this.toggleCheck}
        noPadding
      >
        <div className="field-label">{text}</div>

        <input 
          type="text"
          className={fieldInputClass}
          readOnly
          value={`My app requires access to the user's ${text.toLowerCase()}.`}
          style={{ height: fieldHeight }}
        />

        {
          isChecked ? (
            checkedIcon()
          ) : (
            uncheckedIcon()
          )
        }
      
    </Container>
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
    if (this.DEBUGGING) {
      console.log(`DEBUG: ` + key + ` updated to: ` + value)
    }
  }

  setTheme() {
    
  }

}
