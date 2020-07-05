/* eslint-disable react/prop-types */
/* eslint-disable react/jsx-no-bind */
// Stylings
import { styles } from 'Layout/data/dashboard_styles.jsx'
// Components
import {
	ButtonView, CheckBox,
	Column, Container, Field, Row, TextView,
} from 'Layout/Items.jsx'
// External dependencies
import Collapse, { Panel } from 'rc-collapse'
import React from 'react'

/**
  UI Definition of the app, all of the "actions" should be passed in from
  the dashboard page and they will do all the heavy lifting whereas this
  page is only a ui representation
**/

function expandIcon({ isActive }) {
  return (
      <div
        style={{
          marginRight: `.5rem`,
          display: `inline-block`,
          transition: `transform .2s`,
          transform: `rotate(${isActive ? 90 : 0}deg)`,
        }}
      >
        &#707;
      </div>
  )
}

export default class App extends React.Component {
  
  constructor(props) { 
    super(props)

    this.DEBUGGING = true

    const { app } = this.props

    const updated = this.timeSince(new Date(app.updated))
        const created = this.timeSince(new Date(app.created))

        this.state = {
          updated: updated,
          created: created,
        }
  }

  componentDidUpdate(prevProps) {
    const { app, index } = this.props

    if(this.DEBUGGING) { console.log(`App updated`) }

    if(app != prevProps.app || index != prevProps.index) { 
      const { app } = this.props

      const updated = this.timeSince(new Date(app.updated))
          const created = this.timeSince(new Date(app.created))

          this.setState({
            updated: updated,
            created: created,
          })
    }
  }

  render() {
    const { updated, created } = this.state
    const { app, actions, index } = this.props

    if(this.DEBUGGING) { console.log(`re-rendering app, name: ` + app.name) }

    // const trashColor = `red`

    console.log(app.oauth.scopes)

    return (
    <Collapse expandIcon={expandIcon}>
        <Panel header={app.name} showArrow>

      <Container styling='transparent' noPadding>
        <Row width="1-1">
          <Column 
            width="1-1" 
            className="title-holder"
          >
            <Field
              title="Title: "
              content={app.name}
              onSave={(value) => { actions.saveEditTitle(index, value) }}
              isSmall
            />
            <Field
              title="API Token: "
              content={app.token}
              canCopy
              onRefresh={ () => { actions.regenToken(index) } }
            />
          </Column>
        </Row>
        
        <Container styling='transparent' noPadding>
          <Column 
            width='1-1' 
            className="settings-collapse"
            noPadding
          >
            <Collapse expandIcon={expandIcon}>
              <Panel header={`OAuth Settings`} showArrow>
              <Container styling='transparent' noPadding>
                <Column
                  width='1-1' 
                  className='settings-section'
                >
                  <TextView text={`OAuth Credentials: `}
                    heading={4}
                    align={`left`} 
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
                    content={app.oauth.callback_url == `` ? `https://` : app.oauth.callback_url}
                    canCopy
                    onSave={(value) => { actions.saveOAuthCallback(index, value) }}
                  />
                </Column>
              </Container>
              <Container styling='transparent' noPadding>
                <Column
                  width='1-1' 
                  className='settings-section'
                >
                  <TextView text={`OAuth Scopes: `}
                    heading={4}
                    align={`left`} 
                  />
                  {app.oauth.scopes.map( (scope, scope_index) => 
                    <CheckBox
                      key={scope_index}
                      text={scope.description}
                      isChecked={scope.enabled}
                      onClick={(value) => { actions.setScope(index, scope_index, value) } }
                      style={{
												float: `left`,
												margin: `12px 10px 0 10px`,
											}}
                    />
                  )}
                </Column>
              </Container>
              </Panel>
              <Panel header={`Webhook Settings`} showArrow>
              <Container styling='transparent' noPadding>
                <Column
                  width='1-1' 
                  className='settings-section'
                >
                  <Field
                    title="Verification Secret: "
                    content={app.webhook.verification_secret}
                    canCopy
                    onRefresh={() => { actions.regenVerificationSecret(index) }}
                  />
                  <Field
                    title="Webhook URL: "
                    content={app.webhook.url==`` ? `https://` : app.webhook.url}
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
                </Column>
              </Container>
              </Panel>
            </Collapse>
          </Column>
        </Container>
        <Container styling='transparent' noPadding>
          <Row width="1-1">
            <Column 
              width="1-1"
              className="bottom-app-column"
              keepInline
            >
              <Column 
                width="165px" 
                alignItems="column"
                className="dates-holder default tablet" 
                keepInline
              >
                <TextView text={`Created: ` + created + ` ago`}
                  heading={5}
                  align="left"
                  style={styles.dates}
                  color="white"
                />
                <TextView text={`Updated: ` + updated + ` ago`}
                  heading={5}
                  align="left"
                  style={styles.dates}
                  color="white"
                />
              </Column>

              <ButtonView
                text={`Delete`} 
                type={`remove`} 
                onClick={() => { actions.deleteConfirm(index) }} 
                fakeLink 
                style={{ cursor: `pointer` }} 
              />
            </Column>
          </Row>
        </Container>
      </Container>
        </Panel>
        </Collapse>
    )
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