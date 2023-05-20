/* eslint-disable react/jsx-no-bind */
// Stylings
import { styles as dashboardStyles } from '@/components/layout/data/dashboard_styles.jsx'
// Components
import {
  CheckBox, AnalyticInfo, AnalyticUserInfo,
  Column, Container, Field, Row,
} from '@/components/layout/Items.jsx'
// External dependencies
import {Button, Panel, PanelGroup } from "rsuite";

import React from "react";
import styles from '@/styles/Dashboard.module.scss'
import AccordionIcon from './AccordionIcon.jsx'

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

    const updated = this.timeSince(new Date(app.updated + `Z`))
    const created = this.timeSince(new Date(app.created + `Z`))

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

      const updated = this.timeSince(new Date(app.updated + `Z`))
      const created = this.timeSince(new Date(app.created + `Z`))

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

    return (
    <PanelGroup accordion className='multi-wrapper'>
      <Panel header={app.name} className={styles.panel}>
        <Container noPadding>
          <Row width="1-1">
            <Column
              width="1-1"
              className="title-holder"
            >
              <Field
                title="Title"
                content={app.name}
                onSave={(value) => { actions.renameProject(index, value) }}
                isSmall
              />
              <Field
                title="API Token"
                content={app.token}
                canCopy
                onRefresh={ () => { actions.regenToken(index) } }
              />
            </Column>
          </Row>

          <Container noPadding>
            <Column
              width='1-1'
              noPadding
            >
              <PanelGroup accordion className='narrow'>
                <Panel header={`OAuth Settings`} className={`narrow ${styles.panel} ${styles.subPanel}`}>
                  <Container noPadding>
                    <Column
                      width='1-1'
                      className={styles.settingsSection}
                      >
                      <h3>
                        OAuth Credentials:
                      </h3>
                      <Field
                        title="Client ID"
                        content={app.oauth.client_id}
                        canCopy
                      />
                      <Field
                        title="Client Secret"
                        content={app.oauth.client_secret}
                        canCopy
                      />
                      <Field
                        title="Callback URL"
                        content={app.oauth.callback_url == ``
                          ? `https://`
                          : app.oauth.callback_url}
                        canCopy
                        onSave={(value) => actions.saveOAuthCallback(index, value)}
                      />
                    </Column>
                  </Container>
                  <Container noPadding>
                    <Column
                      width='1-1'
                      className={styles.settingsSection}
                    >
                      <h4>OAuth Scopes:</h4>
                      {app.oauth.scopes.map( (scope, scope_index) =>
                        <CheckBox
                          key={scope_index}
                          text={scope.description}
                          isChecked={scope.enabled}
                          onClick={(value) => actions.setScope(
                            index, scope_index, value
                            )
                          }
                        />
                      )}
                    </Column>
                  </Container>
                </Panel>
                <Panel header={`Analytics`} className={`narrow ${styles.panel} ${styles.subPanel}`}>
                  <Container noPadding>
                    <Column width='1-1'>
                      {[`requests`, `remaining_quota`].map((analytic, analytic_index) =>
                        <AnalyticInfo
                          key={analytic_index}
                          analytic={analytic}
                          value={app.analytics[analytic]}
                        />
                      )}
                      <AnalyticUserInfo
                        users={app.analytics.users}
                        usersPerDept={app.analytics.users_per_dept}
                      />
                    </Column>
                  </Container>
                </Panel>
              </PanelGroup>
            </Column>
          </Container>
          <Container noPadding>
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
                <p style={dashboardStyles.dates}>Created: {created} ago</p>
                <p style={dashboardStyles.dates}>Updated: {updated} ago</p>
              </Column>

              <Button
                color='red'
                appearance='primary'
                onClick={() => { actions.deleteConfirm(index) }}
              >
                Delete
              </Button>
            </Column>
          </Container>
        </Container>
        </Panel>
      </PanelGroup>
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
