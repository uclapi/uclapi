import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
    "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
    "course": "UMNCOMSMAT05"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/timetable/data/courses/modules", params);

let response = `
{
    "ok": true,
    "modules": {
        "MATH0082": {
            "module_id": "MATH0082",
            "name": "Evolutionary Games and Population Genetics",
            "instances": [
                {
                    "full_module_id": "MATH0082-A7U-T2",
                    "class_size": 20,
                    "delivery": {
                        "fheq_level": 7,
                        "is_undergraduate": true,
                        "student_type": "Campus-based, numeric mark scheme"
                    },
                    "periods": {
                        "teaching_periods": {
                            "term_1": false,
                            "term_2": true,
                            "term_3": false,
                            "term_1_next_year": false,
                            "summer": false
                        },
                        "year_long": false,
                        "lsr": false,
                        "summer_school": {
                            "is_summer_school": false,
                            "sessions": {
                                "session_1": false,
                                "session_2": false
                            }
                        }
                    },
                    "instance_code": "A7U-T2"
                },
                {
                    "full_module_id": "MATH0082-A7P-T2",
                    "class_size": 12,
                    "delivery": {
                        "fheq_level": 7,
                        "is_undergraduate": false,
                        "student_type": "Campus-based, numeric mark scheme"
                    },
                    "periods": {
                        "teaching_periods": {
                            "term_1": false,
                            "term_2": true,
                            "term_3": false,
                            "term_1_next_year": false,
                            "summer": false
                        },
                        "year_long": false,
                        "lsr": false,
                        "summer_school": {
                            "is_summer_school": false,
                            "sessions": {
                                "session_1": false,
                                "session_2": false
                            }
                        }
                    },
                    "instance_code": "A7P-T2"
                }
            ]
        },
        ...
    }
}`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class GetDataCoursesModules extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="timetable/data/courses/modules">Get List of Course Modules</h1>
            <p>
              Endpoint: <code>https://uclapi.com/timetable/data/courses/modules</code>
            </p>
            <p>
              This endpoint returns a list of every module taught on a given course at UCL.
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
            <Cell
                name="course"
                requirement="required"
                example="UMNCOMSMAT05"
                description="The course ID available from /data/courses." />
            <Cell
                name="term_1"
                requirement="optional"
                example="false"
                description="Boolean designating if you would like module instances that are taught in term 1." />
            <Cell
                name="term_2"
                requirement="optional"
                example="true"
                description="Boolean designating if you would like module instances that are taught in term 2." />
            <Cell
                name="term_3"
                requirement="optional"
                example="false"
                description="Boolean designating whether or not you want module instances that are taught in term 3." />
            <Cell
                name="term_1_next_year"
                requirement="optional"
                example="true"
                description="Boolean designating if you would like module instances that are taught in term 1 of the next academic year. This is used by admissions to calculate the end dates for non-standard programmes, and therefore is rare" />
            <Cell
                name="summer"
                requirement="optional"
                example="true"
            description="Boolean designating if you would like module instances that are timetabled in the summer. This can happen in some Postgraduate and Medicine teaching arrangements, but is rare. Note that this is NOT the same as the UCL Summer School." />
            <Cell
                name="year_long"
                requirement="optional"
                example="false"
                description="Boolean designating if you would like module instances where the course is timetabled to last for an entire academic year." />
            <Cell
                name="lsr"
                requirement="optional"
                example="true"
                description="Boolean designating if you would like module instances where the module is timetabled during the Late Summer Resit period. This is used internally by Examinations to timetable Late Summer Assessments (LSAs)." />
            <Cell
                name="is_summer_school"
                requirement="optional"
                example="false"
                description="Boolean designating if you would like module instances where the course is taught as part of the UCL Summer School (true) or standard academic teaching (false)." />
            <Cell
                name="session_1"
                requirement="optional"
                example="true"
                description="Boolean designating if you would like module instances where the module is taught in the first summer school session of this academic year's summer." />
            <Cell
                name="session_2"
                requirement="optional"
                example="false"
                description="Boolean designating if you would like module instances where the module is taught in the second summer school session of this academic year's summer." />
            <Cell
                name="is_undergraduate"
                requirement="optional"
                example="true"
                description="Boolean designating if you would like undergraduate module instances." />
            <Cell
                name="only_available"
                requirement="optional"
                example="false"
                description="Boolean designating if you would only like available module instances (i.e. ones that are not compulsory for the course)." />
            <Cell
                name="only_compulsory"
                requirement="optional"
                example="true"
                description="Boolean designating if you would only like compulsory module instances." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              A list of all modules offered in the requested course at UCL.
            </p>
            <Table
              name="Response">
              <Cell
                name="modules"
                extra="dictionary"
                example={`"modules": { "COMP0066": { ... }, "COMP0148": { ... } }`}
                description="A dictionary of all modules offered in the requested course. The key is the module code and the value is the module's data." />
              <Cell
                name="modules[n][module_id]"
                extra="string"
                example="COMP0066"
                description="The module code. This is provided again to ease parsing of the module data, and is the same as the module's dictionary key." />
              <Cell
                name="modules[n][name]"
                extra="string"
                example="Introductory Programming"
                description="The human readable name for the module." />
              <Cell
                name="modules[n][instances]"
                extra="list of dictionaries"
                example=""
                description="A list of instances of the modules" />
            <Cell
                name="modules[n][instances][i][full_module_id]"
                extra="string"
                example="COMP0066-A6U-T1"
                description="The module code concatenated with the instance data. This instance data is defined by the UCL Academic Model Project, and it is expanded out within this section." />
            <Cell
                name="modules[n][instances][i][instance_code]"
                extra="string"
                example="A6U-T1"
                description="A code that, when combined with a module code, forms the 'full_module_id' field above. This data is used to calculate the delivery and periods information that is also provided via JSON. Concatenating the module_id, a hyphen and the instance_code forms the full_module_id field." />

            <Cell
                name="modules[n][instances][i][class_size]"
                extra="integer"
                example="15"
                description="The maximum number of students in the module permitted in that instance. In this example, fifteen undergraduates are permitted to take this module in their third year, but ninety postgraduates may take the module." />
            <Cell
                name="modules[n][instances][i][delivery]"
                extra="dictionary"
                example={`"fheq_level": 6, "is_undergraduate": true`}
                description="The level the course is taught at, and whether it is an undergraduate (true) or postgraduate (false) course." />
              <Cell
                name="modules[n][instances][i][delivery][fheq_level]"
                extra="integer"
                example="6"
                description="The level that the course is taught at. Level 4 => first year, Level 5 => second year, Level 6 => third year, Level 7 => fourth year or postgraduate" />
              <Cell
                name="modules[n][instances][i][delivery][is_undergraduate]"
                extra="boolean"
                example="true"
                description="Whether the course instance is for undergraduate (true) students or postgraduate (false) students." />
              <Cell
                name="modules[n][instances][i][delivery][student_type]"
                extra="string"
                example="Campus-based, numeric mark scheme"
                description="The type of student and assessment pattern available for that course. There are five options: 'Campus-based, numeric mark scheme', 'Campus-based, non-numeric mark scheme', 'Distance learner, numeric mark scheme', 'Distance learner, non-numeric mark scheme' and 'MBBS Resit'." />
              <Cell
                name="modules[n][instances][i][periods]"
                extra="dictionary"
                example={`"teaching_periods": { ... }, "year_long": false, "lsr": false, "summer_school": { ... }`}
                description="When this course instance is taught." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods]"
                extra="dictionary"
                example={`"term_1": true, "term_2": false, "term_3": false, "term_1_next_year": false, "summer": false`}
                description="Which teaching periods this course instance is taught during." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods][term_1]"
                extra="boolean"
                example="true"
                description="Whether the course is taught during Term 1." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods][term_2]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 2." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods][term_3]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 3." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods][term_1_next_year]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 1 of the following academic year. This is used by admissions to calculate the end dates for non-standard programmes, and therefore is rare." />
              <Cell
                name="modules[n][instances][i][periods][teaching_periods][summer]"
                extra="boolean"
                example="false"
                description="Whether the course timetabled during the summer holidays. This can happen in some Postgraduate and Medicine teaching arrangements, but is rare. Note that this is NOT the same as the UCL Summer School." />
              <Cell
                name="modules[n][instances][i][periods][year_long]"
                extra="boolean"
                example="false"
                description="Whether the course is timetabled to last for an entire academic year." />
              <Cell
                name="modules[n][instances][i][periods][lsr]"
                extra="boolean"
                example="false"
                description="Whether the module is timetabled during the Late Summer Resit period. This is used internally by Examinations to timetable Late Summer Assessments (LSAs)." />
              <Cell
                name="modules[n][instances][i][periods][summer_school]"
                extra="dictionary"
                example={`"is_summer_school": false, "sessions": { ... }`}
                description="Information on whether the course is taught by the UCL Summer School programme and, if so, when." />
              <Cell
                name="modules[n][instances][i][periods][summer_school][is_summer_school]"
                extra="boolean"
                example="false"
                description="Whether the module is taught as part of the UCL Summer School (true) or standard academic teaching (false)." />
              <Cell
                name="modules[n][instances][i][periods][summer_school][sessions][session_1]"
                extra="boolean"
                example="false"
                description="Whether the module is taught in the first summer school session of this academic year's summer. This will be false for all standard academic modules." />
              <Cell
                name="modules[n][instances][i][periods][summer_school][sessions][session_2]"
                extra="boolean"
                example="false"
                description="Whether the module is taught in the second summer school session of this academic year's summer. This will be false for all standard academic modules." />
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
                name="Given parameter is not of corrrect type"
                description="Gets returned when you supply a parameter that is not of the correct type." />
              <Cell
                name="only_available and only_compulsory cannot both be true"
                description="Gets returned when you set both only_available and only_compulsory parameters to be true" />
            </Table>
          </Topic>
        </div>
      )
    }

}
