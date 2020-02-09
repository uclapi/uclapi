// Styling
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Dependencies
import dayjs from 'dayjs'
import Cookies from 'js-cookie'
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'

import { CheckBoxView, Field, OverlayBox } from 'Dashboard/DashboardUI.jsx'
import { styles } from 'Layout/data/dashboard_styles.jsx'

// Components
import { CardView, Column, Footer, NavBar, Row, TextView, ButtonView } from 'Layout/Items.jsx'
import { editIcon, cancelIcon } from 'Layout/Icons.jsx'

const defaultHeaders = {
  'Content-Type': `application/x-www-form-urlencoded`,
  'X-CSRFToken': Cookies.get(`csrftoken`),
}

const Dates = (created, updated, alignment) => (
  <>
    <TextView text={`Created: ` + created + ` ago`}
      heading={5}
      align={alignment} 
      style={styles.dates}
    />
    <TextView text={`Updated: ` + updated + ` ago`}
      heading={5}
      align={alignment}
      style={styles.dates}
    />
  </>
)

const Title = (size, title, created, updated, isEditing, toggleEditTitle, saveEditTitle, cancelEditTitle, deleteApp) => {
  return (
  <Row styling='transparent' noPadding>
    <CardView width={size===`mobile` ? `1-1` : `1-2`} minWidth="140px" type="no-bg" style={styles.squareCard} snapAlign>
      { !isEditing ? (
          <>
            <TextView text={title}
              heading={2}
              align={size===`mobile` ? `center` : `left`} 
              style={styles.titleText}
            />
            {editIcon(toggleEditTitle, {float: `left`})} 
            {cancelIcon(deleteApp, {float: `left`})} 
          </>
        ) : (
          <>
            { Field(`Title: `, title, {
              save: {action: saveEditTitle},
              cancel: {action: cancelEditTitle},
            }, {isSmall: true} ) }
          </>
        )
      }
    </CardView>
    <CardView width={size===`mobile` ? `1-1` : `1-2`} minWidth="140px" type="no-bg" snapAlign style={styles.rowItem}>
      {size===`mobile` ? (
        Dates(created, updated, `center`)
      ) : (
        Dates(created, updated, `right`)
      )}
    </CardView>
  </Row>
  )
}
  
class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

    this.timeSince = this.timeSince.bind(this)
    
    this.toggleEditTitle = this.toggleEditTitle.bind(this)
    this.saveEditTitle = this.saveEditTitle.bind(this)
    this.cancelEditTitle = this.cancelEditTitle.bind(this)

    this.copyToClipBoard = this.copyToClipBoard.bind(this)
    
    this.regenToken = this.regenToken.bind(this)
    this.regenVerificationSecret = this.regenVerificationSecret.bind(this)

    this.saveWebhookURL = this.saveWebhookURL.bind(this)
    this.saveWebhookContact = this.saveWebhookContact.bind(this)
    this.saveWebhookSiteID = this.saveWebhookSiteID.bind(this)
    this.saveWebhookRoomID = this.saveWebhookRoomID.bind(this)

    this.queryDashboardAPI = this.queryDashboardAPI.bind(this)
    this.updateWebhookSettings = this.updateWebhookSettings.bind(this)

    this.saveOAuthCallback = this.saveOAuthCallback.bind(this)

    this.setScope = this.setScope.bind(this)

    this.addNewProject = this.addNewProject.bind(this)
    this.deleteProject = this.deleteProject.bind(this)

    // Sort the apps by last updated property
    window.initialData.apps.sort((a, b) => {
      const dateA = dayjs(a.created)
      const dateB = dayjs(b.created)

      if (dateA.isBefore(dateB)) {
        return -1
      } else if (dateB.isBefore(dateA)) {
        return 1
      } else {
        return 0
      }
    })

    const savedData = []
    window.initialData.apps.map( (app) => {
      savedData.push(
        {
          name: app.name,
          url: app.webhook.url,
          contact: app.webhook.contact,
          siteid: app.webhook.siteid,
          roomid: app.webhook.roomid,
          callback_url: app.oauth.callback_url,
          editName: false,
        }
      )
    })

    this.state = { 
      savedData: savedData,
      data: window.initialData,
      view: `default`,
      toDelete: -1,
    }
  }

  render() {
    const { data: { name, cn, apps }, editName, savedData, view, toDelete} = this.state 

    const actions = {
      toggleEditTitle: this.toggleEditTitle,
      copyToClipBoard: this.copyToClipBoard,
      regenToken: this.regenToken,
      regenVerificationSecret: this.regenVerificationSecret,
      webhook: {
        saveURL: this.saveWebhookURL,
        saveContact: this.saveWebhookContact,
        saveSiteID: this.saveWebhookSiteID,
        saveRoomID: this.saveWebhookRoomID,
      },
      saveEditTitle: this.saveEditTitle,
      cancelEditTitle: this.cancelEditTitle,
      setScope: this.setScope,
      saveOAuthCallback: this.saveOAuthCallback,
      addNewProject: this.addNewProject,
      deleteProject: this.deleteProject,
    }

    return (
      <>
        <NavBar isScroll={false} />

        <Modal 
          isOpen={view == `add-project`}
          contentLabel="Create app form"
          onRequestClose={ () => this.setState({view: `default`}) }
          className="Modal"
          overlayClassName="Overlay"
          style={styles.modal}
        >
          <OverlayBox
            text="Enter the name of your new project"
            success={(value) => { actions.addNewProject(value) } }
            fail={() => { this.setState({view: `default`}) } }
          />
        </Modal>

        <Modal 
          isOpen={view == `delete-project`}
          contentLabel="Delete app form"
          onRequestClose={ () => this.setState({view: `default`}) }
          className="Modal"
          overlayClassName="Overlay"
          style={styles.modal}
        >
          {toDelete !== -1 ? (
            <OverlayBox
              text={"Enter the name of your project to confirm deletion (" + apps[toDelete].name  + ")"}
              success={(value) => { actions.deleteProject(toDelete) } }
              fail={() => { this.setState({view: `default`}) } }
              value={ apps[toDelete].name }
            />
          ) : null }
        </Modal>

        <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100%`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `80px` }}>
            <TextView text={`Welcome, ` + name}
              heading={1}
              align={`left`} 
              style={styles.baseText}
            />
            <TextView text={`Your username is: ` + cn}
              heading={2}
              align={`left`} 
              style={styles.lightText}
            />

            <div className="app-holder" style={styles.appHolder}>
              {apps.map( (app, index) => {
                const updated = this.timeSince(new Date(app.updated))
                const created = this.timeSince(new Date(app.created))

                const isPersonalTimetable = apps[index].oauth.scopes[0].enabled
                const isStudentNumber = apps[index].oauth.scopes[1].enabled

                return (
                  <CardView width='1-1' type='default' key={index} noPadding style={{ margin: `25px 0` }} >
                    <div className="default tablet"> { Title(`not-mobile`, app.name, created, updated, savedData[index].editName, 
                      () => { actions.toggleEditTitle(index) }, (reference, shouldPersist) => { actions.saveEditTitle(index, reference.current.value, shouldPersist) },
                      () => { actions.cancelEditTitle(index) },
                      () => { this.setState({ view: `delete-project`, toDelete: index }) } )}</div>
                    <div className="mobile"> { Title(`mobile`, app.name, created, updated, savedData[index].editName,
                      () => { actions.toggleEditTitle(index) }, (reference, shouldPersist) => { actions.saveEditTitle(index, reference.current.value, shouldPersist) },
                      () => { actions.cancelEditTitle(index) },
                      () => { this.setState({ view: `delete-project`, toDelete: index }) } )}</div>
                    
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        { Field(`API Token: `, app.token, {
                          copy: {action: actions.copyToClipBoard},
                          refresh: {action: () => { actions.regenToken(index) } },
                        }, {} ) }
                      </CardView>
                    </Row>
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        <div className="settings-collapse">
                          <Collapse>
                            <Panel header={`> OAuth Settings`} showArrow>
                              <Row styling='transparent' noPadding>
                                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                                  <TextView text={`OAuth Credentials: `}
                                    heading={3}
                                    align={`left`} 
                                    style={styles.oauthTitles}
                                  />
                                  { Field(`Client ID: `, app.oauth.client_id, {
                                    copy: {action: actions.copyToClipBoard},
                                  }, {} ) }
                                  { Field(`Client Secret: `, app.oauth.client_secret, {
                                    copy: {action: actions.copyToClipBoard},
                                  }, {} ) }
                                  { Field(`Callback URL: `, app.oauth.callback_url == `` ? `https://` : app.oauth.callback_url, {
                                    save: {action: (reference, shouldPersist) => { actions.saveOAuthCallback(index, reference.current.value, shouldPersist) } },
                                  }, {isNotSaved: app.oauth.callback_url != savedData[index].callback_url} ) }
                                </CardView>
                              </Row>
                              <Row styling='transparent' noPadding>
                                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                                  <TextView text={`OAuth Scopes: `}
                                    heading={3}
                                    align={`left`} 
                                    style={styles.oauthTitles}
                                  />
                                  { CheckBoxView(`Personal Timetable`, isPersonalTimetable, (value) => { actions.setScope(index, 0, value) } ) }
                                  { CheckBoxView(`Student Number`, isStudentNumber, (value) => { actions.setScope(index, 1, value) }) }
                                </CardView>
                              </Row>
                            </Panel>
                            <Panel header={`> Webhook Settings`} showArrow>
                              <Row styling='transparent' noPadding>
                                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                                  { Field(`Verification Secret:`, app.webhook.verification_secret, {
                                    copy: {action: actions.copyToClipBoard},
                                    refresh: {action: () => { actions.regenVerificationSecret(index) } },
                                  }, {} ) }
                                  { Field(`Webhook URL:`, app.webhook.url==`` ? `https://` : app.webhook.url, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveURL(index, reference.current.value, shouldPersist) } },
                                  }, {isNotSaved: app.webhook.url != savedData[index].url} ) }
                                  { Field(`'siteid' (optional):`, app.webhook.siteid, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveSiteID(index, reference.current.value, shouldPersist) } },
                                  }, {isNotSaved: app.webhook.siteid != savedData[index].siteid} ) }
                                  { Field(`'roomid' (optional):`, app.webhook.roomid, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveRoomID(index, reference.current.value, shouldPersist) } },
                                  }, {isNotSaved: app.webhook.roomid != savedData[index].roomid} ) }
                                  { Field(`Contact (optional):`, app.webhook.contact, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveContact(index, reference.current.value, shouldPersist) } },
                                  }, {isNotSaved: app.webhook.contact != savedData[index].contact} ) }
                                </CardView>
                              </Row>
                            </Panel>
                          </Collapse>
                        </div>
                      </CardView>
                    </Row>
                  </CardView>
                  )
              }
              )}
            </div>
            <ButtonView text={`Add new project`} type={`default`} 
              style={{ marginTop: `25px`, cursor: `pointer` }} 
              onClick={ () => { this.setState({ view: `add-project` }) } } fakeLink/>
          </Column>
        </Row>

        <Footer />
      </>
    )
  }

  addNewProject(name) {
    this.queryDashboardAPI(`/dashboard/api/create/`, `name=` + name, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Add the new app to the state so it gets rendered
      let newApp = json.app
      newApp['name'] = name

      const { data: { apps }, savedData } = this.state
      apps.push(newApp)

      // Update the saved data aswell
      savedData.push(
        {
          name: newApp.name,
          url: newApp.webhook.url,
          contact: newApp.webhook.contact,
          siteid: newApp.webhook.siteid,
          roomid: newApp.webhook.roomid,
          callback_url: newApp.oauth.callback_url,
          editName: false,
        }
      )

      // Go to new state visually
      this.setState({
        savedData: savedData,
        view: `default`, 
        data: {...this.state.data, apps: apps}
      })
    })
  }

  deleteProject(index) {
    const { data: { apps }, savedData } = this.state 

    this.queryDashboardAPI(`/dashboard/api/delete/`, `app_id=` + apps[index].id, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Remove the deleted app
      apps.splice(index, 1)
      savedData.splice(index, 1)

      // Go to new state visually
      this.setState({  
        toDelete: -1,
        savedData: savedData,
        view: `default`, 
        data: {...this.state.data, apps: apps}
      })
    })
  }

  cancelEditTitle(index) {
    const updatedData = {...this.state.data}
    updatedData.apps[index].name = this.state.savedData[index].name

    this.setState({ data: updatedData })
    this.toggleEditTitle(index)
  }

  saveEditTitle(index, value, shouldPersist) {
    const updatedData = {...this.state.data}
    updatedData.apps[index].name = value

    if(shouldPersist  && this.state.savedData[index].editName==true) {
      const updatedSavedData = this.state.savedData
      updatedSavedData[index].name = value

      // Send request
      const { data: { apps } } = this.state
      
      this.queryDashboardAPI(`/dashboard/api/rename/`, `new_name=` + value + `&app_id=` + apps[index].id, (json) => {
        if(this.DEBUGGING) { console.log(json) }
      })
      
      this.setState({ 
        data: updatedData,
        savedData: updatedSavedData,
      })
      this.toggleEditTitle(index)
    } else {
      this.setState({ data: updatedData })
    }
  }

  toggleEditTitle(index) {
    if(this.DEBUGGING) { console.log("edit title: " + index) }

    const updatedSavedData = this.state.savedData
    updatedSavedData[index].editName = !updatedSavedData[index].editName
    
    this.setState({savedData: updatedSavedData})
  }

  saveOAuthCallback(index, value, shouldPersist) {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      const updatedData = {...this.state.data}
      updatedData.apps[index].oauth.callback_url = value

      const persistedData = this.state.savedData

      if(shouldPersist) { 
        const { data: { apps }} = this.state

        this.queryDashboardAPI(`/dashboard/api/setcallbackurl/`, `app_id=` + apps[index].id + `&callback_url=` + value, (json) => {
          console.log(json)
        })
        persistedData[index].callback_url = value
      }

      this.setState(
        { 
          data: updatedData,
          savedData: persistedData, 
        }
      )
    }
  }

  setScope(index, scope, value) {
    const { data: { apps } } = this.state

    const scopesData = [
      {
        name: `timetable`,
        checked: apps[index].oauth.scopes[0].enabled,
      },
      {
        name: `student_number`,
        checked: apps[index].oauth.scopes[1].enabled,
      },
    ]

    scopesData[scope].checked = value

    const json = JSON.stringify(scopesData)

    this.queryDashboardAPI(`/dashboard/api/updatescopes/`, `app_id=` + apps[index].id + 
      `&scopes=` + encodeURIComponent(json), (json) => {
        console.log(json)
    })

    const updatedData = {...this.state.data}
    updatedData.apps[index].oauth.scopes[scope].enabled = value

    this.setState({ data: updatedData })
  }

  copyToClipBoard(e, reference){
    e.preventDefault()

    if(this.DEBUGGING) { console.log(`Copy to clipboard`) }
    if(this.DEBUGGING) { console.log(reference) }
    if(this.DEBUGGING) { console.log(e) }

    reference.current.select()
    
    try {
      document.execCommand(`copy`)
    }catch (err) {
      alert(`please press Ctrl/Cmd+C to copy`)
    }
  }

  regenToken(index) {
    const { data: { apps } } = this.state 

    this.queryDashboardAPI(`/dashboard/api/regen/`, `app_id=` + apps[index].id, (json) => {
      const values = {
        token: json.app.token,
        updated: json.app.date,
      }

      const updatedData = {...this.state.data}
      updatedData.apps[index].token = values.token

      this.setState({ data: updatedData })
    })
  }

  regenVerificationSecret(index) {
    const { data: { apps } } = this.state 

    this.queryDashboardAPI(`dashboard/api/webhook/refreshsecret/`, `app_id=` + apps[index].id, (json) => {
      const secret = json.new_secret

      const updatedData = {...this.state.data}
      updatedData.apps[index].webhook.verification_secret = secret

      this.setState({ data: updatedData })
    })
  }

  saveWebhookURL(index, value, shouldPersist) {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      const updatedData = {...this.state.data}
      updatedData.apps[index].webhook.url = value

      const persistedData = this.state.savedData

      if(shouldPersist) { 
        this.updateWebhookSettings({url: value}, index) 
        persistedData[index].url = value
      }

      this.setState(
        { 
          data: updatedData,
          savedData: persistedData, 
        }
      )
    }
  }
  saveWebhookContact(index, value, shouldPersist) {
    const updatedData = {...this.state.data}
    updatedData.apps[index].webhook.contact = value

    const persistedData = this.state.savedData

    if(shouldPersist) { 
      this.updateWebhookSettings({contact: value}, index) 
      persistedData[index].contact = value
    }

    this.setState(
      { 
        data: updatedData,
        savedData: persistedData, 
      }
    )
  }
  saveWebhookSiteID(index, value, shouldPersist) {
    const updatedData = {...this.state.data}
    updatedData.apps[index].webhook.siteid = value

    const persistedData = this.state.savedData

    if(shouldPersist) { 
      this.updateWebhookSettings({siteid: value}, index)
      persistedData[index].siteid = value
    }

    this.setState(
      { 
        data: updatedData,
        savedData: persistedData, 
      }
    )
  }
  saveWebhookRoomID(index, value, shouldPersist) {
    const updatedData = {...this.state.data}
    updatedData.apps[index].webhook.roomid = value

    const persistedData = this.state.savedData

    if(shouldPersist) { 
      this.updateWebhookSettings({roomid: value}, index)
      persistedData[index].roomid = value
    }

    this.setState(
      { 
        data: updatedData,
        savedData: persistedData, 
      }
    )
  }

  updateWebhookSettings(settings, index) {
    const { data: { apps }} = this.state

    let siteid = ``
    let roomid = ``
    let contact = ``
    let url = ``

    const app = this.state.savedData[index]

    if(app.siteid) { siteid = app.siteid }
    if(app.roomid) { roomid = app.roomid }
    if(app.contact) { contact = app.contact }
    if(app.url) { url = app.url }

    if(settings.siteid) { siteid = settings.siteid }
    if(settings.roomid) { roomid = settings.roomid }
    if(settings.contact) { contact = settings.contact }
    if(settings.url) { url = `https://` + settings.url }

    const parameters = `url=` + url + `&siteid=` + siteid + `&roomid=` + roomid 
      + `&contact=` + contact + `&app_id=` + apps[index].id

    this.queryDashboardAPI(`dashboard/api/webhook/edit/`, parameters, (json) => {
        console.log(`For parameters: ` + parameters)
        console.log(json)
    })
  }

  queryDashboardAPI(url, querystring, callback) {
    fetch(url, {
      method: `POST`,
      credentials: `include`,
      headers: defaultHeaders,
      body: querystring,
    }).then((res)=>{
      return res.json()
    }).then(callback)
    .catch((err)=>{
      console.log(`Failed to save details to: ` + url)
      console.log(err)
    })
  }

  timeSince(date) {
    const seconds = Math.floor((new Date() - date) / 1000)

    let interval = Math.floor(seconds / 31536000)

    if (interval > 1) {
      return interval + ` years`
    }
    interval = Math.floor(seconds / 2592000)
    if (interval > 1) {
      return interval + ` months`
    }
    interval = Math.floor(seconds / 86400)
    if (interval > 1) {
      return interval + ` days`
    }
    interval = Math.floor(seconds / 3600)
    if (interval > 1) {
      return interval + ` hours`
    }
    interval = Math.floor(seconds / 60)
    if (interval > 1) {
      return interval + ` minutes`
    }
    return Math.floor(seconds) + ` seconds`
  }
}

ReactDOM.render(
  <Dashboard />,
  document.querySelector(`.app`)
)
