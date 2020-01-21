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
import update from 'immutability-helper';

import { CheckBoxView,   clipboardIcon, editIcon, Field,
Icon, refreshIcon, saveIcon } from 'Dashboard/DashboardUI.jsx'
import { styles } from 'Layout/data/dashboard_styles.jsx'
// Components
import { CardView, CheckBox,Column,   Footer, ImageView,
NavBar, Row, TextView } from 'Layout/Items.jsx'

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

const Title = (size, title, created, updated, isEditing, actions) => {
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
            {editIcon(actions.toggleEditTitle)} 
          </>
        ) : (
          <>
            { Field(`Title: `, title, {
              save: {action: actions.test},
              cancel: {action: actions.toggleEditTitle},
            }, {isSmall: true} ) }
          </>
        )
      }
    </CardView>
    <CardView width={size===`mobile` ? `1-1` : `1-2`} minWidth="140px" type="no-bg" snapAlign>
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
    this.copyToClipBoard = this.copyToClipBoard.bind(this)
    
    this.testEvent = this.testEvent.bind(this)

    this.regenToken = this.regenToken.bind(this)
    this.regenVerificationSecret = this.regenVerificationSecret.bind(this)

    this.saveWebhookURL = this.saveWebhookURL.bind(this)
    this.saveWebhookContact = this.saveWebhookContact.bind(this)
    this.saveWebhookSiteID = this.saveWebhookSiteID.bind(this)
    this.saveWebhookRoomID = this.saveWebhookRoomID.bind(this)

    this.queryDashboardAPI = this.queryDashboardAPI.bind(this)

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
      editName: false,
    }
  }

  render() {
    const { data: { name, cn, apps }, editName} = this.state 

    const actions = {
      toggleEditTitle: this.toggleEditTitle,
      test: this.testEvent,
      copyToClipBoard: this.copyToClipBoard,
      regenToken: this.regenToken,
      regenVerificationSecret: this.regenVerificationSecret,
      webhook: {
        saveURL: this.saveWebhookURL,
        saveContact: this.saveWebhookContact,
        saveSiteID: this.saveWebhookSiteID,
        saveRoomID: this.saveWebhookRoomID
      }
    }

    return (
      <>
        <NavBar isScroll={false} />

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
                const created = this.timeSince(new Date(app.updated))

                return (
                  <CardView width='1-1' type='default' key={index} noPadding>
                    <div className="default tablet"> { Title(`not-mobile`, app.name, created, updated, editName, actions)}</div>
                    <div className="mobile"> { Title(`mobile`, app.name, created, updated, editName, actions) } </div>
                    
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
                                  { Field(`Callback URL: `, app.oauth.callback_url, {
                                    copy: {action: actions.copyToClipBoard},
                                  }, {} ) }
                                </CardView>
                              </Row>
                              <Row styling='transparent' noPadding>
                                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                                  <TextView text={`OAuth Scopes: `}
                                    heading={3}
                                    align={`left`} 
                                    style={styles.oauthTitles}
                                  />
                                  { CheckBoxView(`Personal Timetable`, false) }
                                  { CheckBoxView(`Student Number`, false) }
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
                                  { Field(`Webhook URL:`, app.webhook.url, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveURL(index, reference.current.value, shouldPersist) } },
                                  }, {} ) }
                                  { Field(`'siteid' (optional):`, app.webhook.siteid, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveSiteID(index, reference.current.value, shouldPersist) } },
                                  }, {} ) }
                                  { Field(`'roomid' (optional):`, app.webhook.roomid, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveRoomID(index, reference.current.value, shouldPersist) } },
                                  }, {} ) }
                                  { Field(`Contact (optional):`, app.webhook.contact, {
                                    save: {action: (reference, shouldPersist) => { actions.webhook.saveContact(index, reference.current.value, shouldPersist) } },
                                  }, {} ) }
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
          </Column>
        </Row>

        <Footer />
      </>
    )
  }

  toggleEditTitle() {
    const { editName } = this.state

    this.setState({editName: !editName})
  }

  testEvent() {
    console.log(`Click has been tested`)
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

      var updatedData = {...this.state.data}
      updatedData.apps[index].token = values.token

      this.setState({ data: updatedData })
    });
  }

  regenVerificationSecret(index) {
    const { data: { apps } } = this.state 

    this.queryDashboardAPI('dashboard/api/webhook/refreshsecret/', `app_id=` + apps[index].id, (json) => {
      const secret = json.new_secret

      var updatedData = {...this.state.data}
      updatedData.apps[index].webhook.verification_secret = secret

      this.setState({ data: updatedData })
    });
  }

  saveWebhookURL(index, value, shouldPersist) {
    if(shouldPersist) {
      // Code to handle making request
    }

    var updatedData = {...this.state.data}
    updatedData.apps[index].webhook.url = value

    this.setState({ data: updatedData })
  }
  saveWebhookContact(index, value, shouldPersist) {
    if(shouldPersist) {
      // Code to handle making request
    }

    var updatedData = {...this.state.data}
    updatedData.apps[index].webhook.contact = value

    this.setState({ data: updatedData })
  }
  saveWebhookSiteID(index, value, shouldPersist) {
    if(shouldPersist) {
      // Code to handle making request
    }

    var updatedData = {...this.state.data}
    updatedData.apps[index].webhook.siteid = value

    this.setState({ data: updatedData })
  }
  saveWebhookRoomID(index, value, shouldPersist) {
    if(shouldPersist) {
      // Code to handle making request
    }

    var updatedData = {...this.state.data}
    updatedData.apps[index].webhook.roomid = value

    this.setState({ data: updatedData })
  }

  queryDashboardAPI(url, querystring, callback) {
    fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: defaultHeaders,
      body: querystring
    }).then((res)=>{
      return res.json()
    }).then(callback)
    .catch((err)=>{
      console.log("Failed to save details to: " + url)
      console.err(err);
    });
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
