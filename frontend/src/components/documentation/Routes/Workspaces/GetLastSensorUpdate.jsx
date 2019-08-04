import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "survey_id": "46"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/sensors/lastupdated", params);

let response = `{
    "last_updated": "2018-02-16T15:33:01",
    "ok": true,
    "survey_id": 46
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetLastSensorUpdate extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/sensors/lastupdated">Get Last Sensor Update by Survey</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/sensors/lastupdated</code>
                    </p>
                    <p>
                        This endpoint replies with the timestamp of the last time the sensor data was updated for a given survey. This allows integrations that poll the API to save on request time by only requesting the full set of sensor information for a survey once it has been updated.
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
                            description="The ID of the survey/library you want to get the last sensor update timestamp for." />
                    </Table>
                </Topic>

                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={responseCodeExample}>
                    <h2>Response</h2>
                    <p>
                        This endpoint will return a dictionary with the ID of the survey requested and an ISO86010-formatted timestamp with the last time new data was sent from a sensor to the Cad-Capture backend.
                    </p>
                    <Table
                        name="Response">
                        <Cell
                            name="survey_id"
                            extra="integer"
                            example="46"
                            description="The ID of the library/survey that was requested in the query parameter." />
                        <Cell
                            name="last_updated"
                            extra="ISO8601 timestamp"
                            example="2018-02-16T15:33:01"
                            description="The last time that a sensor in the survey requested sent an update to Cad-Capture. If no adjustment for timezone is provided then the time can be assumed to be Europe/London local time." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
