import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'

const codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
}
r = requests.get("https://uclapi.com/roombookings/rooms", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/roombookings/rooms \\
-d token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `fetch("https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
  "ok": true,
  "rooms": [
    {
      "roomname": "Wilkins Building (Main Building) Portico",
      "roomid": "Z4",
      "siteid": "005",
      "sitename": "Main Building",
      "capacity": 50,
      "classification": "SS",
      "classification_name": "Social Space",
      "automated": "N",
      "location": {
        "coordinates": {
          "lat": "51.524699",
          "lng": "-0.13366"
        },
        "address": [
          "Gower Street",
          "London",
          "WC1E 6BT",
          ""
        ]
      }
    }
    ...
  ]
}
`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const GetRooms = ({ activeLanguage }) => {
  return (
    <div>
      <Topic
        activeLanguage={activeLanguage}
        codeExamples={codeExamples}
      >
        <h1 id="roombookings/rooms">Get Rooms</h1>
        <p>
          Endpoint: <code>https://uclapi.com/roombookings/rooms</code>
        </p>
        <p>
          This endpoint returns rooms and information about them.
          If you don’t specify any query parameters besides <code>token</code>,
          all rooms will be returned.
          </p>
        <p>
          <i>
            Note: This endpoint only returns publicly bookable rooms.
            Departmentally bookable rooms are not included.
            </i>
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
            name="roomname"
            requirement="optional"
            example="Torrington (1-19) 433"
            description="The name of the room. It often includes the name of the site (building) as well."
          />
          <Cell
            name="roomid"
            requirement="optional"
            example="433"
            description="The room ID (not to be confused with the roomname)."
          />
          <Cell
            name="siteid"
            requirement="optional"
            example="086"
            description="Every room is inside a site (building). All sites have IDs."
          />
          <Cell
            name="sitename"
            requirement="optional"
            example="Torrington Place, 1-19"
            description="Every site (building) has a name. In some cases this is contained in the roomname as well."
          />
          <Cell
            name="classification"
            extra="string"
            example="SS"
            description="The room type ID."
          />
          <Cell
            name="capacity"
            requirement="optional"
            example="55"
            description="Every room has a set capacity of how many people can fit inside it. When supplied, all rooms with the given capacity or greater will be returned."
          />
        </Table>
      </Topic>

      <Topic
        activeLanguage={activeLanguage}
        codeExamples={responseCodeExample}
      >
        <h2>Response</h2>
        <p>
          The room field contains a list of rooms that match your query.
          If no filters are applied, all rooms will be returned.
          </p>
        <Table
          name="Response"
        >
          <Cell
            name="roomname"
            extra="string"
            example="Wilkins Building (Main Building) Portico"
            description="Every site (building) has a name. In some cases this is contained in the roomname as well."
          />
          <Cell
            name="roomid"
            extra="string"
            example="Z4"
            description="The room ID (not to be confused with the roomname)."
          />
          <Cell
            name="siteid"
            extra="string"
            example="086"
            description="Every room is inside a site (building). All sites have IDs."
          />
          <Cell
            name="sitename"
            extra="string"
            example="Main Building"
            description="The name of the site (building)."
          />
          <Cell
            name="capacity"
            extra="int"
            example="50"
            description="The number of people that can fit in the room."
          />
          <Cell
            name="classification"
            extra="string"
            example="SS"
            description="The room type ID."
          />
          <Cell
            name="classification_name"
            extra="string"
            example="Social Space"
            description="A human-readable version of the room type. AN = Anechoic Chamber, CI = Clinic Room, CF = Catering Facilities CFE = Cafe, CL = Cloakroom, CR = Classroom, ER = Equipment Room, IN = Installation, LA = Laboratory, LB = Library, LT = Lecture Theatre, MR = Meeting Room, OF = Office, PC1 = Public Cluster, PC2 = Public Cluster - Tutorial, PC3 = Public Cluster - Students, RC = Reverberation Chamber, SS = Social Space, STU = Studio, TH = Theatre. If the room type is unknown, this value will be set to 'Unknown Room Type'."
          />
          <Cell
            name="automated"
            extra="string"
            example="N"
            description="Whether bookings in this room will be confirmed automatically. A stands for automated, and N for not automated. P represents that the confirmation will be automatic, but only under certain circumstances."
          />
          <Cell
            name="location"
            extra="string"
            example="-"
            description={`
                Contains an object with two keys address, and coordinates. address contains an array of address information, which when combined will make up a complete address.
                Coordinates contains a lat and lng key with the latitude and longitude of the room.`
            }
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
            name="capacity should be an int"
            description="capacity should always be an int."
          />
        </Table>
      </Topic>
    </div>
  )
}

export default GetRooms