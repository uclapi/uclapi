import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "client_secret": "secret"
}
r = requests.get("https://uclapi.com/timetable/personal", params=params)
print(r.json())`,

  shell: `curl -X GET https://uclapi.com/timetable/personal \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \
-d client_secret=secret`,

  javascript: `fetch("https://uclapi.com/timetable/personal?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&client_secret=secret")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}


let response = `{
    "timetable":{
        "2018-01-29": [
            {
                "location": {
                    "address": [
                        "29 Gordon Sq",
                        "London",
                        "WC1H 0PP"
                    ],
                    "name": "Gordon House 106",
                    "sitename": "Gordon House",
                    "type": "CB",
                    "capacity": 50
                },
                "end_time": "18:00:00",
                "module": {
                    "module_id": "COMP3058",
                    "lecturer": {
                        "email": "ucacdgo@ucl.ac.uk",
                        "name": "GORSE, Denise (Dr)"
                    },
                    "name": "Artificial Intelligence and Neural Computing",
                    "course_owner": "COMPS_ENG",
                },
                "duration": 120,
                "start_time": "16:00:00"
            }
        ]
    },
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
                name="sitename"
                extra="string"
                example="Gordon House"
                description="Name of the site where the event is happening." />
              <Cell
                name="type"
                extra="string"
                example="CB"
                description="Type of the room eg., Lecture Theatre, etc." />
              <Cell
                name="capacity"
                extra="int"
                example="100"
                description="Capacity of the room." />
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
                name="module"
                extra="object"
                example="JSON Object"
                description="Json object containing module details." />
              <Cell
                name="module_id"
                extra="string"
                example="COMP3058"
                description="Module id." />
              <Cell
                name="name"
                extra="string"
                example="Artificial Intelligence and Neural Computing	"
                description="Module name." />
              <Cell
                name="course_owner"
                extra="string"
                example="COMPS_ENG"
                description="Department the module comes under." />
              <Cell
                name="duration"
                extra="int"
                example="120"
                description="Duration of the event." />
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
