import '../lib/ErrorReporting'

import Warning from 'Layout/Warning.jsx'
import React from 'react'


const NotFoundPage = () => (
  <Warning
    title="Error 404"
    content="Oops we cannot seem to find that page! Please click below to go back to the front page:"
  />
)

export default NotFoundPage
