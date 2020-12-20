import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "survey_id": 72,
  "sensor_id": 20664009,
  "start": "2020-01-16T14:00:00",
  "end": "2020-01-16T15:00:00"
}

r = requests.get("${Constants.DOMAIN}/workspaces/historical/sensors", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/workspaces/historical/sensors \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
-d survey_id=72 \
-d sensor_id=20664009 \
-d start="2020-01-16T14:00:00" \
-d end="2020-01-16T15:00:00"`,

  javascript: `fetch("${Constants.DOMAIN}/workspaces/historical/sensor?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&survey_id=72&start=2020-01-16T14%3A00%3A00&end=2020-01-16T15%3A00%3A00&sensor_id=20664009",
{
    method: "GET",
})
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
  "ok": true,
  "historical": {
    "2020-01-16T14:00:00": 0,
    "2020-01-16T14:10:00": 0,
    "2020-01-16T14:20:00": 1,
    "2020-01-16T14:30:00": 1,
    "2020-01-16T14:40:00": 1,
    "2020-01-16T14:50:00": 0,
    "2020-01-16T15:00:00": 0
  }
}`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const WorkspacesHistoricalGetSensor = ({activeLanguage}) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="workspaces/historical/sensor">Get Sensor</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/workspaces/historical/sensor</code>
        </p>
        <p>
          This endpoint provides historical sensor readings for a single sensor in a single survey location. From a
          start datetime to an end datetime. It can optionally provide only deltas (when the state changes).
        </p>
        <p>
          States: 1 = occupied, 0 = absent, -1 = unknown
        </p>

        <Table
          name="Query Parameters"
        >
          <Cell
            name="token"
            requirement="required"
            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
            description="Authentication token."
          />
          <Cell
            name="survey_id"
            requirement="required"
            example="72"
            description="The ID of the survey/library."
          />
          <Cell
            name="sensor_id"
            requirement="required"
            example="20664009"
            description="The ID of the sensor."
          />
          <Cell
            name="start"
            requirement="required"
            example="2020-01-16T14:00:00"
            description="The start datetime in ISO 8601."
          />
          <Cell
            name="end"
            requirement="optional"
            example="2020-01-16T15:00:00"
            description="The end datetime in ISO 8601, defaults to current datetime."
          />
          <Cell
            name="delta"
            requirement="optional"
            example="true"
            description="Only return deltas, defaults to false."
          />
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={responseCodeExample}
      >
        <h2>Response</h2>
        <p>
          This endpoint will return a dictionary of every sensor reading in the time range.
        </p>
        <Table
          name="Response"
        >
          <Cell
            name="workspaces"
            extra="dictionary"
            example={`{"2020-01-16T14:10:00": 0, "2020-01-16T14:20:00": 1}`}
            description="The occupancy of the sensor at the specified datetime."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalGetSensor
