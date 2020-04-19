import PropTypes from 'prop-types'
import React from 'react'

import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic.jsx'


const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "query": "Jane"
}
r = requests.get("https://uclapi.com/search/people", params=params)
print(r.json())`,

  // eslint-disable-next-line no-secrets/no-secrets
  shell: `curl -G https://uclapi.com/search/people \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
-d query='Jane'`,

  // eslint-disable-next-line no-secrets/no-secrets
  javascript: `fetch("https://uclapi.com/search/people?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&query=Jane")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`,
}


const response = `{
  "ok": true,
  "people": [
    {
      "name": "Jane Doe",
      "status": "Student",
      "department": "Dept of Med Phys & Biomedical Eng",
      "email": "jane.doe.17@ucl.ac.uk"
    },
    ...
  ]
}
`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}


export default class GetEquiment extends React.Component {

  static propTypes = {
    activeLanguage: PropTypes.string,
  }

  render() {
    const { activeLanguage } = this.props
    return (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="search/people">Get People</h1>
          <p>
            This endpoint returns matching people and information about them.
            </p>
          <p>
            <i>
              Note: This endpoint only returns a maximum of 20 matches.
              </i>
          </p>
          <p>
            <i>
              Following a change to UCL&apos;s systems in 2019, this endpoint only returns
              staff. Students will not be returned through this API.
            </i>
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
              name="query"
              requirement="required"
              example="Jane"
              description="Name of the person you are searching for."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={this.props.activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The people field contains a list of people that match your query.
            </p>
          <Table
            name="Response"
          >
            <Cell
              name="name"
              extra="string"
              example="Jane Doe"
              description="The name of the person."
            />
            <Cell
              name="status"
              extra="string"
              example="Staff"
              description={`
                Since only staff are returned through this API,
                this should always be Staff.`
              }
            />
            <Cell
              name="department"
              extra="string"
              example="UCL Medical School"
              description="The department the member of staff works under."
            />
            <Cell
              name="email"
              extra="string"
              example="jane.doe.17@ucl.ac.uk"
              description="The email of the person."
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
            <Cell
              name="Token does not exist"
              description="Gets returned when you supply an invalid token."
            />
            <Cell
              name="No query provided"
              description="Gets returned when you have not supplied a query in your request."
            />
          </Table>
        </Topic>
      </div>
    )
  }

}
