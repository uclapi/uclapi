// Styling
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Dependencies
import dayjs from 'dayjs'
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'
import ReactDOM from 'react-dom'

// Images
import clipboardImage from 'Images/dashboard/clipboard.svg'
import refreshImage from 'Images/dashboard/refresh.svg'
import saveImage from 'Images/dashboard/save.svg'
import deleteImage from 'Images/dashboard/trash.svg'
// Components
import { CardView, CheckBox,Column,   Footer, ImageView,
NavBar, Row, TextView } from 'Layout/Items.jsx'

const styles = {
  baseText: {
    color: `white`,
    fontWeight: `300`,
  },
  titleText: {
    color: `white`,
    fontWeight: `300`,
    marginBottom: `0`,
  },
  oauthTitles: {
    color: `white`,
    fontWeight: `300`,
    padding: `10px 0`,
    textDecoration: `underline`,
  },
  lightText: {
    color: `#ddd`,
    fontWeight: `100`,
  },
  dates: {
    color: `#ddd`,
    fontWeight: `100`,
    margin: `0`,
  },
  appHolder: {
    marginTop: `80px`,
  },
  tokenHolder: {
    borderRadius: `0`,
  },
  copyableField: {
    marginTop: `0`,
    width: `80%`,
    padding: `15px`,
    textAlign: `left`,
  },
  copyableFieldMobile: {
    marginTop: `0`,
    width: `auto`,
    padding: `15px`,
    textAlign: `left`,
    maxWidth: `50%`,
  },
  tokenText: {
    float: `left`,
    margin: `6px 10px 0 0`,
    color: `white`,
    fontWeight: `30 y5r 64taeyrwgT\EQaW FR0`,
  },
  button: {
    height: `40px`,
    maxWidth: `40px`,
    minWidth: `40px`,
    float: `right`,
    margin: `5px`,
    marginLeft: `5px`,
  },
  buttonIcon: {
    marginTop: `8px`,
  },
  fieldHolder: {
    height: `50px`,
    paddingBottom: `20px`,
  },
  field: {
    backgroundColor: `#3498db`,
    height: `50px`,
    float: `left`,
    paddingRight: `10px`,
    width: `100%`,
  },
  checkBox: {
    margin: `10px`,
    float: `left`,
  },
}

const logosize = `20px`

const Icon = (image, description) => (
  <CardView width='1-3' type='emphasis' style={styles.button} fakeLink>
    <ImageView src={image}
      width={logosize}
      height={logosize}
      description={description} 
      style={styles.buttonIcon}
      isCentered
    />
  </CardView>
)

const CheckBoxView = (text, value) => (
  <>                      
    <div className="field" style={styles.field}>
      <CheckBox onClick={ (value) => {console.log(`check box clicked: ` + value)} } isChecked={value} style={styles.checkBox}/>
      <TextView text={text} heading={5} align={`left`} style={styles.tokenText} /> 
      {saveIcon}
    </div>
  </>
)

const clipboardIcon = Icon(clipboardImage, `copy token to clipboard`)
const refreshIcon = Icon(refreshImage, `refresh token`)
const saveIcon = Icon(saveImage, `save details for future`)

const Field = (title, content, icons) => (
  <>
    <TextView text={title} heading={5} align={`left`} style={styles.tokenText} />
                          
    <div className="field" style={styles.field}>
      <div className="tablet default">
        <input type="text" className="token-input" readOnly value={content} style={styles.copyableField}/>
      </div>
      <div className="mobile">
        <input type="text" className="token-input" readOnly value={content} style={styles.copyableFieldMobile}/>
      </div>
      {icons.includes(`copy`) ? clipboardIcon : null}
      {icons.includes(`refresh`) ? refreshIcon : null}
      {icons.includes(`save`) ? saveIcon : null}
    </div>
  </>
)

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

const Title = (size, title, created, updated) => (
  <Row styling='transparent' noPadding>
    <CardView width={size==="mobile" ? '1-1' : '1-2'} minWidth="140px" type="no-bg" snapAlign>
      <TextView text={title}
        heading={2}
        align={size==="mobile" ? `center` : `left`} 
        style={styles.titleText}
      />
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
  
class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

    this.timeSince = this.timeSince.bind(this)

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

    this.state = { data: window.initialData }
  }
  render() {
    const { data: { name, cn, apps } } = this.state 

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
                    <div className="default tablet"> { Title("not-mobile", app.name, created, updated) }</div>
                    <div className="mobile"> { Title("mobile", app.name, created, updated) } </div>
                    
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        { Field(`API Token: `, app.token, [`copy`, `refresh`] ) }
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
                                  { Field(`Client ID: `, app.oauth.client_id, [`copy`] ) }
                                  { Field(`Client Secret: `, app.oauth.client_secret, [`copy`] ) }
                                  { Field(`Callback URL: `, app.oauth.callback_url, [`save`] ) }
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
                                  { Field(`Verification Secret:`, app.webhook.verification_secret, [`save`, `refresh`] ) }
                                  { Field(`Webhook URL:`, app.webhook.url, [`save`] ) }
                                  { Field(`'siteid' (optional):`, app.webhook.siteid, [`save`] ) }
                                  { Field(`'roomid' (optional):`, app.webhook.roomid, [`save`] ) }
                                  { Field(`Contact (optional):`, app.webhook.contact, [`save`] ) }
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
