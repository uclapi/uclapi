/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

// React
// Column for sizing
import { Column } from 'Layout/Items.jsx'
import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.width - e.g 8-10 = 80% (Also can take fit-content)

OPTIONAL ATTRIBUTES:
this.props.type - e.g default (dark grey) / default-no-shadow (dark grey no shadow) / alternate (light grey) / emphasis (orange) / fit-content (no padding or margin for inner content)
this.props.style (An array of styles to add to the Card)
this.props.containerStyle (Affects sizing and orientation of column wrapping card)

this.props.link (default is not clickable) => 'no-action' enables hover but does not reroute
this.props.fakeLink - same behaviour as a link

this.props.minWidth - e.g 300px a minimum width (default is unset)
this.props.noShadow - disables box shadow
this.props.noPadding - disables the padding 

this.props.keepInline (don't snap to a column when in mobile view)
**/

export default class CardView extends React.Component {

  constructor(props) {
    super(props)

    this.DEFAULT_WIDTH = 0
    this.DEBUGGING = false

    this.cardRef = React.createRef()

    this.state = {
      containerWidth: -1,
      className: ``,
      style: {},
      containerStyle: {},
    }
  }

  render() {
    const { className, style, containerStyle } = this.state
    const { children, link, fakeLink, type, width, minWidth = `unset`, keepInline } = this.props

    if (this.DEBUGGING) { console.log(`DEBUG: CardView rendered with the following styles: ` + type + ` and class: ` + className) }

    const doesLinkRoute = (typeof link != `undefined`) && (typeof fakeLink == `undefined`)

    // RENDER METHOD
    if (doesLinkRoute) {
      return (
        <Column
          width={width}
          minWidth={minWidth}
          style={containerStyle}
          keepInline={keepInline}
        >
          <a className={className} href={link} style={style}>
            {children}
          </a>
        </Column>
      )
    } else {
      return (
        <Column width={width} style={containerStyle} keepInline={keepInline}>
          <div className={className} style={style}>
            {children}
          </div>
        </Column>
      )
    }
  }

  refresh = () => {
    const { style: propsStyle, link, fakeLink, noShadow, type, noPadding, containerStyle: propsContainerStyle } = this.props
    const styling = typeof type === `undefined` ? `default` : type

    let className = `uclapi-card uclapi-card-` + styling
    const style = {
      ...propsStyle,
    }
    let containerStyle = {
      ...propsContainerStyle,
    }
    // LINK
    if (link || fakeLink) {
      className += ` default-transition background-color-transition clickable uclapi-card-clicked-` + styling
    }
    // ADD SHADOW AS DEFAULT
    if (typeof noShadow === `undefined` && styling != `no-bg`) {
      className += ` uclapi-card-shadow`
    }
    // NO PADDING
    if (noPadding) {
      containerStyle = {
        ...containerStyle,
        margin: 0,
        padding: 0,
      }
    }

    // Set the stylings and class
    this.setState({
      className: className,
      style: style,
      containerStyle: containerStyle,
    })
  }

  componentDidMount() {
    this.refresh()
  }
}
