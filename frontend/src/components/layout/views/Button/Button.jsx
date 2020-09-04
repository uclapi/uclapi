import React from 'react'
import './Button.scss'

const Button = ({
  className,
  link,
  onClick,
  text, // usually ALL CAPS
  style = {},
  centred = false, // if added will center the button inside its parent
  type = `default`,
  // changes the styling of the button:
  // Can take default (grey), alternate (white)
}) => {
  const componentClass = [
    `uclapi-button`,
    `default-transition`,
    `background-color-transition`,
    `${type}-button`,
    className,
  ]

  const buttonStyle = {
    ...style,
    width: `fit-content`,
    ...(centred ? {
      marginLeft: `auto`,
      marginRight: `auto`,
    }: {}),
  }

  return link ? (
    <a href={link} className={componentClass} style={buttonStyle}>
      {text}
    </a>
  ) : (
    <div className={componentClass}
      style={buttonStyle}
      onClick={onClick}
    >
      {text}
    </div>
  )
}

export default Button
