// Styling
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Dependencies
import dayjs from 'dayjs'
import Cookies from 'js-cookie';

import React from 'react'
import ReactDOM from 'react-dom'

import Collapse, { Panel } from 'rc-collapse'

// Components
import { CardView, CheckBox,Column,   Footer, ImageView,
NavBar, Row, TextView } from 'Layout/Items.jsx'

import { styles } from 'Layout/data/dashboard_styles.jsx'
import { Icon, CheckBoxView, Field,
  clipboardIcon, refreshIcon, editIcon, saveIcon } from 'Dashboard/DashboardUI.jsx'

const defaultHeaders = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-CSRFToken': Cookies.get('csrftoken')
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
    <CardView width={size==="mobile" ? '1-1' : '1-2'} minWidth="140px" type="no-bg" style={styles.squareCard} snapAlign>
      { !isEditing ? (
          <>
            <TextView text={title}
              heading={2}
              align={size==="mobile" ? `center` : `left`} 
              style={styles.titleText}
            />
            {editIcon(actions.toggleEditTitle)} 
          </>
        ) : (
          <>
            { Field(`Title: `, title, {
              save: {action: actions.test},
              cancel: {action: actions.toggleEditTitle}
            }, {isSmall: true} ) }
          </>
        )
      }
    </CardView>
    <CardView width={size==="mobile" ? '1-1' : '1-2'} minWidth="140px" type="no-bg" snapAlign>
      {size==="mobile" ? (
        Dates(created, updated, "center")
      ) : (
        Dates(created, updated, "right")
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
    this.testEvent = this.testEvent.bind(this)
    this.copyToClipBoard = this.copyToClipBoard.bind(this)
    this.regenToken = this.regenToken.bind(this)

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
                    <div className="default tablet"> { Title("not-mobile", app.name, created, updated, editName, actions)}</div>
                    <div className="mobile"> { Title("mobile", app.name, created, updated, editName, actions) } </div>
                    
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        { Field(`API Token: `, app.token, {
                          copy: {action: actions.copyToClipBoard},
                          refresh: {action: () => { actions.regenToken(index) } }
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
                                    copy: {action: actions.copyToClipBoard}
                                  }, {} ) }
                                  { Field(`Client Secret: `, app.oauth.client_secret, {
                                    copy: {action: actions.copyToClipBoard}
                                  }, {} ) }
                                  { Field(`Callback URL: `, app.oauth.callback_url, {
                                    copy: {action: actions.copyToClipBoard}
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
                                    save: {action: actions.test},
                                    refresh: {action: actions.test}
                                  }, {} ) }
                                  { Field(`Webhook URL:`, app.webhook.url, {
                                    save: {action: actions.test}
                                  }, {} ) }
                                  { Field(`'siteid' (optional):`, app.webhook.siteid, {
                                    save: {action: actions.test}
                                  }, {} ) }
                                  { Field(`'roomid' (optional):`, app.webhook.roomid, {
                                    save: {action: actions.test}
                                  }, {} ) }
                                  { Field(`Contact (optional):`, app.webhook.contact, {
                                    save: {action: actions.test}
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
    console.log("Click has been tested")
  }

  copyToClipBoard(e, reference){
    e.preventDefault()

    if(this.DEBUGGING) { console.log("Copy to clipboard") }
    if(this.DEBUGGING) { console.log(reference) }
    if(this.DEBUGGING) { console.log(e) }

    reference.current.select()
    
    try {
      document.execCommand('copy')
    }catch (err) {
      alert('please press Ctrl/Cmd+C to copy');
    }
  }

  regenToken = (index) => {

    const { data: { apps } } = this.state 

    // Query the backend endpoint to fetch a new token
    // Also updates server side for persistence
    fetch('/dashboard/api/regen/', {
      method: 'POST',
      credentials: 'include',
      headers: defaultHeaders,
      body: 'app_id=' + apps[index].appId
    }).then((res) => {
      
      // Check whether respose has ok'ed on the backend
      if (res.ok) { return res.json(); }
      throw new Error('Unable to regen token.');
    }).then((json) => {
      
      // Assuming all is okay then access the json
      if (json.success) {
        // The important details from the response
        let values = {
          token: json.app.token,
          updated: json.app.date
        };
        // Update the state of the app (visual)
        const { data: updatedData } = this.state 
        updatedData[index].token = values.token

        this.setState({
          data: updatedData
        })
        return;
      }

      throw new Error(json.message);
    }).catch((err) => {
      console.error("Token not refreshed")
      console.error(err.message)
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
