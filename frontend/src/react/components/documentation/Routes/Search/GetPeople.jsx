import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "query": "Jane"
}
r = requests.get("https://uclapi.com/search/people", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/search/people \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb
-d query='Jane'`,

  javascript: `fetch("https://uclapi.com/search/people?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&query=Jane")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`
}


let response = `{
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

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetEquiment extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="search/people">Get People</h1>
            <p>
              This endpoint returns matching people and information about them.
            </p>
            <p>
              <i>
                Note: This endpoint only returns a maximum of 20 matches.
              </i>
            </p>

            <Table
              name="Query Pararmeters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
              <Cell
                name="query"
                requirement="required"
                example="Jane"
                description="Name of the person you are searching for." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The equipment field contains a list of equipment items. This list can have a different length depending on the room, and it can also be empty.
            </p>
            <p>
              Each equipment item contains a type, a description, and the number of units.
            </p>
            <Table
              name="Response">
              <Cell
                name="type"
                extra="string"
                example="FE"
                description="The type of equipment. Either Fixed Equipment (FE) or Fixed Feature (FF)." />
              <Cell
                name="description"
                extra="string"
                example="Managed PC"
                description="What the piece of equipment actually is." />
              <Cell
                name="units"
                extra="int"
                example="1"
                description="The number of times this piece of equipment exists in the room." />
            </Table>
          </Topic>

          <Topic
            noExamples={true}>
            <Table
              name="Errors">
              <Cell
                name="No token provided"
                description="Gets returned when you have not supplied a token in your request." />
              <Cell
                name="Token does not exist"
                description="Gets returned when you supply an invalid token." />
              <Cell
                name="No query provided"
                description="Gets returned when you have not supplied a query in your request." />
            </Table>
          </Topic>
        </div>
      )
    }

}
