import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("https://uclapi.com/dashboard/api/analytics/oauth/total/", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/oauth/total/ \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/oauth/total/?token=
  uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
  "ok": true,
  "users": 1024
}
`

const responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

export default class UsersPerApp extends React.Component {
  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/oauth/total">Total Number of Users for an App</h1>
          <p>
            Endpoint:&nbsp;
            <code>https://uclapi.com/dashboard/api/analytics/oauth/total</code>
          </p>

          <Table
            name="Query Parameters"
          >
            <Cell
              name="token"
              requirement="required"
              example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
              description="Token of app to check users of."
            />
            <Cell
              name="start_date"
              requirement="optional"
              example="2020-12-20"
              description="Start date to filter by."
            />
            <Cell
              name="end_date"
              requirement="optional"
              example="2020-12-30"
              description="End date to filter by."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains the total number of&nbsp;
            users for an app, optionally filtered by date.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="users"
              extra="int"
              example="1024"
              description="The number of users for the app."
            />
          </Table>
        </Topic>

        <Topic
          noExamples
        >
          <Table
            name="Errors"
          >
            <Cell
              name="No token provided"
              description="Gets returned when you have not supplied a token in your request."
            />
          </Table>
        </Topic>
      </div>
    )
  }
}
