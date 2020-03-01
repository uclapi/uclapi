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
import propTypes from 'prop-types'
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

Section.propTypes = {
  sectionTitle: propTypes.string,
  children: propTypes.node,
}

Section.defaultProps = {
  sectionTitle: ``,
  children: null,
}

const menuContents = (
  <>
    <List component="div">
      <Section sectionTitle="Meta">
        <ListItem button>
          <ListItemText
            primary="Welcome"
            key="Welcome"
            href="#welcome"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Your API Key"
            key="Get Your API Key"
            href="#get-api-key"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="API Rate Limits"
            key="API Rate Limits"
            href="#api-rate-limits"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="API Data Freshness"
            key="API Data Freshness"
            href="#api-expiry-times"
          />
        </ListItem>
      </Section>
      <Section sectionTitle="OAuth">
        <ListItem button>
          <ListItemText
            primary="Meta"
            key="Meta"
            href="#oauth/meta"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Authorise"
            key="Authorise"
            href="#oauth/authorise"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Token"
            key="Token"
            href="#oauth/token"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="User Data"
            key="User Data"
            href="#oauth/user/data"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="Student Number"
            key="Student Number"
            href="#oauth/user/studentnumber"
          />
        </ListItem>
      </Section>

      <Section sectionTitle="Room Bookings">
        <ListItem button>
          <ListItemText
            primary="Get Rooms"
            key="Get Rooms"
            href="#roombookings/rooms"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="Get Bookings"
            key="Get Bookings"
            href="#roombookings/bookings"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="Get Equipment"
            key="Get Equipment"
            href="#roombookings/equipment"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="Get Free Rooms"
            key="Get Free Rooms"
            href="#roombookings/freerooms"
          />
        </ListItem>

        <ListItem button>
          <ListItemText
            primary="Webhooks"
            key="Webhooks"
            href="#roombookings/webhooks"
          />
        </ListItem>
      </Section>

      <Section sectionTitle="Search">
        <ListItem button>
          <ListItemText
            primary="Get People"
            key="Get People"
            href="#search/people"
          />
        </ListItem>
      </Section>

      <Section sectionTitle="Timetable">
        <ListItem button>
          <ListItemText
            primary="Get Personal Timetable"
            key="Get Personal Timetable"
            href="#timetable/personal"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primaryText="Get Timetable By Modules"
            key="Get Timetable By Modules"
            href="#timetable/bymodule"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get List of Departments"
            key="Get List of Departments"
            href="#timetable/data/departments"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get List of Department Modules"
            key="Get List of Department Modules"
            href="#timetable/data/modules"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get List of Department Modules"
            key="Get List of Department Modules"
            href="#timetable/data/modules"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get List of Department Courses"
            key="Get List of Department Courses"
            href="#timetable/data/courses"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get List of Course Modules"
            key="Get List of Course Modules"
            href="#timetable/data/courses/modules"
          />
        </ListItem>
      </Section>

      <Section sectionTitle="Resources">
        <ListItem button>
          <ListItemText
            primaryText="Get Desktop availability"
            key="Get Desktop availability"
            href="#resources/desktops"
          />
        </ListItem>
      </Section>

      <Section sectionTitle="Workspaces">
        <ListItem button>
          <ListItemText
            primary="Get Surveys"
            key="Get Surveys"
            href="#workspaces/surveys"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Sensors"
            key="Get Sensors"
            href="#workspaces/sensors"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Average Sensor Data"
            key="Get Average Sensor Data"
            href="#workspaces/sensors/averages/time"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Last Sensor Update"
            key="Get Last Sensor Update"
            href="#workspaces/sensors/lastupdated"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Sensors Summary"
            key="Get Sensors Summary"
            href="#workspaces/sensors/summary"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Map Image"
            key="Get Map Image"
            href="#workspaces/images/map"
          />
        </ListItem>
        <ListItem button>
          <ListItemText
            primary="Get Live Map Image"
            key="Get Live Map Image"
            href="#workspaces/images/map/live"
          />
        </ListItem>
      </Section>



      {/* 
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