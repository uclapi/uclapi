import React from 'react';

import Topic from './Topic.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb"
}
r = requests.get("https://uclapi.com/roombookings/rooms", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb`,

  javascript: `etch("https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}

export default class DocumentationComponent extends React.Component {

    render () {
      return (
        <Topic codeExamples={codeExamples}>
          <h1>Get Rooms</h1>
          <p>
            This endpoint returns rooms and information about them.
            If you don’t specify any query parameters besides the token, all rooms will be returned.
            Note: This endpoint only returns publicly bookable rooms.
            Departmentally bookable rooms are not included.
          </p>
        </Topic>
      )
    }

}
