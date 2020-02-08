import RaisedButton from 'material-ui/RaisedButton'
import PropTypes from 'prop-types'
import React from 'react'

class LogInLayout extends React.Component {
  static propTypes = {
    url: PropTypes.string,
  }

  render() {
    const { url } = this.props
    return <div className="log-in-layout">
      <div className="container">
        <h1>Sign in to manage app settings</h1>
        <a href={url}>
          <RaisedButton label="Log in" primary />
        </a>
      </div>
    </div>
  }
}

export default LogInLayout