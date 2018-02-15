import React from 'react';
import Drawer from 'material-ui/Drawer';
import {List, ListItem, makeSelectable} from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import MenuItem from 'material-ui/MenuItem';
import {spacing, typography, zIndex} from 'material-ui/styles';

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

const SelectableList = makeSelectable(List);

const styles = {
  logo: {
    cursor: 'pointer',
    fontSize: 24,
    color: typography.textFullWhite,
    lineHeight: `${spacing.desktopKeylineIncrement}px`,
    fontWeight: typography.fontWeightLight,
    backgroundColor: "#434343",
    paddingLeft: spacing.desktopGutter,
    marginBottom: 8,
  },
  version: {
    paddingLeft: spacing.desktopGutterLess,
    fontSize: 16,
  },
};


export default class Sidebar extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Drawer
        docked={true}
        open={true}>
        <div style={styles.logo}>
          <span className="sidebarLogo">
            <img src={window.staticURL + 'simpleAPILogoWhite.svg'}/>
            UCL API
          </span>
        </div>
        <SelectableList
          value={location.pathname}
        >
          <ListItem
            href="#welcome"
            primaryText="Meta"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem primaryText="Welcome" href="#welcome" />,
              <ListItem primaryText="Get Your API Key" href="#get-api-key" />,
              <ListItem primaryText="API Rate Limits" href="#api-rate-limits" />,
              <ListItem primaryText="Version Information" href="#version-information" />,
            ]}
          />

          <ListItem
            href="#oauth"
            primaryText="OAuth"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Meta"
                href="#oauth/meta"
              />,
              <ListItem
                primaryText="Authorise"
                href="#oauth/authorise"
              />,
              <ListItem
                primaryText="Token"
                href="#oauth/token"
              />,
              <ListItem
                primaryText="User Data"
                href="#oauth/user/data"
              />,
            ]}
          />

          <ListItem
            href="#roombookings"
            primaryText="Room Bookings"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get Rooms"
                href="#roombookings/rooms"
              />,
              <ListItem
                primaryText="Get Bookings"
                href="#roombookings/bookings"
              />,
              <ListItem
                primaryText="Get Equipment"
                href="#roombookings/equipment"
              />,
              <ListItem
                primaryText="Get Free Rooms"
                href="#roombookings/freerooms"
              />,
              <ListItem
                primaryText="Webhooks"
                href="#roombookings/webhooks"
              />,
            ]}
          />

          <ListItem
            href="#search"
            primaryText="Search"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get People"
                href="#search/people"
              />,
            ]}
          />

          <ListItem
            href="#timetable"
            primaryText="Timetable"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get Personal Timetable"
                href="#timetable/personal"
              />,
              <ListItem
                primaryText="Get Timetable By Modules"
                href="#timetable/bymodule"
              />,
            ]}
          />
          
          <ListItem
            href="#resources"
            primaryText="Resources"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get Desktop availability"
                href="#resources/desktops"
              />,
            ]}
          />

          <ListItem
            href="#workspaces"
            primaryText="Workspaces"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get Rooms"
                href="#workspaces/rooms"
              />,
              <ListItem
                primaryText="Get Sensors"
                href="#workspaces/sensors"
              />,
              <ListItem
                primaryText="Get Last Sensor Updates"
                href="#workspaces/sensorsLastUpdated"
              />,
              <ListItem
                primaryText="Get Map Image"
                href="#workspaces/image"
              />
            ]}
          />

          <ListItem
            primaryText="Get Involved"
            href="#getInvolved"
          />
        </SelectableList>

        <Divider />

        <SelectableList
          value=""
        >
          <Subheader>Links</Subheader>
          <ListItem primaryText="GitHub" href="https://github.com/uclapi" />
          <ListItem primaryText="Facebook" href="https://facebook.com/uclapi" />
          <ListItem primaryText="Twitter" href="https://twitter.com/uclapi" />
        </SelectableList>
      </Drawer>
    );
  }

}
