import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/surveys", params);

let response = `{
    "ok": true,
    "surveys": [
        {
            "id": 46,
            "name": "UCL Institute of Education Library",
            "active": 1,
            "start_time": "09:00",
            "end_time": "17:00",
            "staff_survey": 0,
            "location": {
                "coordinates": {
                    "lat": "51.522897",
                    "lng": "-0.127864"
                },
                "address": [
                    "Newsam Library and Archives",
                    "20 Bedford Way",
                    "London",
                    "WC1H  0AL"
                ]
            },
            "maps": [
                {
                    "id": 114,
                    "name": "Level 4",
                    "image_id": 123
                },
                {
                    "id": 115,
                    "name": "Level 3",
                    "image_id": 126
                },
                {
                    "id": 116,
                    "name": "Level 5",
                    "image_id": 127
                }
            ]
        },
        ...
    ]
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetSurveys extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/surveys">Get Surveys</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/surveys</code>
                    </p>
                    <p>
                        This endpoint returns all UCL libraries with the Cad-Capture devices fitted to the seats. Each library is known as a 'survey', as it is a survey of the building. Within each survey there are multiple 'maps', each of which corresponds to a section such as a level, wing or separated library work area. Each sensor is tied to a specific map, and each map belongs to a survey.
                    </p>

                    <Table
                        name="Query Parameters">
                        <Cell
                            name="token"
                            requirement="required"
                            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                            description="Authentication token." />
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
                        The surveys key contains a list of dictionaries, each of which corresponds to a library survey with seating sensors attached. Each survey has a number of maps, corresponding to the regions within the library, such as a different floor or wing.
                    </p>
                    <p>
                        Note that the <code>location[address]</code> field will not always contain a precise address, and may simply contain the address to the UCL campus (i.e. Gower Street, London), which may not be helpful. If it is present, the <code>location[coordinates]</code> will generally be more precise.
                    </p>
                    <Table
                        name="Response">
                        <Cell
                            name="id"
                            extra="integer"
                            example="46"
                            description="The library survey's ID. This is used later to identify individual libraries." />
                        <Cell
                            name="name"
                            extra="string"
                            example="UCL Institute of Education Library"
                            description="The human-readable name of the library." />
                        <Cell
                            name="active"
                            extra="boolean"
                            example="true"
                            description="Whether the survey is active and working." />
                        <Cell
                            name="start_time"
                            extra="string"
                            example="09:00"
                            description="Standard UCL opening time supplied by the backend. This field should NOT be trusted as information on when a particular library is open. This is usually set to 09:00." />
                        <Cell
                            name="end_time"
                            extra="string"
                            example="17:00"
                            description="Standard UCL closing time supplied by the backend. This field should NOT be trusted as information on when a particular library closes. This is usually set to 17:00." />
                        <Cell
                            name="staff_survey"
                            extra="boolean"
                            example="false"
                            description="Whether the survey represents a staff workspace (`true`) or a student work or study space (`false`). This is useful in apps where you set the `survey_filter` parameter to `all` and wish to do filtering of student and staff workspaces in your app or API as opposed to leaving the filtering to UCL API. By default, as `survey_filter` is set to `student` unless you specify otherwise, all workspaces will have this parameter set to `false`." />
                        <Cell
                            name="location"
                            extra="object"
                            example='{"coordinates": {"lat": "51.522897","lng": "-0.127864"},"address": ["Newsam Library and Archives","20 Bedford Way","London","WC1H  0AL"]'
                            description="Object containing survey location information including co-ordinates and the address." />
                        <Cell
                            name='location[coordinates]'
                            extra="object"
                            example='{"lat": "51.522897","lng": "-0.127864"}'
                            description="Object containing a latitude and longitude." />
                        <Cell
                            name='location[coordinates][lat]'
                            extra="string"
                            example='"51.522897"'
                            description="Latitude of the survey location." />
                        <Cell
                            name='location[coordinates][lng]'
                            extra="string"
                            example='"-0.127864"'
                            description="Longitude of the survey location." />
                        <Cell
                            name='location[address]'
                            extra="list"
                            example='["Newsam Library and Archives","20 Bedford Way","London","WC1H  0AL"]'
                            description="List containing address lines for the survey location." />
                        <Cell
                            name='location[address][n]'
                            extra="string"
                            example='"20 Bedford Way"'
                            description="One line of an address for a survey location." />
                        <Cell
                            name="maps"
                            extra="list"
                            example={`[{"image_id": 79, "name": "Level 3", "id": 73}, ...]`}
                            description="List of maps corresponding to regions within the library's survey." />
                        <Cell
                            name="maps[n][name]"
                            extra="string"
                            example="Level 3"
                            description="The name of the mapped section of the library's survey, such as a level, room or wing." />
                        <Cell
                            name="maps[n][image_id]"
                            extra="integer"
                            example="79"
                            description="The ID of the map's image. This can be used to download a CAD drawing of the map." />
                        <Cell
                            name="maps[n][id]"
                            extra="integer"
                            example="73"
                            description="The map's ID." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
