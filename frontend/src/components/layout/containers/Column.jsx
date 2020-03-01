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
    this.DEBUGGING = true
    this.HORIZONTAL_PADDING = 2 + 2

    if (typeof this.props.width == `undefined`) { console.log(`EXCEPTION: Column.constructor: no width defined`) }

    this.state = {
      style: {},
      verticalAlignment: `no-vertical-align`,
    }
  }

  render() {
    const { verticalAlignment, style } = this.state
    const { children, className = `` } = this.props

    return (
      <div className={verticalAlignment} >
        <div className={`column ${className}`} style={style} >
          {children}
        </div>
      </div>
    )
  }

  refresh = () => {
    const { style: propsStyle } = this.props
    let style = { ...propsStyle }

    style = this.setTheme(style)

    this.setState({ style: { ...style } })
  }

  componentDidUpdate(prevProps) {
    for (const index in prevProps) {
      if (prevProps[index] !== this.props[index]) {
        this.refresh()
      }
    }
  }

  componentDidMount() {
    this.refresh()
  }

  setTheme = (style) => {
    // REQUIRED ATTRIBUTES
    // Set the width and padding of the column
    style = this.setColumnWidthAndPadding(style)

    // OPTIONAL ATTRIBUTES
    // Handles horizontal alignment
    if (this.props.horizontalAlignment) { style = this.setHorizontalAlignment(style) }
    // Handles vertical alignment
    if (this.props.verticalAlignment) { style = this.setVerticalAlignment(style) }
    // Handles the text alignment
    if (this.props.textAlign) {
      style = {
        ...style,
        textAlign: this.props.textAlign,
      }
    }

    return style
  }

  setVerticalAlignment = (style) => {
    switch (this.props.verticalAlignment) {
      case `top`:
        // Stub needs implementing
        break

      case `center`:
        this.setState({ verticalAlignment: `vertical-align center-y` })
        style = {
          ...style,
          height: `100%`,
        }
        break

      case `bottom`:
        this.setState({
          verticalAlignment: `vertical-align bottom-y`,
        })
        break
    }
    return style
  }

  setHorizontalAlignment = (style) => {
    switch (this.props.horizontalAlignment) {
      case `left`:
        style = {
          ...style,
          float: `left`,
        }
        break

      case `center`:
        style = {
          ...style,
          marginLeft: `auto`,
          marginRight: `auto`,
        }
        break

      case `right`:
        style = {
          ...style,
          float: `right`,
        }
        break
    }
    return style
  }

  getColumnWidth = () => {
    const { width } = this.props
    if (typeof width == `undefined`) { console.log(`EXCEPTION: no width set for column so setting column width to 0`); return 0 }

    const buffer = width.split(`-`)

    const fraction = buffer[0] / buffer[1]

    const paddingSpace = 0

    const spaceForColumns = 100 - paddingSpace

    const percentage = spaceForColumns * fraction
    return percentage + `%`
  }

  setColumnWidthAndPadding = (style) => {
    style = {
      ...style,
      width: this.getColumnWidth(),
    }

    if (this.props.maxWidth) {
      style = {
        ...style,
        maxWidth: this.props.maxWidth,
      }
    }
    if (this.props.minWidth) {
      style = {
        ...style,
        minWidth: this.props.minWidth,
      }
    }

    return style
  }

}
