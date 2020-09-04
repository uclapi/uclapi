import {
  Drawer,
  SwipeableDrawer,
} from '@material-ui/core'
import { ButtonView } from 'Layout/Items.jsx'
import React, { useCallback, useState } from 'react'
import Menu from './MenuContent.jsx'

/*
  Got this entire thing from
  https://github.com/callemall/material-ui/blob/master/docs/src/app/components/AppNavDrawer.js
  as our side bar just needs to be similar to the material-ui docs sidebar here:
  http://www.material-ui.com/#/components/drawer

  Didn't get the time to look into how the links will work
  but I think we can have an href inside each Topic component
  and when you click on the link in the sidebar, you get routed to
  the href in the Topic component
*/

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(false)
  const toggleOpen = useCallback(() => setIsOpen(!isOpen), [isOpen])

  return (
    <>
      <div className={`default`}>
        <Drawer
          variant="permanent"
        >
          <div style={{
            marginTop: `61px`,
            width: `256px`,
            overflow: `auto`,
          }}
          >
            <Menu />
          </div>
        </Drawer>
      </div>
      <div className={`mobile tablet`}>
        <ButtonView text={`≡`}
          onClick={toggleOpen}
          style={{
            left: `2px`,
            padding: `15px 20px`,
            top: `62px`,
            position: `fixed`,
            borderRadius: `50px`,
            cursor: `pointer`,
          }}
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