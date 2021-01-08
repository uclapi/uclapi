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
  "historical": [
     {
      "survey_id": 72,
      "name": " Bedford Way LG16",
      "start": "2019-07-06T08:00:00",
      "end": "2030-12-31T20:00:00",
      "active": true
    }, ...
  ]
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
          survey from workspaces).
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
            name="workspaces"
            extra="list"
            example={`[{"survey_id": ...}, {}]`}
            description="The survey locations."
          />
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
        </Table>
      </Topic>
    </div>
  )
}

export default WorkspacesHistoricalListSurveys
