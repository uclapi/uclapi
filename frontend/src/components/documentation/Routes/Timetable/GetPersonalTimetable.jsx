import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-user-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "client_secret": "secret"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/timetable/personal", params);

let response = `{
    "timetable": {
      "2017-11-17": [
        {
            "start_time": "09:00",
            "end_time": "10:00",
            "duration": 60,
            "module": {
                "module_id": "COMP3004",
                "name": "Computational Complexity",
                "department_id": "COMPS_ENG",
                "department_name": "Computer Science",
                "lecturer": {
                    "name": "HIRSCH, Robin (Prof)",
                    "department_name": "Computer Science",
                    "department_id": "COMPS_ENG",
                    "email": "ucacrdh@ucl.ac.uk"
                }
            },
            "location": {
                "name": "Anatomy G29 J Z Young LT",
                "address": [
                    "Gower Street",
                    "London",
                    "WC1E 6BT"
                ],
                "site_name": "Medical Sciences and Anatomy",
                "type": "CB",
                "capacity": 186
            },
            "session_type": "L",
            "session_type_str": "Lecture",
            "session_group": "",
            "session_title": "Computational Complexity A",
            "contact": "Prof Robin Hirsch"
        },
        ...
      ],
      ...
    }
    "ok": true
}`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetPersonalTimetable extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="timetable/personal">Get Personal Timetable</h1>
            <p>
              Endpoint: <code>https://uclapi.com/timetable/personal</code>
            </p>
            <p>
              This endpoint returns the personal timetable of the user.
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
              <Cell
                name="client_secret"
                requirement="required"
                example="mysecret"
                description="Client secret of the authenticating app." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The timetable field contains an object where dates are mapped to event objects.
            </p>
            <Table
              name="Response">
              <Cell
                name="location"
                extra="object"
                example="JSON Object"
                description="Location of details of the timetable event." />
              <Cell
                name="address"
                extra="array"
                example={`["29 Gordon Sq", "London", "WC1H 0PP"]`}
                description="Address represented as an array." />
              <Cell
                name="name"
                extra="string"
                example="Gordon House 106"
                description="Room name of the timetable event." />
              <Cell
                name="site_name"
                extra="string"
                example="Gordon House"
                description="Name of the site / building where the event is happening." />
              <Cell
                name="type"
                extra="string"
                example="CB"
                description="Type of the room eg., Centrally Bookable (CB) or Departmentally Bookable (DB)." />
              <Cell
                name="capacity"
                extra="int"
                example="100"
                description="Capacity of the room (e.g. how many seats are in a lecture theatre, or how many can be sat at tables in a flat space)." />
              <Cell
                name="module"
                extra="object"
                example={`{"module_id": "COMP3011", name": "Functional Programming", "department_id": "COMPS_ENG", "department_name": "Computer Science", "lecturer": {"name": "CLACK, Chris (Dr)", "department_id": "COMPS_ENG", "department_name": "Computer Science", "email": "REDACTED@ucl.ac.uk"}}`}
                description="Information about the module as a whole, including its lead lecturer"/>
              <Cell
                name="module_id"
                extra="string"
                example="COMP3011"
                description="Module ID." />
              <Cell
                name="name"
                extra="string"
                example="Functional Programming"
                description="Module name." />
              <Cell
                name="department_id"
                extra="string"
                example="COMPS_ENG"
                description="Department the module comes under." />
              <Cell
                name="department_name"
                extra="string"
                example="Computer Science"
                description="Human readable department name that owns the module." />
              <Cell
                name="lecturer"
                extra="object"
                example={`"lecturer": {"name": "CLACK, Chris (Dr)", "department_id": "COMPS_ENG", "department_name": "Computer Science", "email": "REDACTED@ucl.ac.uk"}`}
                description="Information about the main course leader / lecturer, and what their home department is. Note that the course lead may not run every lecture, so in timetable apps you should use the contact field listed below." />
              <Cell
                name="duration"
                extra="int"
                example="120"
                description="Duration of the event in minutes." />
              <Cell
                name="start_time"
                extra="string"
                example="16:00:00"
                description="Start time of the event." />
              <Cell
                name="end_time"
                extra="string"
                example="18:00:00"
                description="End time of the event." />
              <Cell
                name="session_type"
                extra="string"
                example="L"
                description="ID of the type of session, e.g. L = Lecture, PBL = Problem Based Learning. These come from UCL's internal database, and are provided in case a new session type that we are not aware of is in the timetable. See session_type_str below." />
              <Cell
                name="session_type_str"
                extra="string"
                example="Lecture"
                description="Type of event such as Lecture, Problem Based Learning, Practical, etc. If the session_type has not been recognised by us then this will have the value Unknown." />
              <Cell
                name="session_group"
                extra="string"
                example="LAB A"
                description="Used for lab groups, or other types of small group activity that does not involve the whole cohort. When the whole cohort is invited (e.g. lectures) this value is a blank string. In the personal timetable endpoint only the labs / group sessions assigned to the user with the OAuth token provided will be returned. For example, if the user is in LAB A then Labs B onwards will not be returned." />
              <Cell
                name="contact"
                extra="string"
                example="Prof Robin Hirsch"
                description="The name associated with the individual room booking. This is the most likely candidate for the person taking the session or lecture. This name is also the most human-readable. Apps should display this value as the lecturer for any given booking, and only use the lecturer information given in the module{lecturer{}} dictionary to reference the course lead or owner." />
            </Table>
          </Topic>

          <Topic
            noExamples={true}>
            <Table
              name="Errors">
              <Cell
                name="No token provided"
                description="Gets returned when you have not supplied a token in your request." />
              <Cell
                name="OAuth token does not exist."
                description="Gets returned when you supply an invalid token." />
              <Cell
                name="Student does not have any assigned timetables."
                description="Gets returned when the user the token belongs to does not have any timetable assigned." />
            </Table>
          </Topic>
        </div>
      )
    }

}
