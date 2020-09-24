import RaisedButton from '@material-ui/core/Button'
import React from 'react'

const LogInLayout = ({ url }) => (
  <div className="log-in-layout">
    <div className="container">
      <h1>Sign in to manage app settings</h1>
      <a href={url}>
        <RaisedButton label="Log in" />
      </a>
    </div>
  </div>
)

export default LogInLayout