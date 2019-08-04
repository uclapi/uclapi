import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "days": 30,
  "survey_ids": "46,45"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/sensors/averages/time", params);

let response = `{
    {
        "ok": true,
        "surveys": [
            {
                "survey_id": 46,
                "averages": {
                    "00:00:00": {
                        "sensors_absent": 291,
                        "sensors_total": 324,
                        "sensors_occupied": 33
                    },
                    "00:10:00": {
                        "sensors_absent": 288,
                        "sensors_total": 323,
                        "sensors_occupied": 35
                    },
                    ...
                    "23:40:00": {
                        "sensors_absent": 289,
                        "sensors_total": 322,
                        "sensors_occupied": 33
                    },
                    "23:50:00": {
                        "sensors_absent": 282,
                        "sensors_total": 320,
                        "sensors_occupied": 38
                    }
                },
                "name": "UCL Institute of Education Library"
            },
            {
                "survey_id": 45,
                "averages": {
                    "00:00:00": {
                        "sensors_absent": 238,
                        "sensors_total": 300,
                        "sensors_occupied": 62
                    },
                    "00:10:00": {
                        "sensors_absent": 241,
                        "sensors_total": 300,
                        "sensors_occupied": 59
                    },
                    ...
                    "23:40:00": {
                        "sensors_absent": 217,
                        "sensors_total": 300,
                        "sensors_occupied": 83
                    },
                    "23:50:00": {
                        "sensors_absent": 224,
                        "sensors_total": 300,
                        "sensors_occupied": 76
                    }
                },
                "name": "UCL Cruciform Hub"
            }
        ]
    }
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetSensorHistoricalTimeData extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/sensors/averages/time">Get Historical Data by Time</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/sensors/averages/time</code>
                    </p>
                    <p>
                        This endpoint will show for every Survey ID provided the average utilisation of the associated library at ten minute intervals throughout the day. This can be used, for example, in apps and integrations which show users how busy each library is at given times of the day. You can show data based on the last day (e.g. yesterday), the last week or the last month. It is updated by us in the early hours of the morning (around 2am) so that users during the day have the latest data.
                    </p>

                    <Table
                        name="Query Parameters">
                        <Cell
                            name="token"
                            requirement="required"
                            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                            description="Authentication token." />
                        <Cell
                            name="days"
                            requirement="required"
                            example="30"
                            description="An integer number of days (either 1, 7 or 30) from which to deliver average data. The format of the data returned does not change based on this value, but the actual averaged figures do. When days is 1, the API will return the data from the previous complete day; when days is 7 the API will return data from the last week and when it is set to 30 the API will return data from the last 30 days, which is approx. one month." />
                        <Cell
                            name="survey_ids"
                            requirement="optional"
                            example="46,45"
                            description="A comma delimited list of Survey IDs. If this parameter is not supplied, historical data for every survey is returned." />
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
                        This endpoint will return a list with every survey requested, its ID, its name and average data for the period requested for every 10 minute period in a day. The  averages are not ordered, so it is recommended that the data is fed into some other code to transform the data in such as way as to ensure that it is user-friendly. One example might be a graphing library to plot the data throughout the day to produce an average occupancy graph.
                    </p>
                    <p>
                        Please note that the counts below may not perfectly add up. This is because we perform an integer division calculation to get an average based on multiple days' worth of data, so you may encounter off-by-one errors if you check that `sensors_absent` + `sensors_occupied` == `sensors_total`. Please do not be alarmed by this! However, if you do get large, unexplained differences do let us know so that we can look into it.
                    </p>
                    <p>
                        Please note further that there are some rare situations where the data source we use may have historical data missing. Sitautions that can cause this include new libraries being added which do not yet have historical data available, and situations where data has not properly been saved by our data provider. In cases like this, our response to your app will include an empty `averages` object with no times within it. Your code should account for this possibility by checking whether each time period is actually present. If time periods are missing your application should alert the user to data being missing and fail gracefully.
                    </p>

                    <Table
                        name="Response">
                        <Cell
                            name="surveys"
                            extra="list"
                            example={`
                                [
                                    {
                                        "survey_id": 46,
                                        "averages": {
                                            "00:00:00": {
                                                "sensors_absent": 291,
                                                "sensors_total": 324,
                                                "sensors_occupied": 33
                                            },
                                            ...
                                        }
                                    }
                                    ...
                                ]
                            `}
                            description="A list of survey objects, each of which contains metadata and average occupancy data for that library." />

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
                            name="surveys[n][averages]"
                            extra="object"
                            example={`
                                {
                                    "00:00:00": {
                                        "sensors_absent": 291,
                                        "sensors_total": 324,
                                        "sensors_occupied": 33
                                    },
                                    "00:10:00": {
                                        "sensors_absent": 288,
                                        "sensors_total": 323,
                                        "sensors_occupied": 35
                                    },
                                    ...
                                }
                            `}
                            description="An object which contains every ten minute time period in a day. The first time period is 00:00:00, and the last one is 23:50:00. Each time period specifies a total number of sensors, a number of absent sensors (e.g. unoccupied seats) and occupied sensors representing seats that are in use. This object can sometimes be empty if the requested data is not available for some reason. Whilst this is rare, your app should be prepared for this and therefore be able to inform the user that the data they requested is unavailable at this time." />
                        <Cell
                            name="surveys[n][averages][t][sensors_absent]"
                            extra="integer"
                            example="291"
                            description="The average number of free seats at time t." />
                        <Cell
                            name="surveys[n][averages][t][sensors_occupied]"
                            extra="integer"
                            example="324"
                            description="The average number of used seats at time t." />
                        <Cell
                            name="surveys[n][averages][t][sensors_total]"
                            extra="integer"
                            example="324"
                            description="The total number of used seats at time t." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
