import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';

// Code Generator 
import * as RequestGenerator from 'Layout/Data/RequestGenerator.jsx';

let params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "image_id": "79",
  "image_format": "base64"
}

let codeExamples = RequestGenerator.getRequest("https://uclapi.com/workspaces/images/map", params);

let response = `{
    "content_type": "image/png",
    "ok": true,
    "data": "iVBORw0KGgoAAAANSUhEUgAAE2AAAAVOCAIAAAA..."
}`

let responseCodeExample = {
    python: response,
    javascript: response,
    shell: response
}

export default class WorkspacesGetImage extends React.Component {
    render() {
        return (
            <div>
                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={codeExamples}>
                    <h1 id="workspaces/images/map">Get a Map's Image</h1>
                    <p>
                        Endpoint: <code>https://uclapi.com/workspaces/images/map</code>
                    </p>
                    <p>
                        This endpoint gets the image specified by the passed in image_id. Image IDs are provided by the <code>/workspaces/surveys</code> endpoint within the array of maps. Each map has an image.
                    </p>

                    <Table
                        name="Query Parameters">
                        <Cell
                            name="token"
                            requirement="required"
                            example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                            description="Authentication token." />
                        <Cell
                            name="image_id"
                            requirement="required"
                            example="46"
                            description="The ID of the image to obtain." />
                        <Cell
                            name="image_format"
                            requirement="optional"
                            example="base64"
                            description="The format of the response. This can either be base64, which returns a JSON object as shown in the example, or raw which will respond with a raw image. In the case of a raw image, the Content-Type header will define the data type, such as image/png." />
                    </Table>
                </Topic>

                <Topic
                    activeLanguage={this.props.activeLanguage}
                    codeExamples={responseCodeExample}>
                    <h2>Response</h2>
                    <p>
                        The response will either be a JSON object if base64 is requested, as described below, or a raw object with the <code>Content-Type</code> header set to the content type.
                    </p>
                    <Table
                        name="Response">
                        <Cell
                            name="content_type"
                            extra="string"
                            example="image/png"
                            description="The MIME content type of the base-64-encoded image within the data element." />
                        <Cell
                            name="data"
                            extra="base64 string"
                            example="iVBORw0KGgoAAAANSUhEUgAAE2AAAAVOCAIAAAA..."
                            description="The base-64-encoded representation of the raw binary image." />
                    </Table>
                </Topic>
            </div>
        )
    }
}
