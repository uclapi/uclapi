import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "roomid": "433"
  "siteid": "086"
}

r = requests.get("${Constants.DOMAIN}/roombookings/equipment", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/roombookings/equipment \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb \\
-d roomid=433 \
-d siteid=086`,

  javascript: `fetch("${Constants.DOMAIN}/roombookings/equipment?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&roomid=433&siteid=086")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`,
}

const response = `{
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

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const GetEquipment = ({ activeLanguage }) => {
  return (
    (
      <div>
        <Topic
          activeLanguage={activeLanguage}
          codeExamples={codeExamples}
        >
          <h1 id="roombookings/equipment">Get Equipment</h1>
          <p>
            Endpoint: <code>{Constants.DOMAIN}/roombookings/equipment</code>
          </p>
          <p>
            This endpoint returns information about the features of and
            equipment present in a specific room. 

            Use this to find out, for instance, whether there is a
            whiteboard, DVD Player, or ramp in the room.
            
            A full example can be seen here.
            </p>
          <p>
            You need to supply a <code>token</code>,
            &nbsp;<code>roomid</code>,
            and <code>siteid</code> to get a response.
          </p>

          <Table
            name="Query Parameters"
          >
            <Cell
              name="token"
              requirement="required"
              example="uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
              description="Authentication token."
            />
            <Cell
              name="roomid"
              requirement="required"
              example="433"
              description="The room ID (not to be confused with the roomname)."
            />
            <Cell
              name="siteid"
              requirement="required"
              example="086"
              description="Every room is inside a site (building). All sites have IDs."
            />
          </Table>
        </Topic>

        <Topic
          activeLanguage={activeLanguage}
          codeExamples={responseCodeExample}
        >
          <h2>Response</h2>
          <p>
            The equipment field contains a list of equipment.
            The length of the list will vary between rooms.
            It may also be empty.
            </p>
          <p>
            Each piece of equipment has a type, a description,
            and a quantity (the number of units).
            </p>
          <Table
            name="Response"
          >
            <Cell
              name="type"
              extra="string"
              example="FE"
              description="The type of equipment. Either Fixed Equipment (FE) or Fixed Feature (FF)."
            />
            <Cell
              name="description"
              extra="string"
              example="Managed PC"
              description="What the piece of equipment actually is."
            />
            <Cell
              name="units"
              extra="int"
              example="1"
              description="The number of times this piece of equipment exists in the room."
            />
          </Table>
        </Topic>

        <Topic
          noExamples
        >
          <Table
            name="Errors"
          >
            <Cell
              name="No token provided"
              description="Gets returned when you have not supplied a token in your request."
            />
            <Cell
              name="Token does not exist"
              description="Gets returned when you supply an invalid token."
            />
            <Cell
              name="No roomid supplied"
              description="Gets returned when you don’t supply a roomid."
            />
            <Cell
              name="No siteid supplied"
              description="Gets returned when you don’t supply a siteid."
            />
          </Table>
        </Topic>
      </div>
    )
  )
}

export default GetEquipment