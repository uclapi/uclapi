import React from 'react';
import Paper from 'material-ui/Paper';

import API from './API.jsx';


let apis = [
  {
    name: "/oauth",
    description: "Enable people to sign in using UCL accounts",
    link: "https://uclapi.com/docs#oauth",
    color: "#F44336"
  },
  {
    name: "/roombookings",
    description: "Get details about all bookable rooms at UCL",
    link: "https://uclapi.com/docs#roombookings",
    color: "#673AB7"
  },
  {
    name: "/search",
    description: "Find details of people at UCL",
    link: "https://uclapi.com/docs#search",
    color: "#2196F3"
  },
  {
    name: "/timetable",
    description: "Access all the timetables at UCL",
    link: "https://uclapi.com/docs#timetable",
    color: "#00BCD4"
  },
  {
    name: "/resources",
    description: "Find how many desktops are currently available",
    link: "https://uclapi.com/docs#resources",
    color: "#CDDC39"
  },
  {
    name: "/workspaces",
    description: "Find how many busy the libraries are",
    link: "https://uclapi.com/docs#workspaces",
    color: "#009688"
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
              bgcolor={a.color}
            />)}
          </div>
        </div>
      </div>
    )
  }

}
