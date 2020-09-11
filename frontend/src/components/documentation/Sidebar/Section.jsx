import {
  Collapse,
  List,
  ListItem,
  ListItemText,
} from '@material-ui/core'
import React, { useCallback, useState } from 'react'
import ChevronDown from '../../../images/documentation/chevron-down.svg'
import ChevronUp from '../../../images/documentation/chevron-up.svg'

const Section = ({ sectionTitle = ``, children = null }) => {
  const [isOpen, setOpen] = useState(false)
  const onClick = useCallback(
    () => setOpen(!isOpen),
    [isOpen]
  )
  return (
    <>
      <ListItem button onClick={onClick}>
        <ListItemText primary={sectionTitle} />
        {isOpen ? <img src={ChevronUp} /> : <img src={ChevronDown} />}
      </ListItem>
      <Collapse
        in={isOpen}
        timeout="auto"
        unmountOnExit
      >
        <List component="div">
          {children}
        </List>
      </Collapse>
    </>
  )
}

export default Section