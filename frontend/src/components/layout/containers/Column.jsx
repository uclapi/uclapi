/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'
/**

REQUIRED ATTRIBUTES:
this.props.width (1-3 => 1/3 width of a row)

OPTIONAL ATTRIBUTES:
this.props.alignItems (whether to align children as if they were columns or rows (column/row) - row by default)
this.props.style (array of extra stylings)
this.props.keepInline (don't snap to a column when in mobile view)
this.props.className (additional class identifiers)

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
    const { style } = this.state
    const { children, className = ``, keepInline } = this.props

    const baseClass = keepInline ? `column-always-inline` : `column`

    return (
      <div className={baseClass + ` ` + className} style={style} >
        {children}
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

    const { alignItems } = this.props

    // REQUIRED ATTRIBUTES
    // Set the width and padding of the column
    style = this.setColumnWidthAndPadding(style)

    if(alignItems) {
      style = {
        ...style,
        flexDirection: alignItems,
      }
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
