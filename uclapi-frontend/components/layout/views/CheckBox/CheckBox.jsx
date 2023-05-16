import { checkedIcon, uncheckedIcon } from '@/components/layout/Icons.jsx'
import { Container } from '@/components/layout/Items.jsx'
import React, { useCallback } from 'react'
import styles from './CheckBox.module.scss'

/**
REQUIRED ATTRIBUTES:
this.props.onClick (function to be triggered when the checkbox is clicked)
this.props.checked (whether it should be checked by default)
this.props.text (text to display alongside the checkbox)

OPTIONAL ATTRIBUTES:
this.props.style
**/

const CheckBox = ({
  text,
  isChecked = false,
  onClick = () => {},
}) => {
  const toggleCheck = useCallback(
    () => onClick(!isChecked),
    [isChecked, onClick]
  )

  return (
    <Container
      className={styles.checkbox}
      height={`55px`}
      onClick={toggleCheck}
      noPadding
    >
      <div className="field-label">{text}</div>

      <p>
        My app requires access to the user&apos;s {text.toLowerCase()}.
      </p>

      {
        isChecked ? (checkedIcon()) : (uncheckedIcon())
      }

  </Container>
  )
}

export default CheckBox
