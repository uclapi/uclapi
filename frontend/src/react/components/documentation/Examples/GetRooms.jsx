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

export default class GetRooms extends React.Component {

    render () {
      return (
        <Topic codeExamples={codeExamples}>
          <h1>Get Rooms</h1>
          <p>
            This endpoint returns rooms and information about them.
            If you don’t specify any query parameters besides the token, all rooms will be returned.
            Note: This endpoint only returns publicly bookable rooms.
            Departmentally bookable rooms are not included.
          </p>
          <Table name="Query Pararmeters">
            <Cell
              name="token"
              required={true}
              example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
              description="Authentication token" />
            <Cell
              name="roomname"
              example="Cruciform Building B.3.05"
              description="The name of the room. It often includes the name of the site (building) as well." />
            <Cell
              name="roomid"
              example="433"
              description="The room ID (not to be confused with the roomname)." />
            <Cell
              name="start_datetime"
              example="2011-03-06T03:36:45+00:00"
              description="Start datetime of the booking. Returns bookings with a start_datetime after the one supplied. Follows the ISO 8601 formatting standard." />
          </Table>
        </Topic>
      )
    }

}
