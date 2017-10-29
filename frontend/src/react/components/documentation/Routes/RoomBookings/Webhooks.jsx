import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let eventsResponse = `{
  "service": "webhooks",
  "name": "challenge",
  "verification_secret": "bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a",
  ...
}`

let eventsResponseExample = {
  python: eventsResponse,
  javascript: eventsResponse,
  shell: eventsResponse
}

let challengeEvent = `# Request from UCL API to your endpoint

{
  "service": "webhooks",
  "name": "challenge",
  "verification_secret": "bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a",
  "challenge": "f9b4fd5325e21e3-002e9e00a1b1af6-bc37b346d59b0cb-730043261cfa206"
}


# Prompt response from your server to verify URL control

{
  "challenge": "f9b4fd5325e21e3-002e9e00a1b1af6-bc37b346d59b0cb-730043261cfa206"
}
`

let challengeEventExample = {
  python: challengeEvent,
  javascript: challengeEvent,
  shell: challengeEvent
}

let bookingsChanged = `{
  "service": "roombookings",
  "name": "bookings_changed",
  "verification_secret": "bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a",
  "content": {
    "bookings_added": [
      {
        "phone": null,
        "contact": "Room Closed",
        "weeknumber": 52,
        "description": "Rm. Closed",
        "start_time": "2017-08-27T23:00:00+01:00",
        "roomid": "G08",
        "siteid": "013",
        "roomname": "Chadwick Building G08",
        "slotid": 907872,
        "end_time": "2017-08-27T23:30:00+01:00"
      },
    ...
    ],
    "bookings_removed": [
      {
        "weeknumber": 45,
        "end_time": "2017-07-07T18:00:00+01:00",
        "slotid": 1631230,
        "phone": null,
        "roomid": "B1.03",
        "siteid": "212",
        "description": "Summer School",
        "roomname": "Cruciform Building B1.03",
        "contact": "Michael Arthur",
        "start_time": "2017-07-07T09:00:00+01:00"
      },
    ...
    ]
  }
}`

let bookingsChangedExample = {
  python: bookingsChanged,
  javascript: bookingsChanged,
  shell: bookingsChanged
}


export default class GetEquiment extends React.Component {

    render () {
      return (
        <div>
          <Topic
            noExamples={true}>
            <h1 id="roombookings/webhooks">Webhooks</h1>
            <p>
              With webhooks, you don’t send HTTP requests to us, we send HTTP requests to you. This is useful for data that changes frequently, such as room bookings. Whenever a booking gets added or removed, we’ll send those details to your server.
            </p>

            <h2>Setup</h2>
            <p>After creating an app in the dashboard, you can configure webhook settings in the app settings view.</p>


            <Table
              name="Settings">
              <Cell
                name="Verification Secret"
                requirement="required"
                example="bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a"
                description="Random string that you use to make sure that all requests to your webhook URL come from UCL API servers, and not a third party. You must keep this secret." />
              <Cell
                name="Webhook URL"
                requirement="required"
                example="https://example.com/webhook"
                description="The URL must use https and must be a publicly accessible URL. This is the URL we’ll send events to." />
              <Cell
                name="siteid"
                requirement="optional"
                example="086"
                description="In case you want to restrict the booking events you receive to only one specific siteid." />
              <Cell
                name="roomid"
                requirement="optional"
                example="433"
                description="In case you want to restrict the booking events you receive to only one specific roomid." />
              <Cell
                name="contact"
                requirement="optional"
                example="Michael Arthur"
                description=" In case you want to restrict the booking events you receive to only one specific contact." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={eventsResponseExample}>
            <h2>Events</h2>
            <p>Whenever you receive data on your webhook we call that an “event”. At the moment there are 2 events: <code>challenge</code> and <code>booking_changed</code></p>
            <p>
              Events are always delivered as POST requests to your webhook URL. The data will be JSON inside the body of the POST request. Every event will contain at least 3 components: <code>service</code>, <code>name</code>, <code>verification_secret</code>. You can see an example on the right.
            </p>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={challengeEventExample}>
            <h2>challenge event</h2>
            <p>
              You’ll receive this event when you first input or alter your webhook URL. It exists to make sure that the URL you entered is under your control. The JSON data sent to you contains a <code>challenge</code> parameter. You need to set up your code to respond promptly with a JSON object containing only the challenge parameter.
            </p>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={bookingsChangedExample}>
            <h2>bookings_changed event</h2>
            <p>
              You’ll receive this event when a booking was either added or removed. You can see an example on the right.
A <code>bookings_changed</code> event contains at least either one <code>bookings_added</code> or <code>bookings_removed</code> key, but not necessarily both.
            </p>
          </Topic>
        </div>
      )
    }

}
