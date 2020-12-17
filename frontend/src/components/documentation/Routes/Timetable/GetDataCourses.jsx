import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

  params = {
      "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
      "department": "COMPS_ENG"
  }
  r = requests.get("${Constants.DOMAIN}/timetable/data/courses", params=params)
  print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/timetable/data/courses \\
  -d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
  -d department=COMPS_ENG`,

  javascript: `fetch("${Constants.DOMAIN}/timetable/data/courses?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&department=COMPS_ENG")
  .then((response) => {
      return response.json()
  })
  .then((json) => {
      console.log(json);
  })`,
}

const response = `
{
  "ok": true,
  "courses": [
    {
      "course_name": "MRes Computational Statistics and Machine Learning",
      "course_id": "TMRCOMSSML01",
      "years": 1
    },
    ...
  ]
}`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const GetDataCourses = ({ activeLanguage }) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="timetable/data/courses">Get List of Department Courses</h1>
        <p>
          Endpoint: <code>{Constants.DOMAIN}/timetable/data/courses</code>
        </p>
        <p>
          This endpoint returns a list of every course
          taught by a given department at UCL.
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
            name="department"
            requirement="required"
            example="COMPS_ENG"
            description="The department ID available from /data/departments."
          />
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={responseCodeExample}
      >
        <h2>Response</h2>
        <p>
          A list of all courses offered by the requested department at UCL.
        </p>
        <Table
          name="Response"
        >
          <Cell
            name="courses"
            extra="list"
            example={`"courses": [ { "course_name": "MRes...", ... }, ... ]`}
            description="A list of courses (represented in dictionaries) that a given department offers."
          />
          <Cell
            name="courses[n][course_name]"
            extra="string"
            example="MRes Computational Statistics and Machine Learning"
            description="The human readable name for the module."
          />
          <Cell
            name="courses[n][course_id]"
            extra="string"
            example="TMRCOMSSML01"
            description="The module code."
          />
          <Cell
            name="courses[n][years]"
            extra="int"
            example="1"
            description="Length of the course given in years"
          />
        </Table>
      </Topic>

      <Topic noExamples>
        <Table name="Errors">
          <Cell
            name="No token provided"
            description="Gets returned when you have not supplied a token in your request."
          />
          <Cell
            name="OAuth token does not exist."
            description="Gets returned when you supply an invalid token."
          />
          <Cell
            name="No department ID provided"
            description="Returned when you have not supplied a department ID in your request."
          />
        </Table>
      </Topic>
      </div>
  )
}

export default GetDataCourses