import propTypes from 'prop-types'
import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-user-abd-def-ghi-jkl",
  "client_secret": "secret",
}
r = requests.get("${Constants.DOMAIN}/oauth/user/data", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/oauth/user/data \
-d client_secret=secret \\
-d token=uclapi-user-abd-def-ghi-jkl`,

  javascript: `fetch("${Constants.DOMAIN}/oauth/user/data?client_secret=secret&token=uclapi-user-abd-def-ghi-jkl")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
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

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const UserData = ({ activeLanguage }) => (
  <div>
    <Topic
      activeLanguage={activeLanguage}
      codeExamples={codeExamples}
    >
      <h1 id="oauth/user/data">User Data</h1>
      <p>
        Endpoint: <code>{Constants.DOMAIN}/oauth/user/data</code>
      </p>

      <Table
        name="Query Parameters"
      >
        <Cell
          name="token"
          requirement="required"
          example="uclapi-user-abd-def-ghi-jkl"
          description="OAuth user token."
        />
        <Cell
          name="client_secret"
          requirement="required"
          example="secret"
          description="Client ID of the authenticating app."
        />
      </Table>
    </Topic>

    <Topic
      activeLanguage={activeLanguage}
      codeExamples={responseCodeExample}
    >
      <h2>Response</h2>
      <Table
        name="Response"
      >
        <Cell
          name="ok"
          extra="boolean"
          example="true"
          description="Returns if the query was successful."
        />
        <Cell
          name="email"
          extra="string"
          example="zcabmrk@ucl.ac.uk"
          description="E-mail for the given user."
        />
        <Cell
          name="full_name"
          extra="string"
          example="Martin Mrkvicka"
          description="Full name of the user. Can be an empty string."
        />
        <Cell
          name="department"
          extra="string"
          example="Dept Of Computer Science"
          description="Department the user belongs to. Can be an empty string."
        />
        <Cell
          name="cn"
          extra="string"
          example="zcabmrk"
          description="UCL username of the given user."
        />
        <Cell
          name="given_name"
          extra="string"
          example="Martin"
          description="Given first name of the user. Can be an empty string."
        />
        <Cell
          name="upi"
          extra="string"
          example="mmrkv12"
          description="Unique Person Identifier."
        />
        <Cell
          name="scope_number"
          extra="int"
          example="0"
          description="Scopes the application has access to on behalf of the user."
        />
        <Cell
          name="is_student"
          extra="boolean"
          example="true"
          description="Whether the user is a student in this academic year."
        />
        <Cell
          name="ucl_groups"
          extra="string"
          example="ucl-all;ucl-ug;"
          description="A semi-colon delimited string of all UCL intranet groups that the user belongs to"
        />
        <Cell
          name="sn"
          extra="string"
          example="Mrkvicka"
          description="Given second name/surname of the user. Can be an empty string."
        />
        <Cell
          name="mail"
          extra="string"
          example="martin.mrkvicka.20@ucl.ac.uk"
          description="Alternative (pretty format) E-mail for the given user."
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
          name="Token does not exist."
          description="Gets returned when token does not exist."
        />
        <Cell
          name="Client secret incorrect."
          description="Gets returned when the client secret was incorrect."
        />
      </Table>
    </Topic>
  </div>
)

UserData.propTypes = {
  activeLanguage: propTypes.string,
}

UserData.defaultProps = {
  activeLanguage: `python`,
}

export default UserData
