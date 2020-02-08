import axios from 'axios'
import PropTypes from 'prop-types'
import React from 'react'

// Components
import { ButtonView, CardView, Column, Row, TextView } from 'Layout/Items.jsx'

const styles = {
  noPadding: {
    marginBottom: 0,
    marginLeft: 0,
  },
  title: {
    marginLeft: 0,
    margin: `20px 0`,
  },
}

class SettingsLayout extends React.Component {
  static propTypes = {
    fullname: PropTypes.string,
    department: PropTypes.string,
    authorised_apps: PropTypes.array,
  }

  constructor(props) {
    super(props)
    const { authorised_apps } = this.props
    this.state = {
      isDeleted: authorised_apps.map(() => false),
    }
  }

  render() {
    const { authorised_apps, fullname, department } = this.props
    const { isDeleted } = this.state

    const appCount = authorised_apps.reduce(
      (prev, curApp) => curApp.active ? (prev + 1) : prev,
      0
    )
    const isApps = appCount === 0

    return (
      <Row
        height='fit-content'
        styling='splash-parallax'
        style={{ minHeight: `100vh` }}
      >
        <Column
          width='2-3'
          horizontalAlignment='center'
          style={{ marginTop: `50px` }}
        >

          <TextView
            text={`Account`}
            heading={2}
            align={`left`}
            style={styles.title}
          />

          <CardView width='1-1' type='default' noPadding>
            <Row height='fit-content' noPadding style={{ padding: `20px` }}>
              <Column width='1-1' horizontalAlignment='center' >
                <TextView
                  text={fullname}
                  heading={2}
                  align={`left`}
                  style={styles.noPadding}
                />
                <TextView
                  text={department}
                  heading={4}
                  align={`left`}
                  style={styles.noPadding}
                />
              </Column>
            </Row>
          </CardView>

          <TextView
            text={`Permissions`}
            heading={2}
            align={`left`}
            style={styles.title}
          />

          <CardView width='1-1' type='default' noPadding>
            <Row noPadding>
              <Column width='1-1'
                horizontalAlignment='center'
                style={{
                  paddingTop: 20,
                  paddingBottom: 20,
                }}
              >
                {isApps ? (
                  <>
                    <TextView
                      text={`No authorised apps yet. Try UCL Assistant?`}
                      heading={2}
                      align={`center`}
                      style={styles.noPadding}
                    />
                    <ButtonView text="Download"
                      type="alternate"
                      link={`/marketplace/uclassistant`}
                      style={{
                        marginBottom: 0,
                        cursor: `pointer`,
                      }}
                    />
                  </>
                ) : (
                    <>
                      {authorised_apps.map((app, i) =>
                        <>
                          {app.active && !isDeleted[i] ? (
                            <>
                              <div className="default tablet">
                                <CardView
                                  width='1-2'
                                  type="transparent"
                                  noShadow
                                >
                                  <TextView text={app.app.name.toUpperCase()}
                                    heading={2}
                                    align={`left`}
                                    style={styles.noPadding}
                                  />
                                  <TextView text={app.app.creator.name}
                                    heading={4}
                                    align={`left`}
                                    style={styles.noPadding}
                                  />
                                </CardView>
                                <CardView
                                  width='1-2'
                                  type="transparent"
                                  noShadow
                                >
                                  <ButtonView
                                    type="alternate"
                                    onClick={
                                      this.handleChange(app.app.client_id, i)
                                    }
                                    text={`Revoke Permissions`}
                                    style={{
                                      float: `right`,
                                      cursor: `pointer`,
                                    }}
                                  />
                                </CardView>
                              </div>
                              <div className="mobile">
                                <CardView
                                  width='1-1'
                                  type="transparent"
                                  noShadow
                                >
                                  <TextView text={app.app.name.toUpperCase()}
                                    heading={2}
                                    align={`center`}
                                    style={styles.noPadding}
                                  />
                                  <TextView text={app.app.creator.name}
                                    heading={4}
                                    align={`center`}
                                    style={styles.noPadding}
                                  />
                                </CardView>
                                <CardView
                                  width='1-1'
                                  type="transparent"
                                  noShadow
                                >
                                  <ButtonView
                                    type="alternate"
                                    onClick={
                                      this.handleChange(app.app.client_id, i)
                                    }
                                    text={`Revoke Permissions`}
                                    style={{ cursor: `pointer` }}
                                  />
                                </CardView>
                              </div>
                            </>
                          ) : null}
                        </>
                      )}
                    </>
                  )}
              </Column>
            </Row>
          </CardView>
        </Column>
      </Row>
    )
  }

  handleChange = (client_id, index) => () => {
    const { authorised_apps } = this.props

    // Add toast to confirm deauthorisation
    const deauthoriseConfirmation = `Are you sure you want to deauthorise `
      + authorised_apps[index].app.name + `? It will probably stop working and `
      + `you'll need to re-authenticate with it again if you want to use it`
    if (confirm(deauthoriseConfirmation)) {
      this.deauthoriseApp(client_id, index)
    }
  }

  deauthoriseApp = (client_id, index) => {
    // Call function in back end to delete scope
    axios.get(`/oauth/deauthorise`, {
      params: {
        client_id: client_id,
      },
      xsrfHeaderName: `X-CSRFToken`,
    }).then(response => {
      // Log success in console
      console.log(`Successfully de-authorised app: `)
      console.log(response)

      const { isDeleted } = this.state
      isDeleted[index] = true

      // Update react to no longer render this app
      this.setState({
        isDeleted: isDeleted,
      })
    }).catch(error => {
      // Handle error
      console.log(error)
    })
  }
}

export default SettingsLayout
