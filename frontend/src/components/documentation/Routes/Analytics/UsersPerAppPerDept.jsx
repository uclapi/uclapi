import React from 'react'

import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'


const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("https://uclapi.com/dashboard/api/analytics/oauth/total_by_dept/", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/oauth/total_by_dept/ \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/oauth/total_by_dept/?token=
  uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

let response = `{
  "ok": true,
  "data": [
    {
      "department": "Dept of Computer Science",
      "count": 100,
    },
    {
      "department": "Dept of Mechanical Engineering",
      "count" 50,
    }
  ]
}
`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

export default class UsersPerAppPerDept extends React.Component {
  render() {
    return (
      <div>
        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/oauth/total_by_dept">Total Number of Users for an App by Department</h1>
          <p>
            Endpoint: <code>https://uclapi.com/dashboard/api/analytics/oauth/total_by_dept</code>
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
          </Table>
        </Topic>

        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains the total number of users for an app by department.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="data"
              extra="list"
              example="-"
              description="List of departments users for the app are from and quantity per department."
            />
          </Table>
        </Topic>

        <Topic
          noExamples={true}
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
