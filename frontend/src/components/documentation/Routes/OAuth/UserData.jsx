import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-user-abd-def-ghi-jkl",
  "client_secret": "secret",
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/oauth/user/data", params);

let response = `{
    "department": "Dept of Department",
    "email": "xxxxxxx@ucl.ac.uk",
    "ok": true,
    "full_name": "Full Name",
    "cn": "xxxxxxx",
    "given_name": "Full",
    "upi": "fname12",
    "scope_number": 0,
    "is_student": true
}`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class UserData extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="oauth/user/data">User Data</h1>
            <p>
              Endpoint: <code>https://uclapi.com/oauth/user/data</code>
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
              name="ok"
              extra="boolean"
              example="true"
              description="Returns if the query was successful." />
            <Cell
              name="email"
              extra="string"
              example="zcabmrk@ucl.ac.uk"
              description="E-mail for the given user." />
            <Cell
              name="full_name"
              extra="string"
              example="Martin Mrkvicka"
              description="Full name of the user. Can be an empty string." />
            <Cell
              name="department"
              extra="string"
              example="Dept Of Computer Science"
              description="Department the user belongs to. Can be an empty string." />
            <Cell
              name="cn"
              extra="string"
              example="zcabmrk"
              description="UCL username of the given user." />
            <Cell
              name="given_name"
              extra="string"
              example="Martin"
              description="Given first name of the user. Can be an empty string." />
            <Cell
              name="upi"
              extra="string"
              example="mmrkv12"
              description="Unique Person Identifier." />
            <Cell
              name="scope_number"
              extra="int"
              example="0"
              description="Scopes the application has access to on behalf of the user." />
            <Cell
              name="is_student"
              extra="boolean"
              example="true"
              description="Whether the user is a student in this academic year." />
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
            </Table>
          </Topic>
        </div>
      )
    }

}
