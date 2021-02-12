import {
  Divider,
  List,
  ListItem,
  ListItemText,
  ListSubheader,
} from '@material-ui/core'
import React from 'react'
import Section from './Section.jsx'

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
  OAuth: [
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
    },
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
  "Workspaces Historical": [
    {
      text: `List Surveys`,
      href: `#workspaces/historical/surveys`,
    },
    {
      text: `List Sensors`,
      href: `#workspaces/historical/sensors`,
    },
    {
      text: `List Data`,
      href: `#workspaces/historical/data`,
    },
  ],
  Analytics: [
    {
      text: `Get Number of Requests`,
      href: `#dashboard/api/analytics/total`,
    },
    {
      text: `Get Remaining Quota for Token`,
      href: `#dashboard/api/analytics/quota`,
    },
    {
      text: `Get List of Services by Popularity`,
      href: `#dashboard/api/analytics/services`,
    },
    {
      text: `Get List of Methods by Popularity`,
      href: `#dashboard/api/analytics/methods`,
    },
    {
      text: `Get Number of Users of an App`,
      href: `#dashboard/api/analytics/oauth/total`,
    },
    {
      text: `Get Number of Users per App per Dept`,
      href: `#dashboard/api/analytics/oauth/total_by_dept`,
    },
  ],
  GetInvolved: {
    text: `Get Involved`,
    href: `#get-involved`,
  },
}

const links = {
  GitHub: `https://github.com/uclapi`,
  Facebook: `https://facebook.com/uclapi`,
  Twitter: `https://twitter.com/uclapi`,
}

const MenuComponent = () => (
  <List component="div">
    {
      Object.entries(menuContents)
        .map(([sectionTitle, sectionContent]) =>
          Array.isArray(sectionContent) ? (
            <Section sectionTitle={sectionTitle} key={sectionTitle}>
              {
                sectionContent.map(({text, href}) => (
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
                    <ListItemText primary={text}/>
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
          ),
        )
    }

    <Divider/>

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

export default MenuComponent
