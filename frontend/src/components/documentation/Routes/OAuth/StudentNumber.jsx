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
r = requests.get("${Constants.DOMAIN}/oauth/user/studentnumber", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/oauth/user/studentnumber \
-d client_secret=secret \\
-d token=uclapi-user-abd-def-ghi-jkl`,

  javascript: `fetch("${Constants.DOMAIN}/oauth/user/studentnumber?client_secret=secret&token=uclapi-user-abd-def-ghi-jkl")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
    "ok": true,
    "student_number": "123456789"
}`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const StudentNumber = ({ activeLanguage }) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="oauth/user/studentnumber">Student Number</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/oauth/user/studentnumber</code>
        </p>
        <p>
          You can use the <code>oauth/user/data</code>&nbsp;
          endpoint to find out whether the user is a student
          before you call this endpoint.
          
          If you call this endpoint and the user is not a student,
          an error will be returned.
        </p>
        <p>
          Please note: to use this endpoint you must have ticked the&nbsp;
          <em>Student Number</em> scope for your application in the&nbsp;
          <a href="/dashboard">Dashboard</a>.
          
          This piece of information has been separated from the others
          because a student number can in some cases be considered
          confidential.
          
          This is because any data exported directly from Portico,
          SITS (E:Vision) or CMIS is usually grouped by Student Number.
          
          One example is that in some cases departments choose to release
          spreadsheets of examination results where each student is identified
          by their student number, and not their name, to provide a degree of
          anonymity in what is otherwise an open data set.
          
          You should consider carefully whether you actually need
          a student number to track students when other unique
          identifiers are available, such as their username-based
          email address and UPI.
          
          If you request a student number and it is not required
          for your application, your users may choose not to provide
          this information to you, and therefore deny your application
          permission to access their details.
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
          name="student_number"
          extra="string"
          example="123456789"
          description="The user's student number. This may be prefixed with a 0 so should be treated as a string, even though it is made up only of digits. The maximum possible length is 12 digits."
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
          <Cell
            name="User is not a student."
            description="The user is not a student, and therefore has no student number that can be returned."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default StudentNumber