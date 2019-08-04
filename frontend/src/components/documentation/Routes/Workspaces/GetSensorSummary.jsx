import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "survey_ids": "46,45"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/sensors/summary", params);

let response = `{
    "surveys": [
        {
            "name": "UCL Cruciform Hub",
            "maps": [
                {
                    "name": "Open Area",
                    "sensors_absent": 47,
                    "sensors_other": 0,
                    "sensors_occupied": 64,
                    "id": "72"
                },
                {
                    "name": "Cluster Areas",
                    "sensors_absent": 76,
                    "sensors_other": 1,
                    "sensors_occupied": 62,
                    "id": "70"
                },
                {
                    "name": "Teaching Rooms",
                    "sensors_absent": 39,
                    "sensors_other": 0,
                    "sensors_occupied": 19,
                    "id": "71"
                }
            ],
            "id": 45,
            "sensors_absent": 219,
            "sensors_occupied": 104,
            "sensors_other": 0
        },
        {
            "name": "UCL Institute of Education Library",
            "maps": [
                {
                    "name": "Level 3",
                    "sensors_absent": 72,
                    "sensors_other": 0,
                    "sensors_occupied": 85,
                    "id": "73"
                },
                {
                    "name": "Level 4",
                    "sensors_absent": 41,
                    "sensors_other": 0,
                    "sensors_occupied": 55,
                    "id": "74"
                },
                {
                    "name": "Level 5",
                    "sensors_absent": 29,
                    "sensors_other": 0,
                    "sensors_occupied": 42,
                    "id": "75"
                }
            ],
            "id": 46,
            "sensors_absent": 147,
            "sensors_occupied": 177,
            "sensors_other": 2
        }
    ],
    "ok": true
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetSensorsSummary extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/sensors/summary">Get Survey Sensors Summary</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/sensors/summary</code>
                    </p>
                    <p>
                        This endpoint summarises, with a one-minute accuracy, the number of seats within each library region that are free and occupied. It is best suited to integrations which show cumulative, live data. Developers can use this endpoint to avoid making many parallel or sequential requests to fetch survey sensor counts.
                    </p>
                    <p>
                        This endpoint takes into account UCL's <a href="https://www.ucl.ac.uk/library/sites/seats/study-space-availability-faqs">thirty minute rule</a>, which allows students to leave their seat unattended for up to thirty minutes at a time (e.g. to use the bathroom or get food). This means that the Summary endpoint may return a lower number of available seats when compared to reality if many students leave the library within a short period of time. The UCL Library's website and the UCL Go! mobile application both follow this rule, so your app or integration should have parity with first party data sources by using the UCL API.
                    </p>

                    <Table
                        name="Query Parameters">
                        <Cell
                            name="token"
                            requirement="required"
                            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                            description="Authentication token." />
                        <Cell
                            name="survey_ids"
                            requirement="optional"
                            example="46,45"
                            description="A comma delimited list of Survey IDs. If this parameter is not supplied, summary data for every survey is returned." />
                        <Cell
                            name="survey_filter"
                            requirement="optional"
                            example="student"
                            description="Filter the surveys based on who they are designed for. Valid values of this parameter are `all` (no filtering), `student` (return only student surveys; this is the default) and `staff` (return only surveys representing work areas for UCL staff only). It is recommended that the default (student) is used in apps aimed at students, unless a specific reason to include a staff workspace is required." />
                    </Table>
                </Topic>

                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={responseCodeExample}>
                    <h2>Response</h2>
                    <p>
                        This endpoint will return a list with every survey requested, and its associated maps. Within each map is a count of absent (e.g. free) and occupied seats. The endpoint also returns the total number of seats in each library that are absent or occupied.
                    </p>
                    <p>
                        If your application or integration is designed to inform students of the total number of free seats in a library please ensure you use the survey total figures. This is because many sensors have not yet been assigned to maps on our data provider's system which means that relying only on map counts will leave many seats unaccounted for. We are actively working with our data provider to rectify this, and we apologise for any inconvenience caused.
                    </p>
                    <Table
                        name="Response">
                        <Cell
                            name="surveys"
                            extra="list"
                            example={`
                                [
                                    {
                                        "name": "UCL Cruciform Hub",
                                        "id": 45,
                                        "maps": [
                                            {
                                                "name": "Open Area",
                                                "id": "72",
                                                "sensors_absent": 47,
                                                "sensors_other": 0,
                                                "sensors_occupied": 64
                                            },
                                            ...
                                        ],
                                        "sensors_absent": 219,
                                        "sensors_occupied": 104,
                                        "sensors_other": 0
                                    },
                                    ...
                                ]
                            `}
                            description="A list of survey objects, each of which contains a list of maps with associated sensor counts, as well as library sensor totals." />

                        <Cell
                            name="surveys[n][name]"
                            extra="string"
                            example="UCL Cruciform Hub"
                            description="The name of the survey (library)." />
                        <Cell
                            name="surveys[n][id]"
                            extra="integer"
                            example="72"
                            description="The survey's ID." />
                        <Cell
                            name="surveys[n][sensors_absent]"
                            extra="integer"
                            example="219"
                            description="Number of free seats in the whole library, including all rooms and floors." />
                        <Cell
                            name="surveys[n][sensors_occupied]"
                            extra="integer"
                            example="104"
                            description="Number of taken / occupied seats in the whole library, including all rooms and floors." />
                        <Cell
                            name="surveys[n][sensors_other]"
                            extra="integer"
                            example="0"
                            description="Number of library seats with an unknown status. This is usually zero." />
                        <Cell
                            name="surveys[n][maps]"
                            extra="list"
                            example={`
                                [
                                    {
                                        "name": "Open Area",
                                        "id": "72",
                                        "sensors_absent": 47,
                                        "sensors_other": 0,
                                        "sensors_occupied": 64
                                    },
                                    ...
                                ]
                            `}
                            description="A list of objects representing maps (regions), each of which has a sensor summary." />
                        <Cell
                            name="surveys[n][maps][n][name]"
                            extra="string"
                            example="Open Area"
                            description="Name of the library region (map)." />
                        <Cell
                            name="surveys[n][maps][n][id]"
                            extra="integer"
                            example="72"
                            description="ID of the library region (map)." />
                        <Cell
                            name="surveys[n][maps][n][sensors_absent]"
                            extra="integer"
                            example="47"
                            description="Number of free seats in that section of the library." />
                        <Cell
                            name="surveys[n][maps][n][sensors_occupied]"
                            extra="integer"
                            example="64"
                            description="Number of taken / occupied seats in that section of the library." />
                        <Cell
                            name="surveys[n][maps][n][sensors_other]"
                            extra="integer"
                            example="0"
                            description="Number of seats with an unknown status. This is usually zero." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
