import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/resources/desktops", params);

let response = `{
    "ok": true,
    "data": [
        {
            "room_status": "Room available all day. For accurate Library opening times, please check the Library Opening hours website http://www.ucl.ac.uk/library/opening",
            "total_seats": "35",
            "location": {
                "latitude": "51.523481",
                "room_id": "C14",
                "postcode": "WC1E 6BT",
                "address": "Malet Place, Gower Street",
                "room_name": "Ground-Ground floor - Public",
                "building_name": "DMS Watson Science Library",
                "longitude": "-0.132571"
            },
            "free_seats": "28"
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

export default class GetEquiment extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="resources/desktops">Get desktop availability.</h1>
            <p>
              This endpoint returns number of desktops and how many are free at the time of making the request.
            </p>

            <Table
              name="Query Pararmeters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token" />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The equipment field contains a list of places with desktops. All the cluster spaces information are always returned.
            </p>
            <p>
              Each room has information about location and number of desktops and how many are available.
            </p>
            <Table
              name="Response">
              <Cell
                name="total_seats"
                extra="int"
                example="25"
                description="Total number of computers available in the room." />
              <Cell
                name="free_seats"
                extra="int"
                example="24"
                description="Number of free seats in the room." />
              <Cell
                name="latitude"
                extra="string"
                example="51.523481"
                description="latitude of the location of the site." />
              <Cell
                name="longitude"
                extra="string"
                example="50.523481"
                description="longitude of the location of the site." />
              <Cell
                name="postcode"
                extra="string"
                example="WC1E 6BT"
                description="Postcode of the location of the room" />
              <Cell
                name="address"
                extra="string"
                example="Malet Place, Gower Street."
                description="Address of the room." />
              <Cell
                name="roomname"
                extra="string"
                example="Ground-Ground floor - Public."
                description="Name of the room." />
              <Cell
                name="building_name"
                extra="string"
                example="DMS Watson Science Library."
                description="Name of the building." />
              <Cell
                name="room_status"
                extra="string"
                example="Room available all day."
                description="Some information about the room." />
            </Table>
          </Topic>

          <Topic
            noExamples={true}>
            <Table
              name="Errors">
              <Cell
                name="Could not parse the desktop availability data. Please try again later or contact us for support"
                description="We don't currently have the up to date data. Wait a while before you make next request." />
            </Table>
          </Topic>
        </div>
      )
    }

}
