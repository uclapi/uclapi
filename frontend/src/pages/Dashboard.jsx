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

import { CheckBoxView } from 'Dashboard/DashboardUI.jsx'
import { styles } from 'Layout/data/dashboard_styles.jsx'

// Components
import { CardView, Column, Footer, NavBar, Row, TextView, 
  ButtonView, Field, ConfirmBox} from 'Layout/Items.jsx'
import { editIcon, cancelIcon } from 'Layout/Icons.jsx'

const defaultHeaders = {
  'Content-Type': `application/x-www-form-urlencoded`,
  'X-CSRFToken': Cookies.get(`csrftoken`),
}
  
class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

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

    this.state = { 
      data: window.initialData,
      view: `default`,
      toDelete: -1,
    }
  }

  render() {
    const { data: { name, cn, apps }, view, toDelete} = this.state 

    const actions = {
      toggleEditTitle: this.toggleEditTitle,
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
      deleteConfirm: this.deleteConfirm
    }

    if(this.DEBUGGING) { console.log("re-rendered dashboard") }

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
          <ConfirmBox
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
            <ConfirmBox
              text={"Enter the name of your project to confirm deletion (" + apps[toDelete].name  + ")"}
              success={(value) => { actions.deleteProject(toDelete) } }
              fail={() => { this.setState({view: `default`}) } }
              value={ apps[toDelete].name }
              shouldCheckValue
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
                    <Row styling='transparent' noPadding>
                      <CardView width="1-1" minWidth="140px" type="no-bg" style={styles.squareCard} snapAlign>
                        <Field
                          title="title: "
                          content={app.name}
                          onSave={(value) => { actions.saveEditTitle(index, value) }}
                          isSmall={true}
                        />
                      </CardView>
                      <CardView width="1-1" minWidth="140px" type="no-bg" snapAlign style={styles.rowItem}>
                        <TextView text={`Created: ` + created + ` ago`}
                          heading={5}
                          align="left" 
                          style={styles.dates}
                        />
                        <TextView text={`Updated: ` + updated + ` ago`}
                          heading={5}
                          align="left"
                          style={styles.dates}
                        />
                      </CardView>
                    </Row>
                    
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        <Field
                          title="API Token: "
                          content={app.token}
                          canCopy
                          onRefresh={ () => { actions.regenToken(index) } }
                        />
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
                                  <Field
                                    title="Client ID: "
                                    content={app.oauth.client_id}
                                    canCopy
                                  />
                                  <Field
                                    title="Client Secret: "
                                    content={app.oauth.client_secret}
                                    canCopy
                                  />
                                  <Field
                                    title="Callback Url: "
                                    content={app.oauth.callback_url == '' ? 'https://' : app.oauth.callback_url}
                                    canCopy
                                    onSave={(value) => { actions.saveOAuthCallback(index, value) }}
                                  />
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
                                  <Field
                                    title="Verification Secret: "
                                    content={app.webhook.verification_secret}
                                    canCopy
                                    onRefresh={() => { actions.regenVerificationSecret(index) }}
                                  />
                                  <Field
                                    title="Webhook URL: "
                                    content={app.webhook.url=='' ? 'https://' : app.webhook.url}
                                    onSave={(value) => { actions.webhook.saveURL(index, value) } }
                                  />
                                  <Field
                                    title="'siteid' (optional):"
                                    content={app.webhook.siteid}
                                    onSave={(value) => { actions.webhook.saveSiteID(index, value) }}
                                  />
                                  <Field
                                    title="'roomid' (optional):"
                                    content={app.webhook.roomid}
                                    onSave={(value) => { actions.webhook.saveRoomID(index, value) }}
                                  />
                                  <Field
                                    title="Contact (optional):"
                                    content={app.webhook.contact}
                                    onSave={(value) => { actions.webhook.saveContact(index, value) }}
                                  />
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

  addNewProject = (name) => {
    this.queryDashboardAPI(`/dashboard/api/create/`, `name=` + name, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Add the new app to the state so it gets rendered
      let newApp = json.app
      newApp['name'] = name

      const { data } = this.state
      data.apps.push(newApp)

      // Go to new state visually
      this.setState({
        view: `default`, 
        data: data
      })
    })
  }

  deleteConfirm = (index) => {
    this.setState({ 
      view: `delete-project`, 
      toDelete: index,
    })
  }

  deleteProject = (index) => {
    const { data } = this.state

    this.queryDashboardAPI(`/dashboard/api/delete/`, `app_id=` + data.apps[index].id, (json) => {
      // For debugging
      if(this.DEBUGGING) { console.log(json) }

      // Remove the deleted app
      data.apps.splice(index, 1)

      // Go to default state visually
      this.setState({  
        toDelete: -1,
        view: `default`, 
        data: data
      })
    })
  }

  saveEditTitle = (index, value) => {
    const { data } = this.state
    
    this.queryDashboardAPI(`/dashboard/api/rename/`, `new_name=` + value + `&app_id=` + data.apps[index].id, (json) => {
      if(this.DEBUGGING) { console.log(json) }
    })
    
    data.apps[index].name = value
    this.setState({ data: data })
  }

  saveOAuthCallback = (index, value) => {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      const { data } = this.state
      data.apps[index].oauth.callback_url = value

      this.queryDashboardAPI(`/dashboard/api/setcallbackurl/`, `app_id=` + updatedData.apps[index].id + `&callback_url=` + value, (json) => {
        console.log(json)
      })

      this.setState({ data: data })
    }
  }

  setScope = (index, scope, value) => {
    const { data } = this.state

    // Update data
    data.apps[index].oauth.scopes[scope].enabled = value

    // Convert scopes into form for backend
    const scopes = data.apps[index].oauth.scopes
    const scopesData = scopes.map( scope => 
      ({
        name: scope.name, 
        checked: scope.enabled
      }))

    const json = JSON.stringify(scopesData)

    this.queryDashboardAPI(`/dashboard/api/updatescopes/`, `app_id=` + data.apps[index].id + 
      `&scopes=` + encodeURIComponent(json), (json) => {
        console.log(json)
    })

    this.setState({ data: data })
  }

  regenToken = (index) => {
    const { data } = this.state 

    this.queryDashboardAPI(`/dashboard/api/regen/`, `app_id=` + data.apps[index].id, (json) => {
      data.apps[index].token = json.app.token 
      this.setState({ data: data })
    })
  }

  regenVerificationSecret = (index) => {
    const { data } = this.state 

    this.queryDashboardAPI(`dashboard/api/webhook/refreshsecret/`, `app_id=` + data.apps[index].id, (json) => {
      data.apps[index].webhook.verification_secret = json.new_secret
      this.setState({ data: data })
    })
  }

  saveWebhookURL = (index, value) => {
    if(value.startsWith("https://") || value.startsWith("http://") || value=="") {
      this.updateWebhookSettings({url: value}, index) 
    }
  }

  saveWebhookContact = (index, value) => { this.updateWebhookSettings({contact: value}, index) }
  saveWebhookSiteID = (index, value) => { this.updateWebhookSettings({siteid: value}, index) }
  saveWebhookRoomID = (index, value) => { this.updateWebhookSettings({roomid: value}, index) }

  updateWebhookSettings = (newValues, index) => {
    const { data } = this.state

    const app = data.apps[index]
    var values = {...app.webhook, ...newValues}

    const parameters = `url=` + values.url + `&siteid=` + values.siteid + `&roomid=` + values.roomid 
      + `&contact=` + values.contact + `&app_id=` + data.apps[index].id

    this.queryDashboardAPI(`dashboard/api/webhook/edit/`, parameters, (json) => {
        console.log(`For parameters: ` + parameters)
        console.log(json)
    })

    data.apps[index].webhook = values
    this.setState({ data: data })
  }

  queryDashboardAPI = (url, querystring, callback) => {
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

  timeSince = (date) => {
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
