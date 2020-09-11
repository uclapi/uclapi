import React from 'react'
import Topic from './../Topic'

const Welcome = () => {
  return (
    <Topic noExamples>
      <h1 id="get-involved">Get Involved</h1>
      <p>
        The full API including front-end, documentation and
        the back-end is all open sourced at&nbsp;
        <a href="https://github.com/uclapi/uclapi">
          github.com/uclapi/uclapi
        </a>.
      </p>
      <p>
        Any and all contributions are welcome!
        If you spot a typo or error, feel free to fix it
        and submit a pull request 😃
      </p>
    </Topic>
  )
}

export default Welcome
