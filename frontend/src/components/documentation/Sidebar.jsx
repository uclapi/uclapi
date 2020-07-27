import {
  Collapse,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemText,
  ListSubheader,
  SwipeableDrawer,
} from '@material-ui/core'
import { ButtonView } from 'Layout/Items.jsx'
import propTypes from 'prop-types'
import React, { useCallback, useState } from 'react'

import ChevronDown from '../../images/documentation/chevron-down.svg'
import ChevronUp from '../../images/documentation/chevron-up.svg'

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

const Section = ({ sectionTitle, children }) => {
  const [isOpen, setOpen] = useState(false)
  const onClick = useCallback(
    () => setOpen(!isOpen),
    [isOpen]
  )
  return (
    <>
      <ListItem
        button
        onClick={onClick}
      >
        <ListItemText primary={sectionTitle} />
        {isOpen ? <img src={ChevronUp} /> : <img src={ChevronDown} />}
      </ListItem>
      <Collapse
        in={isOpen}
        timeout="auto"
        unmountOnExit
      >
        <List
          component="div"
        >
          {children}
        </List>
      </Collapse>
    </>
  )
}

Section.propTypes = {
  sectionTitle: propTypes.string,
  children: propTypes.node,
}

Section.defaultProps = {
  sectionTitle: ``,
  children: null,
}

const menuContents = {
  Meta: [
    {
      text: `Welcome`,
      href: `#welcome`,
    },
    {
      text: `Get Your API Key`,
      href: `#get-api-key`,
    },
    {
      text: `Rate Limits`,
      href: `#rate-limits`,
    },
    {
      text: `Data Freshness`,
      href: `#expiry-times`,
    },
  ],
  Oauth: [
    {
      text: `Scopes`,
      href: `#oauth/scopes`,
    },
    {
      text: `Workflow`,
      href: `#oauth/workflow`,
    },
    {
      text: `Authorise`,
      href: `#oauth/authorise`,
    },
    {
      text: `Token`,
      href: `#oauth/token`,
    },
    {
      text: `User Data`,
      href: `#oauth/user/data`,
    },
    {
      text: `Student Number`,
      href: `#oauth/user/studentnumber`,
    },
  ],
  "Room Bookings": [
    {
      text: `Get Rooms`,
      href: `#roombookings/rooms`,
    },
    {
      text: `Get Bookings`,
      href: `#roombookings/bookings`,
    },
    {
      text: `Get Equipment`,
      href: `#roombookings/equipment`,
    },
    {
      text: `Get Free Rooms`,
      href: `#roombookings/freerooms`,
    },
    {
      text: `Webhooks`,
      href: `#roombookings/webhooks`,
    },
  ],
  Search: [
    {
      text: `Get People`,
      href: `#search/people`,
    },
  ],
  Timetable: [
    {
      text: `Get Personal Timetable`,
      href: `#timetable/personal`,
    },
    {
      text: `Get Timetable By Modules`,
      href: `#timetable/bymodule`,
    },
    {
      text: `Get List of Departments`,
      href: `#timetable/data/departments`,
    },
    {
      text: `Get List of Department Modules`,
      href: `#timetable/data/modules`,
    },
    {
      text: `Get List of Deaprtment Courses`,
      href: `#timetable/data/courses`,
    },
    {
      text: `Get List of Course Modules`,
      href: `#timetable/data/courses/modules`,
    },
  ],
  Resources: [
    {
      text: `Get Desktop Availability`,
      href: `#resources/desktops`,
    }
  ],
  Workspaces: [
    {
      text: `Get Surveys`,
      href: `#workspaces/surveys`,
    },
    {
      text: `Get Sensors`,
      href: `#workspaces/sensors`,
    },
    {
      text: `Get Average Sensor Data`,
      href: `#workspaces/sensors/averages/time`,
    },
    {
      text: `Get Last Sensor Update`,
      href: `#workspaces/sensors/lastupdated`,
    },
    {
      text: `Get Sensors Summary`,
      href: `#workspaces/sensors/summary`,
    },
    {
      text: `Get Map Image`,
      href: `#workspaces/images/map`,
    },
    {
      text: `Get Live Map Image`,
      href: `#workspaces/images/map/live`,
    },
  ],
  GetInvolved: {
    text: `Get Involved`,
    href: `#get-involved`,
  },
}

const links = {
  Github: `https://github.com/uclapi`,
  Facebook: `https://facebook.com/uclapi`,
  Twitter: `https://twitter.com/uclapi`,
}


const sidebarContent = (
  <List component="div">
    {
      Object.entries(menuContents)
        .map(([sectionTitle, sectionContent]) =>
          Array.isArray(sectionContent) ? (
            <Section sectionTitle={sectionTitle} key={sectionTitle}>
              {
                sectionContent.map(({ text, href }) => (
                  <ListItem
                    button
                    component="a"
                    href={href}
                    key={href}
                    style={{
                      paddingLeft: `2rem`,
                      boxSizing: `border-box`,
                    }}
                  >
                    <ListItemText
                      primary={text}
                    />
                  </ListItem>
                ))
              }
            </Section>
          ) : (
              <ListItem
                button
                component="a"
                href={sectionContent.href}
                key={sectionContent.href}
              >
                <ListItemText
                  primary={sectionContent.text}
                />
              </ListItem>
            )
        )
    }

    <Divider />

    <ListSubheader>Links</ListSubheader>
    {
      Object.entries(links)
        .map(([text, href]) => (
          <ListItem
            button
            component="a"
            href={href}
            key={href}
          >
            <ListItemText
              primary={text}
            />
          </ListItem>
        ))
    }
  </List>
)

export default class Sidebar extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      isOpen: false,
    }
  }

  toggleOpen = () => {
    const { isOpen } = this.state
    this.setState({
      isOpen: !isOpen,
    })
  }

  render() {
    const { isOpen } = this.state
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
              {sidebarContent}
            </div>
          </Drawer>
        </div>
        <div className={`mobile tablet`}>
          <ButtonView text={`≡`}
            onClick={this.toggleOpen}
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
            onClose={this.toggleOpen}
            onOpen={this.toggleOpen}
          >
            {sidebarContent}
          </SwipeableDrawer>
        </div>
      </>
    )
  }

}