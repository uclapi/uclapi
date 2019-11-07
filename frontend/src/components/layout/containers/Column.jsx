/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'
/**

REQUIRED ATTRIBUTES:
this.props.width (1-3 => 1/3 width of a row)

OPTIONAL ATTRIBUTES:
this.props.horizontalAlignment (left / center / right)
this.props.verticalALignment (top / center / bottom) => Row Height must be set otherwise weird behaviour
this.props.textAlign (like the normal inline tag)
this.props.style (array of extra stylings)

**/
export default class Column extends React.Component {

  constructor(props) {
    super(props)

    this.UNSET_ERROR_WIDTH = `0px`
    this.DEBUGGING = false
    this.HORIZONTAL_PADDING = 2 + 2

    this.getColumnWidth = this.getColumnWidth.bind(this)
    this.setColumnWidthAndPadding = this.setColumnWidthAndPadding.bind(this)
    this.setHorizontalAlignment = this.setHorizontalAlignment.bind(this)
    this.setVerticalAlignment = this.setVerticalAlignment.bind(this)
    this.setStyleKeyValuePair = this.setStyleKeyValuePair.bind(this)
    this.setTheme = this.setTheme.bind(this)

    if (typeof this.props.width == `undefined`) { console.log(`EXCEPTION: Column.constructor: no width defined`) }

    this.class = `column`
    this.style = []

    if (this.props.style) { this.style = this.props.style }

    this.verticalAlignment = `no-vertical-align`

    this.setTheme()

    this.state = {
      class: this.class,
      style: this.style,
      verticalAlignment: this.verticalAlignment,
    }
  }

  render() {
    return (
      <div className={this.state.verticalAlignment} >
        <div className={this.state.class} style={this.state.style} >
          {this.props.children}
        </div>
      </div>
    )
  }

  setStyleKeyValuePair(key, value) {
    this.style[key] = value
    if (this.DEBUGGING) { console.log(`DEBUG: ` + key + ` updated to: ` + value) }
  }

  setTheme() {
    // REQUIRED ATTRIBUTES
    // Set the width and padding of the column
    this.setColumnWidthAndPadding()

    // OPTIONAL ATTRIBUTES
    // Handles horizontal alignment
    if (this.props.horizontalAlignment) { this.setHorizontalAlignment() }
    // Handles vertical alignment
    if (this.props.verticalAlignment) { this.setVerticalAlignment() }
    // Handles the text alignment
    if (this.props.textAlign) { this.setStyleKeyValuePair(`textAlign`, this.props.textAlign) }

  }

  setVerticalAlignment() {
    switch (this.props.verticalAlignment) {
      case `top`:
        // Stub needs implementing
        break

      case `center`:
        this.verticalAlignment = `vertical-align center-y`
        this.setStyleKeyValuePair(`height`, `100%`)
        break

      case `bottom`:
        this.verticalAlignment = `vertical-align bottom-y`
        break
    }
  }

  setHorizontalAlignment() {
    switch (this.props.horizontalAlignment) {
      case `left`:
        this.setStyleKeyValuePair(`float`, `left`)
        break

      case `center`:
        this.setStyleKeyValuePair(`margin`, `auto`)
        break

      case `right`:
        this.setStyleKeyValuePair(`float`, `right`)
        break
    }
  }

  getColumnWidth() {
    if (typeof this.props.width == `undefined`) { console.log(`EXCEPTION: no width set for column so setting column width to 0`); return 0 }

    const buffer = this.props.width.split(`-`)

    const fraction = buffer[0] / buffer[1]

    const paddingSpace = 0

    const spaceForColumns = 100 - paddingSpace

    const percentage = spaceForColumns * fraction
    return percentage + `%`
  }

  setColumnWidthAndPadding() {
    this.setStyleKeyValuePair(`width`, this.getColumnWidth())

    if (this.props.maxWidth) { this.setStyleKeyValuePair(`maxWidth`, this.props.maxWidth) }
    if (this.props.minWidth) { this.setStyleKeyValuePair(`minWidth`, this.props.minWidth) }
  }

}
