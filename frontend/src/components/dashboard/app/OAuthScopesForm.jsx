import update from 'immutability-helper'
import PropTypes from 'prop-types'
import React from 'react'

import defaultHeaders from './defaultHeaders.js'

class OAuthScopesForm extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      scopes: this.props.scopes,
      scopesSaved: false,
    }
  }

  handleScopeChange = (e) => {
    e.persist()
    this.setState((state) => {
      return update(state, { scopes: { [e.target.name]: { enabled: { $set: e.target.checked } } } })
    })
  }

  submitScopes = (e) => {
    e.preventDefault()

    const scopesData = []

    for (const scope of this.state.scopes) {
      scopesData.push({
        'name': scope.name,
        'checked': scope.enabled,
      })
    }

    const json = JSON.stringify(scopesData)

    fetch(`/dashboard/api/updatescopes/`, {
      method: `POST`,
      credentials: `include`,
      headers: defaultHeaders,
      body: `app_id=` + this.props.appId + `&scopes=` + encodeURIComponent(json),
    }).then((res) => {
      if (res.ok) { return res.json() }
      throw new Error(`Unable to save scopes.`)
    }).then((json) => {
      if (!json.success) { throw new Error(json.message) }
      this.setState({ scopesSaved: true })
      setTimeout(() => { this.setState({ scopesSaved: false }) }, 5000)
    }).catch((err) => {
      this.props.setError(err.message)
    })
  }

  render() {
    return (
      <form onSubmit={this.submitScopes} className="pure-for">
        {this.state.scopes.map((scope, index) => {
          return <div key={index}>
            <input
              type="checkbox"
              onChange={this.handleScopeChange}
              defaultChecked={scope.enabled}
              name={index}
              className="scope-checkbox"
            />
            {scope.description}
          </div>
        })}
        <button
          type="submit"
          className="pure-button pure-button-primary pure-input-1 tooltip"
          onMouseEnter={this.setSaveScopes}
          style={{ 'border': `1px solid #ccc`,
'borderRadius': `0px` }}
        >
          <i className="fa fa-save" aria-hidden="true"></i>
          <span>{this.state.scopesSaved ? `Saved!` : `Click to save changes to the requested permissions.`}</span>
        </button>
      </form>

    )
  }

}

OAuthScopesForm.propTypes = {
  scopes: PropTypes.arrayOf(PropTypes.object),
  appId: PropTypes.string,
  setError: PropTypes.func,
}

export default OAuthScopesForm
