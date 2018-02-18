import React from 'react';
import Paper from 'material-ui/Paper';

import API from './API.jsx';


let apis = [
  {
    name: "/oauth",
    description: "Enable people to sign in using UCL accounts",
    link: "https://uclapi.com/docs#oauth",
  },
  {
    name: "/roombookings",
    description: "Get details about all bookable rooms at UCL",
    link: "https://uclapi.com/docs#roombookings",
  },
  {
    name: "/search",
    description: "Find details of people at UCL",
    link: "https://uclapi.com/docs#search",
  },
  {
    name: "/timetable",
    description: "Access all the timetables at UCL",
    link: "https://uclapi.com/docs#timetable",
  },
  {
    name: "/resources",
    description: "Find how many desktops are currently available",
    link: "https://uclapi.com/docs#resources",
  },
];

export default class APIs extends React.Component {

  render() {
    return (
      <div className="apis">
        <div className="container">
          <h1>Get Started using our APIs</h1>
          <div>
            {apis.map((a, i) => <API
              k={i}
              name={a.name}
              description={a.description}
              link={a.link}
            />)}
          </div>
        </div>
      </div>
    )
  }

}
