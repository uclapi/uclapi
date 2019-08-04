import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/timetable/data/departments", params);

let response = `{
    {
        "ok": true,
        "departments": [
            {
                "department_id": "COMPS_ENG",
                "name": "Computer Science"
            },
            {
                "department_id": "SPACE_MAP",
                "name": "Space and Climate Physics"
            },
            ...
        ]
    }
}`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetDataDepartments extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="timetable/data/departments">Get List of Departments</h1>
            <p>
              Endpoint: <code>https://uclapi.com/timetable/data/departments</code>
            </p>
            <p>
              This endpoint returns a list of every department at UCL, along with its internal name. This can be used with the /data/modules endpoint to request information on all modules for a department.
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              A list of all departments at UCL.
            </p>
            <Table
              name="Response">
              <Cell
                name="departments"
                extra="list of dictionaries"
                example={`"departments": [ ... ]`}
                description="A list of department objects" />
              <Cell
                name="departments[n][department_id]"
                extra="string"
                example="COMPS_ENG"
                description="The internal ID for the department that can be used when querying information on a department, such as the modules offered by it." />
              <Cell
                name="departments[n][name]"
                extra="string"
                example="Computer Science"
                description="The human readable name for the department." />
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
                name="OAuth token does not exist."
                description="Gets returned when you supply an invalid token." />
            </Table>
          </Topic>
        </div>
      )
    }

}
