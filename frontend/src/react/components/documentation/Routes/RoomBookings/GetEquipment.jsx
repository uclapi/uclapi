import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "roomid": "433"
  "siteid": "086"
}

r = requests.get("https://uclapi.com/roombookings/equipment", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/roombookings/equipment?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&roomid=433&siteid=086`,

  javascript: `fetch("https://uclapi.com/roombookings/equipment?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&roomid=433&siteid=086")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`
}


let response = `{
  "ok": true,
  "equipment": [
    {
      "type": "FF",
      "description": "Managed PC",
      "units": 1
    },
    {
      "type": "FE",
      "description": "Chairs with Tables",
      "units": 1
    },
    ...
  ]
}
`

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
            <h1 id="rooms/get-equipment">Get Equipment</h1>
            <p>
              This endpoint returns any equipment/feature information about a specific room. So, for example whether there is a Whiteboard or a DVD Player in the room. A full example can be seen here.
            </p>
            <p>
              You need to supply a token, roomid, and siteid to get a response.
            </p>

            <Table
              name="Query Pararmeters">
              <Cell
                name="token"
                requirement="required"
                example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
                description="Authentication token" />
              <Cell
                name="roomid"
                requirement="optional"
                example="433"
                description="The room ID (not to be confused with the roomname)." />
              <Cell
                name="siteid"
                requirement="optional"
                example="086"
                description="Every room is inside a site (building). All sites have IDs." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              The equipment field contains a list of equipment items. This list can have a different length depending on the room, and it can also be empty.
            </p>
            <p>
              Each equipment item contains a type, a description, and the number of units.
            </p>
            <Table
              name="Response">
              <Cell
                name="type"
                extra="string"
                example="FE"
                description="The type of equipment. Either Fixed Equipment (FE) or Fixed Feature (FF)." />
              <Cell
                name="description"
                extra="string"
                example="Managed PC"
                description="What the piece of equipment actually is." />
              <Cell
                name="units"
                extra="int"
                example="1"
                description="The number of times this piece of equipment exists in the room." />
            </Table>
          </Topic>
        </div>
      )
    }

}
