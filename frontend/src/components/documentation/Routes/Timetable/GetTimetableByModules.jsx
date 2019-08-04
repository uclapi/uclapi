import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "modules": "COMP0030,COMP0133-A7U-T1"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/timetable/bymodule", params);

let response = `{
    "timetable": {
      "2018-10-02": [
        {
            "start_time": "10:00",
            "end_time": "11:00",
            "duration": 60,
            "module": {
                "module_id": "COMP0030",
                "department_id": "COMPS_ENG",
                "department_name": "Computer Science",
                "name": "Research Methods",
                "lecturer": {
                    "name": "HUNTER, Anthony (Prof)",
                    "email": "ucachun@ucl.ac.uk",
                    "department_id": "COMPS_ENG",
                    "department_name": "Computer Science"
                }
            },
            "location": {
                "name": "Roberts Building 421",
                "capacity": 94,
                "type": "CB",
                "address": [
                    "Torrington Place",
                    "London",
                    "WC1E 7JE",
                    ""
                ],
                "site_name": "Roberts Building",
                "coordinates": {
                    "lat": null,
                    "lng": null
                }
            },
            "session_title": "Research Methods",
            "session_type": "L",
            "session_type_str": "Lecture",
            "contact": "Unknown",
            "instance": {
                "delivery": {
                    "fheq_level": 6,
                    "is_undergraduate": true
                },
                "periods": {
                    "teaching_periods": {
                        "term_1": true,
                        "term_2": false,
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
                "instance_code": "A6U-T1"
            }
        }
      ],
      ...
    },
    "ok": true
}`

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
            <h1 id="timetable/bymodule">Get Timetable By Modules</h1>
            <p>
              Endpoint: <code>https://uclapi.com/timetable/bymodule</code>
            </p>
            <p>
              This endpoint returns a yearly timetable for the supplied modules.
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token." />
              <Cell
                name="modules"
                requirement="required"
                example="COMP0030,COMP0133-A7U-T1"
                description="A comma-separated list of the module codes you want the timetable of. You can supply either standard module codes (e.g. COMP0133), or full codes including the instance of the module (COMP0133-A7U-T1). Note that if you do not supply an instance, every single timetable entry will be returned including duplicates for the same module taught as multiple instances. It is recommended that a full module code including instance be supplied." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              This endpoint will create a timetable for the module ids provided and return the yearly calendar.
            </p>
            <p>
              The <code>timetable</code> field contains an object where dates are mapped to event objects.
            </p>
            <Table
              name="Response">
              <Cell
                name="location"
                extra="object"
                example="JSON Object"
                description="Location of details of the timetable event." />
              <Cell
                name="address"
                extra="array"
                example={`["29 Gordon Sq", "London", "WC1H 0PP"]`}
                description="Address represented as an array." />
              <Cell
                name="name"
                extra="string"
                example="Gordon House 106"
                description="Room name of the timetable event." />
              <Cell
                name="site_name"
                extra="string"
                example="Gordon House"
                description="Name of the site / building where the event is happening." />
              <Cell
                name="type"
                extra="string"
                example="CB"
                description="Type of the room eg., Centrally Bookable (CB) or Departmentally Bookable (DB)." />
              <Cell
                name="capacity"
                extra="int"
                example="100"
                description="Capacity of the room (e.g. how many seats are in a lecture theatre, or how many can be sat at tables in a flat space)." />
              <Cell
                name="module"
                extra="object"
                example={`{"module_id": "COMP3011", name": "Functional Programming", "department_id": "COMPS_ENG", "department_name": "Computer Science", "lecturer": {"name": "CLACK, Chris (Dr)", "department_id": "COMPS_ENG", "department_name": "Computer Science", "email": "REDACTED@ucl.ac.uk"}}`}
                description="Information about the module as a whole, including its lead lecturer"/>
              <Cell
                name="module_id"
                extra="string"
                example="COMP3011"
                description="Module ID." />
              <Cell
                name="name"
                extra="string"
                example="Functional Programming"
                description="Module name." />
              <Cell
                name="department_id"
                extra="string"
                example="COMPS_ENG"
                description="Department the module comes under." />
              <Cell
                name="department_name"
                extra="string"
                example="Computer Science"
                description="Human readable department name that owns the module." />
              <Cell
                name="lecturer"
                extra="object"
                example={`"lecturer": {"name": "CLACK, Chris (Dr)", "department_id": "COMPS_ENG", "department_name": "Computer Science", "email": "REDACTED@ucl.ac.uk"}`}
                description="Information about the main course leader / lecturer, and what their home department is. Note that the course lead may not run every lecture, so in timetable apps you should use the contact field listed below." />
              <Cell
                name="duration"
                extra="int"
                example="120"
                description="Duration of the event in minutes." />
              <Cell
                name="start_time"
                extra="string"
                example="16:00:00"
                description="Start time of the event." />
              <Cell
                name="end_time"
                extra="string"
                example="18:00:00"
                description="End time of the event." />
              <Cell
                name="session_type"
                extra="string"
                example="L"
                description="ID of the type of session, e.g. L = Lecture, PBL = Problem Based Learning. These come from UCL's internal database, and are provided in case a new session type that we are not aware of is in the timetable. See session_type_str below." />
              <Cell
                name="session_type_str"
                extra="string"
                example="Lecture"
                description="Type of event such as Lecture, Problem Based Learning, Practical, etc. If the session_type has not been recognised by us then this will have the value Unknown." />
              <Cell
                name="session_group"
                extra="string"
                example="LAB A"
                description="Used for lab groups, or other types of small group activity that does not involve the whole cohort. When the whole cohort is invited (e.g. lectures) this value is a blank string." />
              <Cell
                name="contact"
                extra="string"
                example="Prof Robin Hirsch"
                description="The name associated with the individual room booking. This is the most likely candidate for the person taking the session or lecture. This name is also the most human-readable. Apps should display this value as the lecturer for any given booking, and only use the lecturer information given in the module{lecturer{}} dictionary to reference the course lead or owner." />
              <Cell
                name="instance"
                extra="dictionary"
                example={`"instance": "delivery": {...}, "periods": {...}, "instance_code": "A6U-T1"`}
                description="The Academic Model Project (AMP) instance data for the module. This contains information on when the module is taught and in which way." />
              <Cell
                name="instance[delivery]"
                extra="dictionary"
                example={`"fheq_level": 6, "is_undergraduate": true`}
                description="The level the course is taught at, and whether it is an undergraduate (true) or postgraduate (false) course." />
              <Cell
                name="instance[delivery][fheq_level]"
                extra="integer"
                example="6"
                description="The level that the course is taught at. Level 4 => first year, Level 5 => second year, Level 6 => third year, Level 7 => fourth year or postgraduate" />
              <Cell
                name="instance[delivery][is_undergraduate]"
                extra="boolean"
                example="true"
                description="Whether the course instance is for undergraduate (true) students or postgraduate (false) students." />
              <Cell
                name="instance[periods]"
                extra="dictionary"
                example={`"teaching_periods": { ... }, "year_long": false, "lsr": false, "summer_school": { ... }`}
                description="When this course instance is taught." />
              <Cell
                name="instance[periods][teaching_periods]"
                extra="dictionary"
                example={`"term_1": true, "term_2": false, "term_3": false, "term_1_next_year": false, "summer": false`}
                description="Which teaching periods this course instance is taught during." />
              <Cell
                name="instance[periods][teaching_periods][term_1]"
                extra="boolean"
                example="true"
                description="Whether the course is taught during Term 1." />
              <Cell
                name="instance[periods][teaching_periods][term_2]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 2." />
              <Cell
                name="instance[periods][teaching_periods][term_3]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 3." />
              <Cell
                name="instance[periods][teaching_periods][term_1_next_year]"
                extra="boolean"
                example="false"
                description="Whether the course is taught during Term 1 of the following academic year. This is used by admissions to calculate the end dates for non-standard programmes, and therefore is rare." />
              <Cell
                name="instance[periods][teaching_periods][summer]"
                extra="boolean"
                example="false"
                description="Whether the course timetabled during the summer holidays. This can happen in some Postgraduate and Medicine teaching arrangements, but is rare. Note that this is NOT the same as the UCL Summer School." />
              <Cell
                name="instance[periods][year_long]"
                extra="boolean"
                example="false"
                description="Whether the course is timetabled to last for an entire academic year." />
              <Cell
                name="instance[periods][lsr]"
                extra="boolean"
                example="false"
                description="Whether the module is timetabled during the Late Summer Resit period. This is used internally by Examinations to timetable Late Summer Assessments (LSAs)." />
              <Cell
                name="instance[periods][summer_school]"
                extra="dictionary"
                example={`"is_summer_school": false, "sessions": { ... }`}
                description="Information on whether the course is taught by the UCL Summer School programme and, if so, when." />
              <Cell
                name="instance[periods][summer_school][is_summer_school]"
                extra="boolean"
                example="false"
                description="Whether the module is taught as part of the UCL Summer School (true) or standard academic teaching (false)." />
              <Cell
                name="instance[periods][summer_school][sessions][session_1]"
                extra="boolean"
                example="false"
                description="Whether the module is taught in the first summer school session of this academic year's summer. This will be false for all standard academic modules." />
              <Cell
                name="instance[periods][summer_school][sessions][session_2]"
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
                name="OAuth token does not exist"
                description="Gets returned when you supply an invalid token." />
              <Cell
                name="No module ids provided."
                description="No module ids provided in post request." />
            </Table>
          </Topic>
        </div>
      )
    }

}
