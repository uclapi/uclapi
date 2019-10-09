import React from 'react';
import Drawer from 'material-ui/Drawer';
import {List, ListItem, makeSelectable} from 'material-ui/List';
import Divider from 'material-ui/Divider';
import Subheader from 'material-ui/Subheader';
import MenuItem from 'material-ui/MenuItem';
import {spacing, typography, zIndex} from 'material-ui/styles';
import apiLogo from './../../images/simpleAPILogoWhite.svg';

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
        open={true}
        style={{"top" : "60px"}}>
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
              <ListItem primaryText="API Data Freshness" href="#api-expiry-times" />,
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
              <ListItem
                primaryText="Student Number"
                href="#oauth/user/studentnumber"
              />
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
              <ListItem
                primaryText="Get List of Departments"
                href="#timetable/data/departments"
              />,
              <ListItem
                primaryText="Get List of Department Modules"
                href="#timetable/data/modules"
              />,
              <ListItem
                primaryText="Get List of Department Courses"
                href="#timetable/data/courses"
              />,
              <ListItem
                primaryText="Get List of Course Modules"
                href="#timetable/data/courses/modules"
              />
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
                primaryText="Get Surveys"
                href="#workspaces/surveys"
              />,
              <ListItem
                primaryText="Get Sensors"
                href="#workspaces/sensors"
              />,
              <ListItem
                primaryText="Get Average Sensor Data"
                href="#workspaces/sensors/averages/time"
              />,
              <ListItem
                primaryText="Get Last Sensor Update"
                href="#workspaces/sensors/lastupdated"
              />,
              <ListItem
                primaryText="Get Sensors Summary"
                href="#workspaces/sensors/summary"
              />,
              <ListItem
                primaryText="Get Map Image"
                href="#workspaces/images/map"
              />,
              <ListItem
                primaryText="Get Live Map Image"
                href="#workspaces/images/map/live"
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
