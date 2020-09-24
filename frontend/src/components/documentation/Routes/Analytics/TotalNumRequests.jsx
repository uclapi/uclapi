import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("https://uclapi.com/dashboard/api/analytics/total/", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/total/ \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/total/?token=
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
  "num": 1024
}
`

const responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

export default class TotalNumRequests extends React.Component {
  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/total">Total Number of Requests</h1>
          <p>
            Endpoint: <code>https://uclapi.com/dashboard/api/analytics/total</code>
          </p>

          <Table
            name="Query Parameters"
          >
            <Cell
              name="token"
              requirement="required"
              example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
              description="Token to check usage of."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains the total number of requests made from a given token.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="num"
              extra="int"
              example="1024"
              description="The number of requests made with the token."
            />
          </Table>
        </Topic>

        <Topic noExamples>
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
