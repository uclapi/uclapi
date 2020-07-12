import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'

const codeExamples = {
  python: `import requests
  
params = {
  "service": "roombookings",
}

r = requests.get("https://uclapi.com/dashboard/api/analytics/methods/", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/dashboard/api/analytics/methods/ \
  -d service=roombookings`,

  javascript: `fetch("https://uclapi.com/dashboard/api/analytics/methods/?service=roombookings")
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
      "method": "rooms",
      "count": 1024
    },
    {
      "method": "bookings",
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

export default class MostPopularMethod extends React.Component {
  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="dashboard/api/analytics/methods">Methods by Popularity</h1>
          <p>
            Endpoint:&nbsp;
            <code>https://uclapi.com/dashboard/api/analytics/methods</code>
          </p>

          <Table
            name="Query Parameters"
          >
            <Cell
              name="service"
              requirement="optional"
              example="roombookings"
              description="Service to check popularity of methods of."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The response contains all methods for a given service,
            or all services, by popularity.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="data"
              extra="List"
              example="-"
              description={
                `List of objects containing a method `+
                `name and the number of requests each has recieved.`
              }
            />
          </Table>
        </Topic>
      </div>
    )
  }
}
