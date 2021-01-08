import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "survey_id": 72
}

r = requests.get("${Constants.DOMAIN}/workspaces/historical/sensors", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/workspaces/historical/sensors \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \
-d survey_id=72` ,

  javascript: `fetch("${Constants.DOMAIN}/workspaces/historical/sensors?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&survey_id=72",
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
    "survey_id": 72,
    "name": " Bedford Way LG16",
    "start": "2019-07-06T08:00:00",
    "end": "2030-12-31T20:00:00",
    "active": true,
    "sensors": [
      {
        "sensor_id": 20664008,
        "hardware_id": 664008,
        "survey_device_id": 14767
      },
      {
        "sensor_id": 20664005,
        "hardware_id": 664005,
        "survey_device_id": 14764
      }, ...
  ],
  "last_updated": "2020-12-16T00:00:00"
}`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const WorkspacesHistoricalListSurveys = ({activeLanguage}) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="workspaces/historical/sensors">List Sensors</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/workspaces/historical/sensors</code>
        </p>
        <p>
          This endpoint lists all sensors in a survey location, this includes inactive sensors (unlike get
          sensors from workspaces).
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
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={responseCodeExample}
      >
        <h2>Response</h2>
        <p>
          This endpoint will return a list of every survey location.
        </p>
        <Table
          name="Response"
        >
          <Cell
            name="survey_id"
            extra="integer"
            example={`72`}
            description="The id of the survey location."
          />
          <Cell
            name="name"
            extra="string"
            example={`Bedford Way LG16`}
            description="The name of the survey location."
          />
          <Cell
            name="start"
            extra="string[ISO 8601]"
            example={`2019-07-06T08:00:00`}
            description="The start datetime of the survey location."
          />
          <Cell
            name="end"
            extra="string[ISO 8601]"
            example={`2030-12-31T20:00:00`}
            description="The estimated end datetime of the survey location."
          />
          <Cell
            name="active"
            extra="boolean"
            example={`true`}
            description="If the survey location is currently active (collecting new data)."
          />
          <Cell
            name="sensors"
            extra="list"
            example={`[{"sensor_id": 20664008 ...}, {}, ...]`}
            description="List of sensors in the survey location."
          />
          <Cell
            name="sensors[n][sensor_id]"
            extra="integer"
            example={`20664008`}
            description="Sensor id (this is the id for requesting sensor data)."
          />
          <Cell
            name="sensors[n][hardware_id]"
            extra="integer"
            example={`664008`}
            description="Hardware id."
          />
          <Cell
            name="sensors[n][survey_device_id]"
            extra="integer"
            example={`14767`}
            description="Survey device id."
          />
          <Cell
            name="last_updated"
            extra="string[ISO 8601]"
            example={`"2020-12-16T00:00:00"`}
            description="Last time data recieved for this survey location (refreshes daily)."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalListSurveys
