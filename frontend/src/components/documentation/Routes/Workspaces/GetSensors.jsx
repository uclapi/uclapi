import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "survey_id": "46",
  "return_states": "true"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/sensors", params);

let response = `{
    "survey_id": "46",
    "maps": [
        {
            "sensors": {
                "584001": {
                    "description_2": "",
                    "floor": "False",
                    "y_pos": "14893.0",
                    "description_3": "",
                    "device_type": "Desk",
                    "host_address": "584",
                    "building_name": "IOE (20 B-Way)",
                    "room_description": "",
                    "last_trigger_type": "Occupied",
                    "survey_id": "46",
                    "room_type": "Open Plan",
                    "room_name": "324",
                    "room_id": "291",
                    "location": "",
                    "survey_device_id": "8420",
                    "share_id": "None",
                    "x_pos": "32432.0",
                    "description_1": "",
                    "hardware_id": "584001",
                    "pir_address": "1",
                    "last_trigger_timestamp": "2018-02-15T22:42:28+00:00",
                    "occupied": true
                },
                ...
            },
            "name": "Level 3",
            "id": "73",
            "image_id": "79"
        },
        ...
    ]
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetSensors extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/sensors">Get Sensors by Survey</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/sensors</code>
                    </p>
                    <p>
                        This endpoint provides a list of every sensor within every map in a survey/library. It can optionally provide the current state of a sensor (e.g. Occupied / Absent), but by default it will only list the sensors without their states.
                    </p>

                    <Table
                        name="Query Parameters">
                        <Cell
                            name="token"
                            requirement="required"
                            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                            description="Authentication token." />
                        <Cell
                            name="survey_id"
                            requirement="required"
                            example="46"
                            description="The ID of the survey/library you want to get sensor data for." />
                        <Cell
                            name="return_states"
                            requirement="optional"
                            example="true"
                            description="Whether or not to return the latest trigger state of each sensor. Defaults to false. For live data, set this to true." />
                    </Table>
                </Topic>

                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={responseCodeExample}>
                    <h2>Response</h2>
                    <p>
                        This endpoint will return a list of every map within a survey, and within it every sensor associated with that map. It will optionally also return the latest triggered state of that sensor (e.g. whether the seat was marked triggered or occupied).
                    </p>
                    <p>
                        Note that the following response data table is deliberately incomplete. This is because we return additional metadata that is not yet useful, and often left blank by the provider. We will update this documentation if and when these extra parameters become useful.
                    </p>
                    <Table
                        name="Response">
                        <Cell
                            name="survey_id"
                            extra="integer"
                            example="46"
                            description="The ID of the library/survey that was requested in the query parameter." />
                        <Cell
                            name="maps"
                            extra="list"
                            example={`[{"sensors": [ "585001": { sensor_data_here }, ... ], "name": "Level 3", "id": 73, "image_id": 79}, ... ]`}
                            description="A list of every map within the survey, within which there is information on that map and every sensor it has in a list of dictionaries." />
                        <Cell
                            name="maps[n][id]"
                            extra="integer"
                            example="73"
                            description="The map's unique ID" />
                        <Cell
                            name="maps[n][name]"
                            extra="string"
                            example="Level 3"
                            description="A human-readable name for the section of the library that the map corresponds to" />
                        <Cell
                            name="maps[n][image_id]"
                            extra="integer"
                            example="73"
                            description="The map's image ID to download the CAD drawing" />
                        <Cell
                            name="maps[n][sensors]"
                            extra="object"
                            example={`{"584001": {
                                "description_2": "",
                                "floor": "False",
                                "y_pos": "14893.0",
                                "description_3": "",
                                "device_type": "Desk",
                                "host_address": "584",
                                "building_name": "IOE (20 B-Way)",
                                "room_description": "",
                                "last_trigger_type": "Occupied",
                                "survey_id": "46",
                                "room_type": "Open Plan",
                                "room_name": "324",
                                "room_id": "291",
                                "location": "",
                                "survey_device_id": "8420",
                                "share_id": "None",
                                "x_pos": "32432.0",
                                "description_1": "",
                                "hardware_id": "584001",
                                "pir_address": "1",
                                "last_trigger_timestamp": "2018-02-15T22:42:28+00:00",
                                "occupied": true
                            }, ... }`}
                            description="An object containing dictionaries, each of which corresponds to a sensor. The key is the sensor's unique ID, and the value is a dictionary of data about that sensor." />
                        <Cell
                            name="maps[n][sensors][n][building_name]"
                            extra="string"
                            example=""
                            description="A short but human-readable name of the room that the sensor is in." />
                        <Cell
                            name="maps[n][sensors][n][device_type]"
                            extra="string"
                            example="Desk"
                            description="Type of seat. Usually this is Desk." />
                        <Cell
                            name="maps[n][sensors][n][floor]"
                            extra="string (boolean)"
                            example="False"
                            description="Whether the device is on the floor" />
                        <Cell
                            name="maps[n][sensors][n][last_trigger_timestamp]"
                            extra="ISO8601 timestamp"
                            example="2018-02-15T22:42:28+00:00"
                            description="The last time that this sensor's update value was recorded. NB: only returned when return_states=true." />
                        <Cell
                            name="maps[n][sensors][n][last_trigger_type]"
                            extra="string"
                            example="Occupied"
                            description="The last event the sensor recorded. Possible known values are Absent and Occupied, but this is not guaranteed. NB: only returned when return_states=true." />
                        <Cell
                            name="maps[n][sensors][n][occupied]"
                            extra="boolean"
                            example="true"
                            description="Whether the seat is occupied or not. This takes into account UCL's thirty minute rule, so it's possible that the seat could have been marked as absent a few minutes ago, but this value is still set to true, as UCL allows students to leave their seat unattended for up to thirty minutes at a time (e.g. to use the bathroom or get food). Integrations that provide live seating information to students should use this value so as to have parity with the UCL Library seating policy and the UCL Library website. NB: only returned when return_states=true." />

                        <Cell
                            name="maps[n][sensors][n][hardware_id]"
                            extra="string"
                            example="584001"
                            description="A unique ID for the sensor." />

                        <Cell
                            name="maps[n][sensors][n][x_pos]"
                            extra="string (float)"
                            example="32432.0"
                            description="The X coordinate position of the sensor on the map." />
                        <Cell
                            name="maps[n][sensors][n][y_pos]"
                            extra="string (float)"
                            example="14893.0"
                            description="The Y coordinate position of the sensor on the map." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
