import styles from './Button.module.scss'

const Button = ({
  className,
  link,
  onClick,
  children,
  style = {},
  centred = false, // if added will center the button inside its parent
  type = `default`,
  // changes the styling of the button:
  // Can take default (grey), alternate (white)
}) => {
  const componentClass = [
    styles.uclapiButton,
    `default-transition`,
    `background-color-transition`,
    `${type}-button`,
    className,
  ].join(` `)

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
      {children}
    </a>
  ) : (
    <div className={componentClass}
      style={buttonStyle}
      onClick={onClick}
    >
      {children}
    </div>
  )
}

export default Button
