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

r = requests.get("${Constants.DOMAIN}/workspaces/historical/surveys", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/workspaces/historical/surveys \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("${Constants.DOMAIN}/workspaces/historical/surveys?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
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
  "surveys": {
    "next": null,
    "previous": null,
    "count": 71,
    "results": [
      {
        "survey_id": 4,
        "name": "Ophthamology Library old",
        "start_datetime": "2017-09-25T09:00:00",
        "end_datetime": "2020-12-25T17:00:00",
        "active": false,
        "last_updated": "2020-12-21T00:00:00"
      },
      {
        "survey_id": 6,
        "name": "UCL Anatomy Hub ",
        "start_datetime": "2017-09-24T08:00:00",
        "end_datetime": "2030-12-31T20:00:00",
        "active": true,
        "last_updated": "2020-12-21T00:00:00"
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
        <h1 id="workspaces/historical/surveys">List Surveys</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/workspaces/historical/surveys</code>
        </p>
        <p>
          This endpoint lists all historical survey locations, this includes inactive survey locations (unlike get
          survey from workspaces). Conforms to StandardResultsSetPagination from Django REST.
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
            example="37"
            description="Survey ID."
          />
          <Cell
            name="active"
            requirement="optional"
            example="true"
            description="If a survey location is active (true) or not (false)."
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
            name="start_datetime"
            extra="string[ISO 8601]"
            example={`2019-07-06T08:00:00`}
            description="The start datetime of the survey location."
          />
          <Cell
            name="end_datetime"
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
            name="last_updated"
            extra="string[ISO 8601]"
            example={`2020-01-02T02:00:00`}
            description="The last time the survey location was updated."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalListSurveys
