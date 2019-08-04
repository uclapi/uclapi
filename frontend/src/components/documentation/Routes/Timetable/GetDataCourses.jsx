import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
    "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
    "department": "COMPS_ENG"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/search/people", params);

let response = `
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

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}


export default class GetDataCourses extends React.Component {

    render () {
        return (
            <div>
            <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="timetable/data/courses">Get List of Department Courses</h1>
            <p>
            Endpoint: <code>https://uclapi.com/timetable/data/courses</code>
            </p>
            <p>
            This endpoint returns a list of every course taught by a given department at UCL.
            </p>

            <Table
            name="Query Parameters">
            <Cell
            name="token"
            requirement="required"
            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
            description="Authentication token." />
            <Cell
            name="department"
            requirement="required"
            example="COMPS_ENG"
            description="The department ID available from /data/departments." />
            </Table>
            </Topic>

            <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
            A list of all courses offered by the requested department at UCL.
            </p>
            <Table
            name="Response">
            <Cell
            name="courses"
            extra="list"
            example={`"courses": [ { "course_name": "MRes...", ... }, ... ]`}
            description="A list of courses (represented in dictionaries) that a given department offers." />
            <Cell
            name="courses[n][course_name]"
            extra="string"
            example="MRes Computational Statistics and Machine Learning"
            description="The human readable name for the module." />
            <Cell
            name="courses[n][course_id]"
            extra="string"
            example="TMRCOMSSML01"
            description="The module code." />
            <Cell
            name="courses[n][years]"
            extra="int"
            example="1"
            description="Length of the course given in years" />
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
            <Cell
            name="No department ID provided"
            description="Returned when you have not supplied a department ID in your request." />
            </Table>
            </Topic>
            </div>
        )
    }

}
