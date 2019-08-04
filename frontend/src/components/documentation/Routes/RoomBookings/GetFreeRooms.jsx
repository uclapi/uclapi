import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "start_datetime": "2017-10-25T03:36:45+00:00",
  "end_datetime": "2017-10-25T23:36:45+00:00"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/roombookings/freerooms", params);

let response = `{
  "ok": true,
  "free_rooms": [
    {
      "siteid": "014",
      "location": {
        "address": [
          "Gower Street",
          "London",
          "WC1E 6BT",
          ""
        ]
      },
      "classification": "ER",
      "classification_name": "Equipment Room",
      "sitename": "Front Lodges",
      "roomname": "North Lodge 001",
      "automated": "N",
      "roomid": "001",
      "capacity": 10
    },
    ...
  ]
}
`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetFreeRooms extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="roombookings/freerooms">Get Rooms</h1>
            <p>
              Endpoint: <code>https://uclapi.com/roombookings/freerooms</code>
            </p>
            <p>
              Given a start time and an end time, this endpoint returns all rooms which are free in that time range.
            </p>
            <p>
              <i>
                Note: This endpoint only returns publicly bookable rooms. Departmentally bookable rooms are not included.
              </i>
            </p>
            <Table
              name="Query Pararmeters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token" />
              <Cell
                name="start_datetime"
                requirement="required"
                example="2011-03-06T03:36:45+00:00"
                description="Start datetime of the time range. Follows the ISO 8601 formatting standard." />
              <Cell
                name="end_datetime"
                requirement="required"
                example="2011-03-06T03:36:45+00:00"
                description="End datetime of the time range. Follows the ISO 8601 formatting standard." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The free_rooms field contains all rooms that are free in the given time range.
            </p>
            <Table
              name="Response">
              <Cell
                name="roomname"
                extra="string"
                example="Wilkins Building (Main Building) Portico"
                description="Every site (building) has a name. In some cases this is contained in the roomname as well." />
              <Cell
                name="roomid"
                extra="string"
                example="Z4"
                description="The room ID (not to be confused with the roomname)." />
              <Cell
                name="siteid"
                extra="string"
                example="086"
                description="Every room is inside a site (building). All sites have IDs." />
              <Cell
                name="sitename"
                extra="string"
                example="Main Building"
                description="The name of the site (building)." />
              <Cell
                name="capacity"
                extra="int"
                example="50"
                description="The number of people that can fit in the room." />
              <Cell
                name="classification"
                extra="string"
                example="SS"
                description="The type of room. LT = Lecture Theatre, CR = Classroom, SS = Social Space, PC1 = Public Cluster." />
              <Cell
                name="automated"
                extra="string"
                example="N"
                description="Whether bookings in this room will be confirmed automatically. A stands for automated, and N for not automated. P represents that the confirmation will be automatic, but only under certain circumstances." />
              <Cell
                name="location"
                extra="string"
                example="-"
                description="Contains an object with two keys address, and coordinates. address contains an array of address information, which when combined will make up a complete address.
coordinates contains a lat and lng key with the latitude and longitude of the room." />
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
                name="Token does not exist"
                description="Gets returned when you supply an invalid token." />
              <Cell
                name="start_datetime or end_datetime not provided"
                description="Gets returned when you don't supply a start datetime or an end datetime" />
            </Table>
          </Topic>
        </div>
      )
    }

}
