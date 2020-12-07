import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests
  
params = {
  "service": "roombookings",
  "split_services": "false",
}

r = requests.get("${Constants.DOMAIN}/dashboard/api/analytics/methods", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/dashboard/api/analytics/methods \
  -d 'service=roombookings&split_services=false'`,

  javascript: `fetch("${Constants.DOMAIN}/dashboard/api/analytics/methods?service=roombookings&split_services=false")
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

const responseSplit = `{
  "ok": true,
  "data": {
    "roombookings": [
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
}
`

const responseCodeExample = {
    python: response,
    javascript: response,
    shell: response,
}

const responseCodeExampleSplit = {
    python: responseSplit,
    javascript: responseSplit,
    shell: responseSplit,
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
            <code>{Constants.DOMAIN}/dashboard/api/analytics/methods</code>
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
            <Cell
              name="split_services"
              requirement="optional"
              example="false"
              description="Group most popular methods by service."
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


        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExampleSplit}
        >
          <p>
            Alternatively, the response contains all methods of a given service,
            or all methods for each available services,
            if <code>split_services</code> is <code>true</code>.
          </p>
          <Table
            name="Response"
          >
            <Cell
              name="data"
              extra="object"
              example=""
              description={
                `Object containing services as keys. ` +
                `Each service's value is a List of objects containing a method name and the number of requests each has recieved. `
              }
            />
          </Table>
        </Topic>
      </div>
    )
  }
}
