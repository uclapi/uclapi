import React from 'react';
import Paper from 'material-ui/Paper';

import API from './API.jsx';


let apis = [
  {
    name: "/oauth",
    description: "Enable people to sign in using UCL accounts",
    link: "/docs#oauth",
    color: "#F44336"
  },
  {
    name: "/roombookings",
    description: "Get details about all bookable rooms at UCL",
    link: "/docs#roombookings",
    color: "#673AB7"
  },
  {
    name: "/search",
    description: "Find details of people at UCL",
    link: "/docs#search",
    color: "#2196F3"
  },
  {
    name: "/timetable",
    description: "Access all the timetables at UCL",
    link: "/docs#timetable",
    color: "#00BCD4"
  },
  {
    name: "/resources",
    description: "Find how many desktops are currently available",
    link: "/docs#resources",
    color: "#CDDC39"
  },
  {
    name: "/workspaces",
    description: "Find how many busy the libraries are",
    link: "/docs#workspaces",
    color: "#009688"
  },
];

export default class APIs extends React.Component {

  render() {
    return (
      <div className="apis">
        <div className="container">
          <h1>Get Started using our APIs</h1>
          <div className="apiContainer">
            {apis.map((a, i) => <API
              key={i}
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
