import 'whatwg-fetch'

import { css,StyleSheet } from 'aphrodite'
import PropTypes from 'prop-types'
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'

import AppNameField from './app/AppNameField.jsx'
import defaultHeaders from './app/defaultHeaders.js'
import DeleteButton from './app/DeleteButton.jsx'
import OAuth from './app/OAuth.jsx'
import Webhook from './app/Webhook.jsx'
import { CopyActionField } from './copyField.jsx'
import RelativeDate from './relativeDate.jsx'

const styles = StyleSheet.create({
  timestamps: {
    margin: `10px 0`,
  },
})

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      error: ``,
    }
  }

  setError = (msg) => {
    this.setState({
      error: msg,
    })
    setTimeout(() => { this.setState({ error: `` }) }, 5000)
  }

  regenToken = () => {
    const that = this
    fetch(`/dashboard/api/regen/`, {
      method: `POST`,
      credentials: `include`,
      headers: defaultHeaders,
      body: `app_id=` + this.props.appId,
    }).then((res) => {
      if (res.ok) { return res.json() }
      throw new Error(`Unable to regen token.`)
    }).then((json) => {
      if (json.success) {
        const values = {
          token: json.app.token,
          updated: json.app.date,
        }
        this.props.update(that.props.appId, values)
        return
      }
      throw new Error(json.message)
    }).catch((err) => {
      this.setError(err.message)
    })
  }

  regenConfirm = (e) => {
    e.preventDefault()
    if (confirm(`Are you sure you want to regenerate your api token?`)) {
      this.regenToken()
    }
  }

  render() {
    return <div className="app pure-u-1 pure-u-xl-1-2">
      <div className="card">
        <div className="pure-g">
          <div className="pure-u-1-2">
            <AppNameField
              origValue={this.props.name}
              update={this.props.update}
              appId={this.props.appId}
              setError={this.setError}
            />
          </div>
          <div className="pure-u-1-2">
            <div style={{ float: `right` }}>
              <DeleteButton
                appId={this.props.appId}
                remove={this.props.remove}
                setError={this.setError}
              />
            </div>
          </div>
        </div>
        <div className="pure-g">
          <div className="pure-u-1">
            API Token
            <CopyActionField
              setError={this.setError}
              val={this.props.appKey}
              action={this.regenConfirm}
              icon="fa fa-refresh"
            />
          </div>
        </div>
        <div className={css(styles.timestamps)}>
          <RelativeDate date={this.props.created} label={`Created: `} />
          <RelativeDate date={this.props.updated} label={`Last Updated: `} />
        </div>
        <Collapse>
          <Panel header="OAuth Settings" showArrow>
            <OAuth
              appId={this.props.appId}
              clientId={this.props.oauth.client_id}
              clientSecret={this.props.oauth.client_secret}
              callbackUrl={this.props.oauth.callback_url}
              scopes={this.props.oauth.scopes}
            />
          </Panel>
          <Panel header="Webhook Settings" showArrow>
            <Webhook
              url={this.props.webhook.url}
              siteid={this.props.webhook.siteid}
              roomid={this.props.webhook.roomid}
              contact={this.props.webhook.contact}
              verification_secret={this.props.webhook.verification_secret}
              appId={this.props.appId}
            />
          </Panel>
        </Collapse>
        <label className="error">{this.state.error}</label>
      </div>
    </div>
  }
}

App.propTypes = {
  name: PropTypes.string,
  appId: PropTypes.string,
  appKey: PropTypes.string,
  created: PropTypes.string,
  updated: PropTypes.string,
  webhook: PropTypes.shape({
    verification_secret: PropTypes.string,
    url: PropTypes.string,
    siteid: PropTypes.string,
    roomid: PropTypes.string,
    contact: PropTypes.string,
  }),
  oauth: PropTypes.shape({
    client_id: PropTypes.string,
    client_secret: PropTypes.string,
    callback_url: PropTypes.string,
    scopes: PropTypes.arrayOf(PropTypes.object),
  }),
  update: PropTypes.func,
  remove: PropTypes.func,
}

export { App }
