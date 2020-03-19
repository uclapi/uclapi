import React from 'react'

// Stylings
import { styles } from 'Layout/data/dashboard_styles.jsx'

// Components
import { CardView, Column, Footer, NavBar, Row, TextView, 
  ButtonView, Field, ConfirmBox, CheckBox, Container } from 'Layout/Items.jsx'
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
        <Container styling='transparent' noPadding>
		    <Row width="1-1">
		      	<Column width="1-2" >
			        <Field
			          title="title: "
			          content={app.name}
			          onSave={(value) => { actions.saveEditTitle(index, value) }}
			          isSmall={true}
			        />
		      	</Column>
		      	<Column width="1-2">
		          	<Row width="auto" style={{ float: `right` }}>
						<Column 
							width="auto" 
							alignItems="column" 
						>
		          			<TextView text={`Created: ` + created + ` ago`} heading={5}
					          align="left" style={styles.dates} color="white" />
					        <TextView text={`Updated: ` + updated + ` ago`} heading={5}
					          align="left" style={styles.dates} color="white" />
		          		</Column>
						<Column 
							width="auto" 
							style={{ padding: `0 0 0 20px` }}
						>
		          			{cancelIcon(
					          () => { actions.deleteConfirm(index) },
					        )}
		          		</Column>
		          	</Row>
			    </Column>
		    </Row>
		    
		    <Container styling='transparent' noPadding>
		      <CardView width='1-1' type="no-bg" style={styles.tokenHolder} noPadding >
		        <Field
		          title="API Token: "
		          content={app.token}
		          canCopy
		          onRefresh={ () => { actions.regenToken(index) } }
		        />
		      </CardView>
		    </Container>
		    <Container styling='transparent' noPadding>
		      <CardView width='1-1' type="no-bg" style={styles.tokenHolder} noPadding>
		        <div className="settings-collapse">
		          <Collapse>
		            <Panel header={`OAuth Settings`} showArrow>
		              <Container styling='transparent' noPadding>
		                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
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
		                    content={app.oauth.callback_url == '' ? 'https://' : app.oauth.callback_url}
		                    canCopy
		                    onSave={(value) => { actions.saveOAuthCallback(index, value) }}
		                  />
		                </CardView>
		              </Container>
		              <Container styling='transparent' noPadding>
		                <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
		                  <TextView text={`OAuth Scopes: `}
		                    heading={4}
		                    align={`left`} 
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
		              </Container>
		            </Panel>
		            <Panel header={`Webhook Settings`} showArrow>
		              <Container styling='transparent' noPadding>
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
		              </Container>
		            </Panel>
		          </Collapse>
		        </div>
		      </CardView>
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