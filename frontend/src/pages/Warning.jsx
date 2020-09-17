import Warning from 'Layout/Warning.jsx'
import React from 'react'
import ReactDOM from 'react-dom'

const WarningPage = () => (
  <Warning
    title="Please note you are not fully logged out!"
    content="You have been logged out from UCL API. However, in order to be fully logged out of all UCL services, you need to close your browser completely and re-open it. Thank you! Click here to go back to the front page:"
  />
)

ReactDOM.render(
  <WarningPage />,
  document.querySelector(`.app`)
)
