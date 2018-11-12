import React from 'react';
import Paper from 'material-ui/Paper';

import API from './API.jsx';


let apis = [
  {
    name: "/oauth",
    description: "Let your users sign in with their UCL credentials",
    link: "/docs#oauth",
    color: "#F44336"
  },
  {
    name: "/roombookings",
    description: "Get details of all bookable rooms at UCL",
    link: "/docs#roombookings",
    color: "#673AB7"
  },
  {
    name: "/search",
    description: "Find people at UCL",
    link: "/docs#search",
    color: "#2196F3"
  },
  {
    name: "/timetable",
    description: "Access personal and module timetables",
    link: "/docs#timetable",
    color: "#00BCD4"
  },
  {
    name: "/resources",
    description: "Find out how many UCL desktops are free",
    link: "/docs#resources",
    color: "#CDDC39"
  },
  {
    name: "/workspaces",
    description: "See how busy the libraries are right now",
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
