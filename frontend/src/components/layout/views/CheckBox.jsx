/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

// Components
import { TextView, Container} from 'Layout/Items.jsx'

/**
REQUIRED ATTRIBUTES:
this.props.onClick (function to be triggered when the checkbox is clicked)
this.props.checked (whether it should be checked by default)
this.props.text (text to display alongside the checkbox)

OPTIONAL ATTRIBUTES:
this.props.style
**/

const styles = {
  tokenText: {
    float: `left`,
    margin: `6px 10px 0 0`,
    color: `white`,
    fontWeight: `300`,
  },
  field: {
    backgroundColor: `#3498db`,
    height: `50px`,
    float: `left`,
    paddingRight: `10px`,
    width: `100%`,
    transition: `background-color 0.2s`,
  }
}

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

    const fieldClass = "field-container-not-editing"
		const fieldHeight = "55px"

    return (
      <Container 
        className={fieldClass}
        height={fieldHeight} 
        onClick={this.toggleCheck}
        noPadding
      >
        <span style={style}>
          <input disabled type="checkbox" checked={isChecked} />
          <span style={{ fontSize : `8px` }}>{isChecked ? `✘` : null}</span>
        </span>

        <TextView text={text} heading={5} align={`left`} style={styles.tokenText} /> 
      
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
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme() {
    
  }

}
