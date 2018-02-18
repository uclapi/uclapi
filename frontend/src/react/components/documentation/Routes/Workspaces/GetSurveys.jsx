import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

let codeExamples = {
    python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
}
r = requests.get("https://uclapi.com/workspaces/surveys", params=params)
print(r.json())`,

  shell: `curl -X GET https://uclapi.com/workspaces/surveys \
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/workspaces/surveys?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}

let response = `{
    "ok": true,
    "surveys": [
        {
            "active": true,
            "maps": [
                {
                    "image_id": 79,
                    "name": "Level 3",
                    "id": 73
                },
                {
                    "image_id": 80,
                    "name": "Level 4",
                    "id": 74
                },
                {
                    "image_id": 81,
                    "name": "Level 5",
                    "id": 75
                }
            ],
            "end_time": "17:00",
            "start_time": "09:00",
            "name": "UCL Institute of Education Library",
            "id": 46
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
                    </Table>
                </Topic>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={responseCodeExample}>
                    <h2>Response</h2>
                    <p>
                        The surveys key contains a list of dictionaries, each of which corresponds to a library survey with seating sensors attached. Each survey has a number of maps, corresponding to the regions within the library, such as a different floor or wing.
                    </p>
                    <Table
                        name="Response">
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
                            name="name"
                            extra="string"
                            example="UCL Institute of Education Library"
                            description="The human-readable name of the library." />
                        <Cell
                            name="id"
                            extra="integer"
                            example="46"
                            description="The library survey's ID. This is used later to identify individual libraries." />
                        <Cell
                            name="maps"
                            extra="list"
                            example={`[{"image_id": 79, "name": "Level 3", "id": 73}, ...]`}
                            description="List of maps corresponding to regions within the library's survey." />
                        <Cell
                            name="maps/name"
                            extra="string"
                            example="Level 3"
                            description="The name of the mapped section of the library's survey, such as a level, room or wing." />
                        <Cell
                            name="maps/image_id"
                            extra="integer"
                            example="79"
                            description="The ID of the map's image. This can be used to download a CAD drawing of the map." />
                        <Cell
                            name="maps/id"
                            extra="integer"
                            example="73"
                            description="The map's ID." />
                    </Table>
                </Topic>
            </div>
        )
    }
}