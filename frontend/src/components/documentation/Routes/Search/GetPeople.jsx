import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "query": "Jane"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/search/people", params);

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
              name="Query Parameters">
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
            The people field contains a list of people that match your query.
            </p>
            <Table
              name="Response">
              <Cell
                name="name"
                extra="string"
                example="Jane Doe"
                description="The name of the person."/>
              <Cell
                name="status"
                extra="string"
                example="Staff"
                description="Tells us whether the person is a student or member of staff."/>
              <Cell
                name="department"
                extra="string"
                example="UCL Medical School"
                description="The department the student studies or works under."/>
              <Cell
                name="email"
                extra="string"
                example="jane.doe.17@ucl.ac.uk"
                description="The email of the person."/>
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
