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
          UCL API
        </div>
        <SelectableList
          value={location.pathname}
        >
          <ListItem
            primaryText="Meta"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem primaryText="Version Information" value="/get-started/required-knowledge" />,
              <ListItem primaryText="Get Your API Key" value="/get-started/installation" />,
              <ListItem primaryText="API Rate Limits" value="/get-started/usage" />,
            ]}
          />
          <ListItem
            primaryText="Room Bookings"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem
                primaryText="Get Rooms"
                value="/components/app-bar"
                href="#/components/app-bar"
              />,
              <ListItem
                primaryText="Get Bookings"
                value="/components/auto-complete"
                href="#/components/auto-complete"
              />,
              <ListItem
                primaryText="Get Equipment"
                value="/components/avatar"
                href="#/components/avatar"
              />,
            ]}
          />
          <ListItem
            primaryText="Get Involved"
            primaryTogglesNestedList={true}
            nestedItems={[
              <ListItem primaryText="Community" value="/discover-more/community" />,
              <ListItem primaryText="Contributing" value="/discover-more/contributing" />,
              <ListItem primaryText="Showcase" value="/discover-more/showcase" />,
              <ListItem primaryText="Related projects" value="/discover-more/related-projects" />,
            ]}
          />
        </SelectableList>
        <Divider />
        <SelectableList
          value=""
        >
          <Subheader>Resources</Subheader>
          <ListItem primaryText="GitHub" value="https://github.com/callemall/material-ui" />
          <ListItem primaryText="Facebook" value="https://github.com/callemall/material-ui" />
          <ListItem primaryText="Twitter" value="https://github.com/callemall/material-ui" />
        </SelectableList>
      </Drawer>
    );
  }

}
