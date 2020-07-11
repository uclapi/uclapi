import React from 'react'

import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'


const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("https://uclapi.com/dashboard/api/analytics/quota/", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/quota/ \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/quota/?token=
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
  "remaining": 1024
}
`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class RemainingQuota extends React.Component {
  render() {
    return (
      <div>
        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/quota">Daily Quota Left for Token</h1>
          <p>
            Endpoint: <code>https://uclapi.com/dashboard/api/analytics/quota</code>
          </p>

          <Table
            name="Query Parameters"
          >
            <Cell
              name="token"
              requirement="required"
              example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
              description="Token to check remaining quota of."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains the remaining daily quota for the token.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="remaining"
              extra="int"
              example="1024"
              description="Quota remaining for the token for today."
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
            <Cell
              name="Token is invalid"
              description="Gets returned when you supply an invalid token."
            />
          </Table>
        </Topic>
      </div>
)
}
}
