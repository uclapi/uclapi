import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "contact": "Mark"
}
r = requests.get("https://uclapi.com/roombookings/bookings", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/roombookings/bookings?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&contact=Mark`,

  javascript: `fetch("https://uclapi.com/roombookings/bookings?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&contact=Mark")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`
}


export default class GetPeople extends React.Component {

    render () {
      return (
        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={codeExamples}>
          <h1 id="rooms/get-bookings">Get Bookings</h1>
          <p>
            This endpoint shows the results to a bookings or space availability query.
            It returns a paginated list of bookings.
            Note: This endpoint only returns publicly displayed bookings.
            Departmental bookings are not included.
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
      )
    }

}
