import {
  Drawer,
  SwipeableDrawer,
} from '@material-ui/core'
import { Button } from 'Layout/Items.jsx'
import React, { useCallback, useState } from 'react'
import Menu from './MenuContent.jsx'
import './Sidebar.scss'

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const toggleOpen = useCallback(() => setIsOpen(!isOpen), [isOpen])

  return (
    <>
      <div className="default">
        <Drawer variant="permanent">
          <div className="menu-container">
            <Menu />
          </div>
        </Drawer>
      </div>
      <div className="mobile tablet">
        <Button text={`≡`}
          onClick={toggleOpen}
          className="hamburger-button"
        />

        <SwipeableDrawer
          open={isOpen}
          onClose={toggleOpen}
          onOpen={toggleOpen}
        >
          <Menu />
        </SwipeableDrawer>
      </div>
    </>
  )
}

export default Sidebar