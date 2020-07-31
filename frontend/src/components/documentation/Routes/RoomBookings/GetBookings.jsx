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

  shell: `curl -G https://uclapi.com/roombookings/bookings \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
-d contact=Mark`,

  javascript: `fetch("https://uclapi.com/roombookings/bookings?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&contact=Mark")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`
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


export default class GetBookings extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="roombookings/bookings">Get Bookings</h1>
            <p>
              Endpoint: <code>https://uclapi.com/roombookings/bookings</code>
            </p>
            <p>
              This endpoint shows the results to a bookings or space availability query.
              It returns a paginated list of bookings. Note: This endpoint only returns publicly displayed bookings. Departmental bookings are not included.
            </p>
            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
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
              <Cell
                name="end_datetime"
                requirement="optional"
                example="2011-03-06T03:36:45+00:00"
                description="End datetime of the booking. Returns bookings with an end_datetime before the one supplied. Follows the ISO 8601 formatting standard." />
              <Cell
                name="date"
                requirement="optional"
                example="20160202"
                description="Date of the bookings you need, in the format YYYYMMDD. Returns bookings occurring on this day. This query parameter is only considered when end_datetime and start_datetime are not supplied." />
              <Cell
                name="siteid"
                requirement="optional"
                example="086"
                description="Every room is inside a site (building). All sites have IDs." />
              <Cell
                name="description"
                requirement="optional"
                example="Lecture"
                description="Describes what the booking is. Could contain a module code (for example WIBRG005) or just the type of activity (for example Lecture)." />
              <Cell
                name="contact"
                requirement="optional"
                example="Mark Herbster"
                description="The name of the person who made the booking. Substrings of the contact name can be used: Queries for Mark will include Mark Herbster. Sometimes, a society or student group may be the contact for a booking." />
              <Cell
                name="results_per_page"
                requirement="optional"
                example="50"
                description="Number of bookings returned per page. Maximum allowed value is 1000. Defaults to 1000." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <Table
              name="Response">
              <Cell
                name="ok"
                extra="boolean"
                example="true"
                description="Boolean indicating whether the request was successful." />
              <Cell
                name="bookings"
                extra="array"
                example="-"
                description="An array of booking objects." />
              <Cell
                name="next_page_exists"
                extra="boolean"
                example="true"
                description="True if there is another page containing more bookings." />
              <Cell
                name="page_token"
                extra="string"
                example="6hb14hXjRV"
                description="Page token parameter that needs to be supplied to view subsequent pages. Only included when the next page exists." />
              <Cell
                name="count"
                extra="int"
                example="1197"
                description="Total number of bookings matching the query. The count field will only be in the first response to a query." />
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
                name="date/time isn't formatted as suggested in the docs"
                description="Passed datetime parameter does not conform to the ISO8601 format." />
              <Cell
                name="results_per_page should be an integer"
                description="results_per_page should always be an integer." />
              <Cell
                name="Page token does not exist"
                description="The passed page_token parameter isn’t a valid one." />
              </Table>
          </Topic>
        </div>
      )
    }

}
