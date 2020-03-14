/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.link (A string that gives internal (/docs) or external (https://www.uclapi.com) link)
this.props.text (A string to describe the link, usually ALL CAPS)

OPTIONAL ATTRIBUTES:
this.props.style (An array of styles to add to the button part)
this.props.containerStyle (Changes only the parent which could be the a tag)
this.props.type (changes the styling of the button: Can take default (grey), alternate (white))
this.props.centred (if added will center the button inside its parent)
this.props.onClick (Called in place of a link)
**/

export default class ButtonView extends React.Component {

  constructor(props) {
    super(props)

    // To enable verbose output
    this.DEBUGGING = false

    // Every button view should contain a link and text
    if (typeof this.props.link == `undefined`) { console.log(`EXCEPTION: ButtonView.constructor: no link defined`) }
    if (typeof this.props.text == `undefined`) { console.log(`EXCEPTION: ButtonView.constructor: no text defined`) }

    // Save class and stylings to the state
    this.state = {
      class: ``,
      containerStyle: {},
    }
  }

  render() {

    const { className, containerStyle } = this.state
    const { style, link, onClick, text } = this.props

    if(link) {
      return (
        <a href={link} style={containerStyle}>
          <div className={className} style={style}>
            {text}
          </div>
        </a>
      )
    } else {
      return (
        <div className={className}
          style={{...style,
...containerStyle}}
          onClick={onClick}
        >
            {text}
        </div>
      )
    }
  }

  refresh = () => {
    const { type, centred, containerStyles } = this.props

    const buttonType = typeof type !== `undefined` ? type : `default`
    const className = `uclapi-button default-transition background-color-transition ` 
      + buttonType + `-button`

    console.log(containerStyles)

    let containerStyle = {
      ...containerStyles,
      width: `fit-content`,
    }

    // If the button should be centred
    if(centred) {
      containerStyle = {
        ...containerStyle,
        marginLeft: `auto`,
        marginRight: `auto`,
      }
    }

    this.setState({
      className: className,
      containerStyle: containerStyle,
    })
  }

  componentDidMount() {
    this.refresh()
  }

}
