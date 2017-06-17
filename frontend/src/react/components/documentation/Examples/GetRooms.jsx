import React from 'react';

import Topic from './../Topic.jsx';
import Table from './../Table.jsx';
import Cell from './../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
}
r = requests.get("https://uclapi.com/roombookings/rooms", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}

let response = `{
   "ok": true,
   "bookings": [
      {
          "slotid": 998503,
          "end_time": "2016-09-02T18:00:00+00:00",
          "description": "split weeks to assist rooming 29.06",
          "roomname": "Torrington (1-19) 433",
          "siteid": "086",
          "contact": "Ms Leah Markwick",
          "weeknumber": 1,
          "roomid": "433",
          "start_time": "2016-09-02T09:00:00+00:00",
          "phone": "45699"
       },
       ...
    ],
    "next_page_exists": true,
    "page_token": "6hb14hXjRV",
    "count": 1197
}
`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetRooms extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1>Get Rooms</h1>
            <p>
              This endpoint returns rooms and information about them.
              If you don’t specify any query parameters besides the token, all rooms will be returned.
              Note: This endpoint only returns publicly bookable rooms.
              Departmentally bookable rooms are not included.
            </p>
            <Table
              name="Query Pararmeters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token" />
              <Cell
                name="roomname"
                requirement="optional"
                example="Cruciform Building B.3.05"
                description="The name of the room. It often includes the name of the site (building) as well." />
              <Cell
                name="roomid"
                requirement="optional"
                example="433"
                description="The room ID (not to be confused with the roomname)." />
              <Cell
                name="start_datetime"
                requirement="optional"
                example="2011-03-06T03:36:45+00:00"
                description="Start datetime of the booking. Returns bookings with a start_datetime after the one supplied. Follows the ISO 8601 formatting standard." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The room field contains a list of rooms that match your query.
              If no filters are applied, all rooms will be returned.
            </p>
            <Table
              name="Response">
              <Cell
                name="roomname"
                example="Wilkins Building (Main Building) Portico"
                description="The name of the room. It often includes the name of the site (building) as well."
                extra="string">
              </Cell>
            </Table>
          </Topic>
        </div>
      )
    }

}
