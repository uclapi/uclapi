import React from 'react'

// Stylings
import { styles } from 'Layout/data/dashboard_styles.jsx'

// Components
import { CardView, Column, Footer, NavBar, Row, TextView, 
  ButtonView, Field, ConfirmBox, CheckBox } from 'Layout/Items.jsx'
import { editIcon, cancelIcon } from 'Layout/Icons.jsx'

// External dependencies
import Collapse, { Panel } from 'rc-collapse'


/**
	UI Definition of the app, all of the "actions" should be passed in from
	the dashboard page and they will do all the heavy lifting whereas this
	page is only a ui representation
**/

export default class App extends React.Component {
	
	constructor(props) { 
		super(props)

		this.DEBUGGING = true

		const { app } = this.props

		const updated = this.timeSince(new Date(app.updated))
        const created = this.timeSince(new Date(app.created))

        this.state = {
        	updated: updated,
        	created: created
        }
	}

	componentDidUpdate(prevProps) {
		const { app, index } = this.props

		if(this.DEBUGGING) { console.log("App updated") }

		if(app != prevProps.app || index != prevProps.index) { 
			const { app } = this.props

			const updated = this.timeSince(new Date(app.updated))
	        const created = this.timeSince(new Date(app.created))

	        this.setState({
	        	updated: updated,
	        	created: created
	        })
		}
	}

	render() {
		const { updated, created } = this.state
		const { app, actions, index } = this.props

		if(this.DEBUGGING) { console.log("re-rendering app, name: " + app.name) }

		const trashColor = "red"

		return (
		<Collapse>
        <Panel header={app.name} showArrow>
        <Row styling='transparent' noPadding>
		  
		    <Row styling='transparent' noPadding>
		      <CardView width="1-2" minWidth="200px" type="no-bg" style={styles.squareCard} snapAlign>
		        <Field
		          title="title: "
		          content={app.name}
		          onSave={(value) => { actions.saveEditTitle(index, value) }}
		          isSmall={true}
		        />
		      </CardView>
		      <CardView width="1-2" minWidth="200px" type="no-bg" snapAlign style={styles.rowItem}>
	          	<div className="default tablet">
		          	{cancelIcon(
			          () => { actions.deleteConfirm(index) },
			          { float: `right`, marginTop: `40px`, backgroundColor: trashColor }
			        )}
			        <div className="app-times" style={{ float: `right`, marginTop: `40px` }}>
				        <TextView text={`Created: ` + created + ` ago`} heading={6}
				          align="right" style={styles.dates} />
				        <TextView text={`Updated: ` + updated + ` ago`} heading={6}
				          align="right" style={styles.dates} />
		          	</div>
	          	</div>
		        <div className="mobile">
		        	<div className="app-times" style={{ margin: `8px auto` }}>
				        <TextView text={`Created: ` + created + ` ago`} heading={5}
				          align="center" style={styles.dates} />
				        <TextView text={`Updated: ` + updated + ` ago`} heading={5}
				          align="center" style={styles.dates} />
				        {cancelIcon(
				          () => { actions.deleteConfirm(index) },
				          { margin: `auto`, float: `unset`, marginTop: `10px` }
				        )}
		          	</div>
		        </div>
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
		            <Panel header={`OAuth Settings`} showArrow>
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
		                  {app.oauth.scopes.map( (scope, scope_index) => 
			                  <CheckBox 
			                    text={scope.name}
			                    isChecked={scope.enabled}
			                    onClick={(value) => { actions.setScope(index, scope_index, value) } }
			                    style={{ float: `left`, margin: `12px 10px 0 10px` }}
			                  />
		                  )}
		                </CardView>
		              </Row>
		            </Panel>
		            <Panel header={`Webhook Settings`} showArrow>
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
		

        </Row>
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