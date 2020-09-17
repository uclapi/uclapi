import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'



const codeExamples = {
  python: `import requests

r = requests.get("https://uclapi.com/dashboard/api/analytics/services/")
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/services/`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/services/")
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
      "service": "roombookings",
      "count": 1024
    },
    {
      "service": "workspaces",
      "count": 500
    }
  ]
}
`

const responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

export default class MostPopularService extends React.Component {
  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/services">Services by Popularity</h1>
          <p>
            Endpoint:&nbsp;
            <code>https://uclapi.com/dashboard/api/analytics/services</code>
          </p>
        </Topic>

        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains all services by popularity.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="data"
              extra="List"
              example="-"
              description={
                `List of objects containing a service name `+
                `and the number of requests each has recieved.`
              }
            />
          </Table>
        </Topic>
      </div>
    )
  }
}
