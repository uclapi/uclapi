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
import React, { useCallback, useState } from 'react'

import { ButtonView } from 'Layout/Items.jsx'

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

const menuContents = (
  <>
    <List component="div">
      <Section sectionTitle="Meta">
        <ListItem button>
          <ListItemText
            inset
            primary="Welcome"
            key="Welcome"
            href="#welcome"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            inset
            primary="Get Your API Key"
            key="Get Your API Key"
            href="#get-api-key"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            inset
            primary="API Rate Limits"
            key="API Rate Limits"
            href="#api-rate-limits"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            inset
            primary="API Data Freshness"
            key="API Data Freshness"
            href="#api-expiry-times"
          />
        </ListItem>
      </Section>

      {/* <ListItem
        href="#oauth"
        primaryText="OAuth"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Meta"
            key="Meta"
            href="#oauth/meta"
          />,
          <ListItem
            primaryText="Authorise"
            key="Authorise"
            href="#oauth/authorise"
          />,
          <ListItem
            primaryText="Token"
            key="Token"
            href="#oauth/token"
          />,
          <ListItem
            primaryText="User Data"
            key="User Data"
            href="#oauth/user/data"
          />,
          <ListItem
            primaryText="Student Number"
            key="Student Number"
            href="#oauth/user/studentnumber"
          />,
        ]}
      />

      <ListItem
        href="#roombookings"
        primaryText="Room Bookings"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Get Rooms"
            key="Get Rooms"
            href="#roombookings/rooms"
          />,
          <ListItem
            primaryText="Get Bookings"
            key="Get Bookings"
            href="#roombookings/bookings"
          />,
          <ListItem
            primaryText="Get Equipment"
            key="Get Equipment"
            href="#roombookings/equipment"
          />,
          <ListItem
            primaryText="Get Free Rooms"
            key="Get Free Rooms"
            href="#roombookings/freerooms"
          />,
          <ListItem
            primaryText="Webhooks"
            key="Webhooks"
            href="#roombookings/webhooks"
          />,
        ]}
      />

      <ListItem
        href="#search"
        primaryText="Search"
        key="Search"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Get People"
            key="Get People"
            href="#search/people"
          />,
        ]}
      />

      <ListItem
        href="#timetable"
        primaryText="Timetable"
        key="Timetable"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Get Personal Timetable"
            key="Get Personal Timetable"
            href="#timetable/personal"
          />,
          <ListItem
            primaryText="Get Timetable By Modules"
            key="Get Timetable By Modules"
            href="#timetable/bymodule"
          />,
          <ListItem
            primaryText="Get List of Departments"
            key="Get List of Departments"
            href="#timetable/data/departments"
          />,
          <ListItem
            primaryText="Get List of Department Modules"
            key="Get List of Department Modules"
            href="#timetable/data/modules"
          />,
          <ListItem
            primaryText="Get List of Department Courses"
            key="Get List of Department Courses"
            href="#timetable/data/courses"
          />,
          <ListItem
            primaryText="Get List of Course Modules"
            key="Get List of Course Modules"
            href="#timetable/data/courses/modules"
          />,
        ]}
      />

      <ListItem
        href="#resources"
        primaryText="Resources"
        key="Resources"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Get Desktop availability"
            key="Get Desktop availability"
            href="#resources/desktops"
          />,
        ]}
      />

      <ListItem
        href="#workspaces"
        primaryText="Workspaces"
        key="Workspaces"
        primaryTogglesNestedList
        nestedItems={[
          <ListItem
            primaryText="Get Surveys"
            key="Get Surveys"
            href="#workspaces/surveys"
          />,
          <ListItem
            primaryText="Get Sensors"
            key="Get Sensors"
            href="#workspaces/sensors"
          />,
          <ListItem
            primaryText="Get Average Sensor Data"
            key="Get Average Sensor Data"
            href="#workspaces/sensors/averages/time"
          />,
          <ListItem
            primaryText="Get Last Sensor Update"
            key="Get Last Sensor Update"
            href="#workspaces/sensors/lastupdated"
          />,
          <ListItem
            primaryText="Get Sensors Summary"
            key="Get Sensors Summary"
            href="#workspaces/sensors/summary"
          />,
          <ListItem
            primaryText="Get Map Image"
            key="Get Map Image"
            href="#workspaces/images/map"
          />,
          <ListItem
            primaryText="Get Live Map Image"
            key="Get Live Map Image"
            href="#workspaces/images/map/live"
          />,
        ]}
      />

      <ListItem
        primaryText="Get Involved"
        key="Get Involved"
        href="#getInvolved"
      />
    </List>

    <Divider />

    <List
      value=""
    >
      <ListSubheader>Links</ListSubheader>
      <ListItem
        primaryText="GitHub"
        key="GitHub"
        href="https://github.com/uclapi"
      />
      <ListItem
        primaryText="facebook"
        key="Facebook"
        href="https://facebook.com/uclapi"
      />
      <ListItem
        primaryText="Twitter"
        key="Twitter"
        href="https://twitter.com/uclapi"
      /> */}
    </List>
  </>
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
            }}
            >
              {menuContents}
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
            {menuContents}
          </SwipeableDrawer>
        </div>
      </>
    )
  }

}