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
  "datetime__gte": "2020-01-16T14:00:00",
  "datetime__lte": "2020-01-16T15:00:00"
}

r = requests.get("${Constants.DOMAIN}/workspaces/historical/data", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/workspaces/historical/data \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
-d survey_id=72 \
-d sensor_id=20664009 \
-d datetime__gte="2020-01-16T14:00:00" \
-d datetime__lte="2020-01-16T15:00:00"`,

  javascript: `fetch("${Constants.DOMAIN}/workspaces/historical/data?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&survey_id=72&datetime__gte=2020-01-16T14%3A00%3A00&datetime__lte=2020-01-16T15%3A00%3A00&sensor_id=20664009",
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
  "data": {
    "next": null,
    "previous": null,
    "results": [
      {
        "sensor_id": 20664009,
        "datetime": "2020-01-16T14:20:00",
        "state": 1
      },
      {
        "sensor_id": 20664009,
        "datetime": "2020-01-16T14:50:00",
        "state": 0
      }
    ]
  }
}`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const WorkspacesHistoricalList = ({activeLanguage}) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="workspaces/historical/data">List Data</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/workspaces/historical/data</code>
        </p>
        <p>
          This endpoint provides historical sensor readings for all sensors in all survey locations. This must be
          restricted to a single survey location with survey_id and can be optionally restricited to a single sensor
          with sensor_id. To specify a start time datetime__gte (datetime greater than or equal to) and for an end
          time datetime__lte (datetime less than or equal to) can be used. The deltas (changes) of a sensor will be
          returned. Conforms to CursorPagination from Django REST.
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
          {/* eslint-disable no-secrets/no-secrets */}
          <Cell
            name="cursor"
            requirement="optional"
            example="bz0xJnA9MjAyMC0wMS0xNysxMiUzQTQwJTNBMDA%3D"
            description="Cursor to fetch the next or previous page of results."
          />
          {/* eslint-enable no-secrets/no-secrets */}
          <Cell
            name="survey_id"
            requirement="required"
            example="72"
            description="The ID of the survey/library."
          />
          <Cell
            name="sensor_id"
            requirement="optional"
            example="20664009"
            description="The ID of the sensor."
          />
          <Cell
            name="datetime__gte"
            requirement="optional"
            example="2020-01-16T14:00:00"
            description="Filter datetime greater than or equal to datetime."
          />
          <Cell
            name="datetime__lte"
            requirement="optional"
            example="2020-01-16T15:00:00"
            description="Filter datetime less than or equal to datetime."
          />
          <Cell
            name="datetime__exact"
            requirement="optional"
            example="2020-01-16T14:50:00"
            description="Filter datetime equal to datetime."
          />
          <Cell
            name="datetime__gt"
            requirement="optional"
            example="2020-01-16T14:00:00"
            description="Filter datetime greater than datetime."
          />
          <Cell
            name="datetime__lt"
            requirement="optional"
            example="2020-01-16T15:00:00"
            description="Filter datetime less than datetime."
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
            name="sensor_id"
            extra="integer"
            example={`20520001`}
            description="The id of the sensor."
          />
          <Cell
            name="datetime"
            extra="string[ISO 8601]"
            example={`2020-01-16T14:20:00`}
            description="The datetime of the sensor state changing."
          />
          <Cell
            name="state"
            extra="integer"
            example={`1`}
            description="The state of the sensor, 1 = occupied, 0 = absent, -1 = unknown."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalList
