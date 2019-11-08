import 'whatwg-fetch'

import update from 'immutability-helper'
import PropTypes from 'prop-types'
import React from 'react'
import Modal from 'react-modal'

import { App } from './app.jsx'
import { AppForm } from './appForm.jsx'

class AppList extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      apps: props.apps,
      showCreate: false,
    }
  }

  addApp = (app) => {
    this.setState((state) => update(state, { apps: { $push: [app] } }))
  }

  updateApp = (id, values) => {
    const appIndex = this.getAppIndex(id)
    if (appIndex !== undefined) {
      Object.keys(values).forEach((key) => {
        this.setState((state) => {
          return update(state, { apps: { [appIndex]: { [key]: { $set: values[key] } } } })
        })
      })
    }
  }

  deleteApp = (appId) => {
    this.setState((state) => {
      const appIndex = this.getAppIndex(appId)
      if (appIndex !== undefined) {
        return update(state, { apps: { $splice: [[appIndex, 1]] } })
      }
    })
  }

  getAppIndex = (appId) => {
    for (const app of this.state.apps) {
      if (app.id === appId) {
        return this.state.apps.indexOf(app)
      }
    }
  }

  clickHandler = (e) => {
    e.preventDefault()
    this.deleteApp(`My Cool App`)
  }

  showForm = () => this.setState({ showCreate: true });

  hideForm = () => this.setState({ showCreate: false });

  render() {
    return <div className="appList pure-u-1">
      <div className="pure-g">
        {this.state.apps.map((app, i) => {
          return <App name={app.name}
            appId={app.id}
            appKey={app.token}
            created={app.created}
            updated={app.updated}
            key={i}
            update={this.updateApp}
            remove={this.deleteApp}
            oauth={app.oauth}
            webhook={app.webhook}
                 />
        })}
      </div>
      <Modal
        isOpen={this.state.showCreate}
        contentLabel="Create app form"
        onRequestClose={this.hideForm}
        className="Modal"
        overlayClassName="Overlay"
      >
        <AppForm add={this.addApp} close={this.hideForm} />
      </Modal>
      <div className="flexCentre">
        <button className="roundButton" onClick={this.showForm}>+</button>
      </div>
    </div>
  }
}

AppList.propTypes = {
  apps: PropTypes.array,
}

export default AppList
