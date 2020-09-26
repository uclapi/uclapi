/* eslint-disable react/jsx-no-bind */
import { styles } from 'Layout/data/dashboard_styles.jsx'
import {
  Button, CardView, Column, ConfirmBox,
  Container, Footer, NavBar, Row, TextView,
} from 'Layout/Items.jsx'
import React from 'react'
import Modal from 'react-modal'
import 'Styles/common/uclapi.scss'
import 'Styles/navbar.scss'
// UI App Component
import App from '../../components/dashboard/App.jsx'
import Api from '../../lib/Api'
import './Dashboard.scss'

class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      data: {
        name: ``,
        cn: ``,
        department: ``,
        intranet_groups: ``,
        apps: [],
      },
      view: `default`,
      toDelete: -1,
    }
  }

  componentDidMount(){
    this.getData()
  }

  render() {
    const { data: { name, cn, apps }, view, toDelete } = this.state

    const actions = {
      regenToken: this.regenToken,
      regenVerificationSecret: this.regenVerificationSecret,
      webhook: {
        saveURL: this.saveWebhookURL,
        saveContact: this.saveWebhookContact,
        saveSiteID: this.saveWebhookSiteID,
        saveRoomID: this.saveWebhookRoomID,
      },
      renameProject: this.renameProject,
      cancelEditTitle: this.cancelEditTitle,
      setScope: this.setScope,
      saveOAuthCallback: this.saveOAuthCallback,
      addNewProject: this.addNewProject,
      deleteProject: this.deleteProject,
      deleteConfirm: this.deleteConfirm,
    }

    return (
      <>
        <NavBar isScroll={false} />

        <Modal
          isOpen={view == `add-project`}
          contentLabel="Create app form"
          onRequestClose={() => this.setState({ view: `default` })}
          className="modal"
          overlayClassName="overlay"
          style={styles.modal}
        >
          <ConfirmBox
            text="Enter the name of your new project"
            success={(value) => { actions.addNewProject(value) }}
            fail={() => { this.setState({ view: `default` }) }}
            shouldCheckValue={false}
          />
        </Modal>

        <Modal
          isOpen={view == `delete-project`}
          contentLabel="Delete app form"
          onRequestClose={() => this.setState({ view: `default` })}
          className="modal"
          overlayClassName="overlay"
          style={styles.modal}
        >
          {toDelete !== -1 ? (
            <ConfirmBox
              text={
                `Enter the name of your project to confirm deletion (${
                  apps[toDelete].name
                })`
              }
              success={() => { actions.deleteProject(toDelete) }}
              fail={() => { this.setState({ view: `default` }) }}
              value={apps[toDelete].name}
              shouldCheckValue
            />
          ) : null}
        </Modal>

        <Container
          height='fit-content'
          styling='splash-parallax'
          style={{ minHeight: `100%` }}
        >
          <Row width='1-1'>
            <Column
              width="2-3"
              alignItems="column"
              style={{ margin: `auto` }}
            >
              <h1>Welcome, {name}</h1>
              <h3>username: {cn}</h3>

              <div className="app-holder" style={styles.appHolder}>
                {apps.length === 0 ? (
                  <CardView width='1-1' type='default' noPadding>
                    <Row noPadding>
                      <Column width='1-1'
                        horizontalAlignment='center'
                        style={{
                          paddingTop: 30,
                          paddingBottom: 20,
                        }}
                      >
                        <TextView
                          text={
                            `You haven't created any apps yet, ` +
                            `click below to get started!`
                          }
                          heading={2}
                          align={`center`}
                          style={styles.noPadding}
                        />
                      </Column>
                    </Row>
                  </CardView>
                ) : apps.map((app, index) => (
                  <App
                    key={app.name}
                    app={app}
                    index={index}
                    actions={actions}
                  />
                ))}
              </div>
            </Column>
          </Row>
          <Row width='1-1'>
            <Button
              type={`default`}
              style={{
                cursor: `pointer`,
                borderRadius: `10px`,
                padding: `20px 25px`,
              }}
              onClick={() => { this.setState({ view: `add-project` }) }}
              centred
            >
              +
            </Button>
        </Row>
        </Container>
        <Footer />
      </>
    )
  }

  getData = async () => {
    const data = await Api.dashboard.getData()
    this.setState({ data })
  }

  addNewProject = async (name) => {
    const newApp = await Api.dashboard.addNewProject(name)
    const { data } = this.state
    this.setState({
      view: `default`,
      data: {
        ...data,
        apps: [...data.apps, newApp],
      },
    })
  }

  deleteConfirm = (index) => this.setState({
    view: `delete-project`,
    toDelete: index,
  })

  deleteProject = async (index) => {
    const { data } = this.state
  
    try {
      await Api.dashboard.deleteProject(data.apps[index].id)

      this.setState({
        toDelete: -1,
        view: `default`,
        data: {
          ...data,
          apps: [
            ...data.apps.slice(0, index),
            ...data.apps.slice(index + 1),
          ],
        },
      })
    } catch (error) {
      window.alert(error.message)
    }
  }

  renameProject = async (index, value) => {
    const { data } = this.state

    try {
      await Api.dashboard.renameProject(data.apps[index].id, value)
      this.updateAppState(index, { name: value })
    } catch (error) {
      window.alert(error.message)
    }
  }

  saveOAuthCallback = async (index, value) => {
    if (value.startsWith(`https://`) || value == ``) {
      const { data } = this.state

      try {
        await Api.dashboard.saveOAuthCallback(data.apps[index].id, value)
        this.updateAppState(index, {
          oauth: {
            ...data.apps[index].oauth,
            callback_url: value,
          },
        })
      } catch (error) {
        window.alert(error.message)
      }
       
    } else {
      window.alert(`Must start with https://`)
    }
  }

  setScope = async (index, scope, value) => {
    const { data } = this.state

    const updatedAppState = ({
      oauth: {
        ...data.apps[index].oauth,
        scopes: [
          ...data.apps[index].oauth.scopes.slice(0, scope),
          {
            ...data.apps[index].oauth.scopes[scope],
            enabled: value,
          },
          ...data.apps[index].oauth.scopes.slice(scope + 1),
        ],
      },
    })
  
    const { oauth: { scopes } } = updatedAppState
    const scopesData = scopes.map(scope => ({
      name: scope.name,
      checked: scope.enabled,
    }))
  
    try {
      await Api.dashboard.setScope(
        data.apps[index].id,
        JSON.stringify(scopesData)
      )

      this.updateAppState(index, updatedAppState)
    } catch (error) {
      window.alert(error.message)
    }
  }

  updateAppState = (index, newAppState) => {
    const { data } = this.state
    return this.setState({
      data: {
        ...data,
        apps: [
          ...data.apps.slice(0, index),
          {
            ...data.apps[index],
            ...newAppState,
          },
          ...data.apps.slice(index + 1),
        ],
      },
    })
  }

  regenToken = async (index) => {
    const { data } = this.state
    const token = await Api.dashboard.regenToken(data.apps[index].id)
    this.updateAppState(index, { token })
  }

  regenVerificationSecret = async (index) => {
    const { data } = this.state
    const secret = await Api.dashboard.regenVerificationSecret(
      data.apps[index].id
    )
    this.updateAppState(index, { webhook: {
      ...data.apps[index].webhook,
      verification_secret: secret,
    }})
  }

  saveWebhookURL = (index, value) => {
    if (value.startsWith(`https://`)
      || value.startsWith(`http://`)
      || value == ``
    ) {
      this.updateWebhookSettings({ url: value }, index)
    } else {
      window.alert(`Must start with https:// or http://`)
    }
  }

  saveWebhookContact = (index, value) => this.updateWebhookSettings(
    { contact: value }, index
  )
  saveWebhookSiteID = (index, value) => this.updateWebhookSettings(
    { siteid: value }, index
  )
  saveWebhookRoomID = (index, value) => this.updateWebhookSettings(
    { roomid: value }, index
  )

  updateWebhookSettings = async (newValues, index) => {
    const { data } = this.state

    const app = data.apps[index]
    const {
      url,
      siteid,
      roomid,
      contact,
    } = {
      ...app.webhook,
      ...newValues,
    }

    try {
      const result = await Api.dashboard.updateWebhookSettings(app.id, {
        url,
        siteid,
        roomid,
        contact,
      })

      this.updateAppState(index, { webhook: result })
    } catch (error) {
      window.alert(error.message)
    }
  }
}

export default Dashboard