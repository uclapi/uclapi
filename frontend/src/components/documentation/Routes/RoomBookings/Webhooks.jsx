import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'

const eventsResponse = `{
  "service": "webhooks",
  "name": "challenge",
  "verification_secret": "bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a",
  ...
}`

const eventsResponseExample = {
  python: eventsResponse,
  javascript: eventsResponse,
  shell: eventsResponse,
}

const challengeEvent = `# Request from UCL API to your endpoint

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

const challengeEventExample = {
  python: challengeEvent,
  javascript: challengeEvent,
  shell: challengeEvent,
}

const bookingsChanged = `{
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

const bookingsChangedExample = {
  python: bookingsChanged,
  javascript: bookingsChanged,
  shell: bookingsChanged,
}

const Webhooks = ({ activeLanguage }) => {
  return (
    <div>
      <Topic
        noExamples
      >
        <h1 id="roombookings/webhooks">Webhooks</h1>
        <p>
          Webhooks allow you to receive updates and execute code
          in response to a change in our data.
          Instead of pulling data from our API with HTTP requests,
          setting a webhook allows us to push data to you via HTTP requests
          as and when the data changes.
          
          This is useful for data that changes frequently,
          such as room bookings.

          Whenever a booking gets added or removed,
          we’ll send details about the booking to your webhook.
        </p>

        <h2>Setup</h2>
        <p>
          After creating an app in the <a href="/dashboard">Dashboard</a>,
          you can set a webhook for that app.
        </p>

        <Table
          name="Settings"
        >
          <Cell
            name="Verification Secret"
            requirement="required"
            example="bc35f27d47742f7-c3bd7768defb2c2-1c556d86859419a-897b8dc9273691a"
            description="Random string that you use to make sure that all requests to your webhook URL come from UCL API servers, and not a third party. You must keep this secret."
          />
          <Cell
            name="Webhook URL"
            requirement="required"
            example="https://example.com/webhook"
            description="The URL must use https and must be a publicly accessible URL. This is the URL we’ll send events to."
          />
          <Cell
            name="siteid"
            requirement="optional"
            example="086"
            description="In case you want to restrict the booking events you receive to only one specific siteid."
          />
          <Cell
            name="roomid"
            requirement="optional"
            example="433"
            description="In case you want to restrict the booking events you receive to only one specific roomid."
          />
          <Cell
            name="contact"
            requirement="optional"
            example="Michael Arthur"
            description=" In case you want to restrict the booking events you receive to only one specific contact."
          />
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={eventsResponseExample}
      >
        <h2>Events</h2>
        <p>
          Whenever you receive data on your webhook we call that an “event”.
          At the moment there are 2 events we send:
          <code>challenge</code> and <code>bookings_changed</code>.</p>
        <p>
          Events are always delivered as POST requests to your webhook URL.
          The data will be JSON inside the body of the POST request.
          Every event will contain at least 3 components:
          <code>service</code>,
          <code>name</code>,
          <code>verification_secret</code>.
          You can see an example on the right.
        </p>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={challengeEventExample}
      >
        <h2 id="webhook/challenge-event">challenge event</h2>
        <p>
          You’ll receive this event when you set or change your webhook URL.
          It exists to make sure that the URL you entered is under your control.
          The JSON data sent to you contains a <code>challenge</code> parameter.
          You need to set up your code to respond promptly with a JSON object
          containing only the <code>challenge</code> parameter.
        </p>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={bookingsChangedExample}
      >
        <h2 id="webhook/bookings_changed-event">bookings_changed event</h2>
        <p>
          You’ll receive this event when a booking is either added or removed.
          You can see an example on the right.
          A <code>bookings_changed</code> event contains at least either one
          <code>bookings_added</code> or <code>bookings_removed</code> key,
          but not necessarily both.
        </p>
      </Topic>
    </div>
  )
}

export default Webhooks
