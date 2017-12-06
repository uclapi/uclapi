import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-user-abd-def-ghi-jkl",
  "client_secret": "secret",
}
r = requests.get("https://uclapi.com/oauth/token", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/oauth/user/data?client_secret=secret&token=uclapi-user-abd-def-ghi-jkl`,

  javascript: `fetch("https://uclapi.com/oauth/user/data?client_secret=secret&token=uclapi-user-abd-def-ghi-jkl")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}

let response = `{
    "department": "Dept of Department",
    "email": "xxxxxxx@ucl.ac.uk",
    "ok": true,
    "full_name": "Full Name",
    "cn": "xxxxxxx",
    "given_name": "Full",
    "upi": "fname12",
    "scope_number": 0,
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
                name="client_id"
                requirement="required"
                example="123.456"
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
              name="department"
              extra="string"
              example="Dept Of Computer Science"
              description="Department the user belongs to." />
            <Cell
              name="email"
              extra="string"
              example="zcabmrk@ucl.ac.uk"
              description="E-mail for the given user." />
            <Cell
              name="ok"
              extra="boolean"
              example="true"
              description="Returns if the query was successful." />
            <Cell
              name="full_name"
              extra="string"
              example="Martin Mrkvicka"
              description="Full name of the user." />
            <Cell
              name="department"
              extra="string"
              example="Dept Of Computer Science"
              description="Department the user belongs to." />
            <Cell
              name="cn"
              extra="string"
              example="."
              description="No idea." />
            <Cell
              name="given_name"
              extra="string"
              example="Martin"
              description="Given first name of the user." />
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
