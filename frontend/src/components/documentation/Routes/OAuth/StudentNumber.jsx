import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-user-abd-def-ghi-jkl",
  "client_secret": "secret",
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/oauth/user/studentnumber", params);

let response = `{
    "ok": true,
    "student_number": "123456789"
}`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}

export default class StudentNumber extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="oauth/user/studentnumber">Student Number</h1>
            <p>
              Endpoint: <code>https://uclapi.com/oauth/user/studentnumber</code>
            </p>
            <p>
              You can use the <code>oauth/user/data</code> endpoint to find out whether the user is a student before you call this endpoint. If you call this endpoint and the user is not a student, an error will be returned.
            </p>
            <p>
              Please note: to use this endpoint you must have ticked the <em>Student Number</em> scope for your application in the UCL API Dashboard. This piece of information has been separated from the others because a student number can in some cases be considered confidential. This is because any data exported directly from Portico, SITS (E:Vision) or CMIS is usually grouped by Student Number. One example is that in some cases departments choose to release spreadsheets of examination results where each student is identified by their student number, and not their name, to provide a degree of anonymity in what is otherwise an open data set. You should consider carefully whether you actually need a student number to track students when other unique identifiers are available, such as their username-based email address and UPI. If you request a student number and it is not required for your application, your users may choose not to provide this information to you, and therefore deny your application permission to access their details.
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-user-abd-def-ghi-jkl"
                description="OAuth user token." />
              <Cell
                name="client_secret"
                requirement="required"
                example="secret"
                description="Client ID of the authenticating app." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <Table
              name="Response">
            <Cell
              name="student_number"
              extra="string"
              example="123456789"
              description="The user's student number. This may be prefixed with a 0 so should be treated as a string, even though it is made up only of digits. The maximum possible length is 12 digits." />
            </Table>
          </Topic>

          <Topic
            noExamples={true}>
            <Table
              name="Errors">
              <Cell
                name="Token does not exist."
                description="Gets returned when token does not exist." />
              <Cell
                name="Client secret incorrect."
                description="Gets returned when the client secret was incorrect." />
              <Cell
                name="User is not a student."
                description="The user is not a student, and therefore has no student number that can be returned." />
            </Table>
          </Topic>
        </div>
      )
    }

}
