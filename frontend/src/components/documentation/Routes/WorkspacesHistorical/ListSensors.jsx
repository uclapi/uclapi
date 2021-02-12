import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
}

r = requests.get("${Constants.DOMAIN}/workspaces/historical/sensors", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/workspaces/historical/sensors \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb` ,

  javascript: `fetch("${Constants.DOMAIN}/workspaces/historical/sensors?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
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
  "okay": true,
  "sensors": {
    "next": "${Constants.DOMAIN}/workspaces/historical/sensors?page=2",
    "previous": null,
    "count": 17936,
    "results": [
      {
        "survey_id": 4,
        "sensor_id": 20520001,
        "hardware_id": 520001,
        "survey_device_id": 1
      },
      {
        "survey_id": 4,
        "sensor_id": 20520002,
        "hardware_id": 520002,
        "survey_device_id": 2
      }, ...
    ]
  }
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
          sensors from workspaces). Conforms to StandardResultsSetPagination from Django REST.
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
            name="page"
            requirement="optional"
            example="2"
            description="Page of pagination results, see url in next field."
          />
          <Cell
            name="survey_id"
            requirement="optional"
            example="72"
            description="The ID of the survey/library."
          />
          <Cell
            name="sensor_id"
            requirement="optional"
            example="20520002"
            description="The ID of a single sensor."
          />
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={responseCodeExample}
      >
        <h2>Response</h2>
        <p>
          This endpoint will return a list of every sensor.
        </p>
        <Table
          name="Response"
        >
          <Cell
            name="survey_id"
            extra="integer"
            example={`4`}
            description="The id of the survey location."
          />
          <Cell
            name="sensor_id"
            extra="integer"
            example={`20520001`}
            description="The id of the sensor."
          />
          <Cell
            name="hardware_id"
            extra="integer"
            example={`520001`}
            description="The hardware id of the sensor."
          />
          <Cell
            name="survey_device_id"
            extra="integer"
            example={`1`}
            description="The survey device id of the sensor."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalListSurveys
