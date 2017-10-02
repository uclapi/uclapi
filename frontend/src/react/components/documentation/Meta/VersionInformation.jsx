import React from 'react';

import Topic from './../Topic.jsx';


export default class VersionInformation extends React.Component {

    render () {
      return (
        <Topic
          noExamples={true}>
          <h1 id="version-information">Version Information</h1>
          <p>Each service has a header named uclapi-servicenamehere-version which you can add to your requests, where servicenamehere is the endpoint name for the service you are using. For example, for the Room Bookings service you would set the uclapi-roombookings-version header.</p>

          {/* Add warning here */}

          <p>On the right hand side you’ll see a code sample with the version data added. We are specifying that version 1 of the roombookings service should be used for the request URL https://uclapi.com/roombookings/rooms?token=uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb. You should amend the example accordingly for the service and API version you are using.</p>
        </Topic>
      )
    }

}
