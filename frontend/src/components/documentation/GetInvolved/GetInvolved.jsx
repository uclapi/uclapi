import React from 'react';

import Topic from './../Topic.jsx';


export default class Welcome extends React.Component {

    render () {
      return (
        <Topic
          noExamples={true}>
          <h1 id="getInvolved">Get Involved</h1>
          <p>
            The full API including front-end, documentation and the back-end is all open sourced at <a href="https://github.com/uclapi/uclapi">https://github.com/uclapi/uclapi</a>.
          </p>
          <p>
            Any and all contributions are welcome! If you spot a typo or error, feel free to fix it and submit a pull request :)
          </p>
        </Topic>
      )
    }

}
