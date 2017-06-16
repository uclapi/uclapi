import React from 'react';

import Topic from './../Topic.jsx';


let codeExamples = {
  python: `import requests

params = {
  "token": "uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb",
  "contact": "Mark"
}
r = requests.get("https://uclapi.com/roombookings/bookings", params=params)
print(r.json())`,

  shell: `curl https://uclapi.com/roombookings/bookings?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&contact=Mark`,

  javascript: `fetch("https://uclapi.com/roombookings/bookings?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb&contact=Mark")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})
`
}

export default class GetBookings extends React.Component {

    render () {
      return (
        <Topic codeExamples={codeExamples}>
          <h1>Get Bookings</h1>
          <p>
            This endpoint shows the results to a bookings or space availability query.
            It returns a paginated list of bookings.
            Note: This endpoint only returns publicly displayed bookings.
            Departmental bookings are not included.
          </p>
        </Topic>
      )
    }

}
