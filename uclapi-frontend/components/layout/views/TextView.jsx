
import React from "react";

/**
REQUIRED ATTRIBUTES:
this.props.heading (what heading the text is)

OPTIONAL ATTRIBUTES:
this.props.align (the alignment of the text as in the css tag text-align)
this.props.link (add a link to the text, this is the url to link to)
this.props.style (An array of styles to add to the component)
**/

export default class TextView extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false

    // Bind functions
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this)
    this.getHeader = this.getHeader.bind(this)
    this.setTheme = this.setTheme.bind(this)

    // Every button view should contain a link and text
    if (typeof this.props.header == `undefined`) { console.log(`EXCEPTION: TextView.constructor: no header defined`) }
    if (typeof this.props.text == `undefined`) { console.log(`EXCEPTION: TextView.constructor: no text defined`) }

    // Set type of button
    this.style = {}
    // If custom styling then include
    if (this.props.style) { this.style = {...this.props.style} }
    // Set up button tags
    this.setTheme()

    // Set whether this is a link
    this.isLink = false
    if (this.props.link) { this.isLink = true }

    // Save class and stylings to the state
    this.state = {
      style: this.style,
      heading: this.getHeader(),
      link: this.isLink,
    }
  }

  render() {

    const { style = {}, link = `#` } = this.state
    const { text = `` } = this.props
    const removeDuplicatedStyles = {...style}
    removeDuplicatedStyles[`top`] = `0`

    return (
      <this.state.heading style={style}>
        {link ? (
          <a className='default-transition color-transition' href={link}>
            {text}
          </a>
        ) : text}
      </this.state.heading>
    )
  }

  getHeader() {
    let heading_size = `6`
    if (this.props.heading) { heading_size = this.props.heading }

    // Font size
    let CustomTag = `h${heading_size}`
    if (heading_size == `p`) { CustomTag = `p` }

    return CustomTag
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme() {
    // align - Set up alignment of the text
    if (this.props.align) { this.setStyleKeyValuePair(`textAlign`, this.props.align) }
    // color - Used to change the color of the text
    if (this.props.color) {
      this.setStyleKeyValuePair(`color`, this.props.color)
      this.setStyleKeyValuePair(`textDecorationColor`, this.props.color)
    }
  }
}
