import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("${Constants.DOMAIN}/dashboard/api/analytics/oauth/total_by_dept/", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/dashboard/api/analytics/oauth/total_by_dept/ \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("${Constants.DOMAIN}/dashboard/api/analytics/oauth/total_by_dept/?token=
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

const responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

export default class UsersPerAppPerDept extends React.Component {
  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/oauth/total_by_dept">Total Number of Users for an App by Department</h1>
          <p>
            Endpoint:&nbsp;
            <code>
              {Constants.DOMAIN}/dashboard/api/analytics/oauth/total_by_dept
            </code>
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
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains the total number of&nbsp;
            users for an app by department.
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
