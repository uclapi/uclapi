import axios from 'axios'
// UCL Assistant splash screen
import uclassistantmarket from 'Images/home-page/uclassistantmarket.png'
// Components
import {
  ButtonView, CardView, Column,
  Container, ImageView,
  Row, TextView,
} from 'Layout/Items.jsx'
import PropTypes from 'prop-types'
import React from 'react'
import { useHistory } from 'react-router-dom'

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

    const cardPadding = `30px`

    return (
      <Container
        height='fit-content'
        styling='splash-parallax'
        style={{ minHeight: `100vh` }}
      >
        <Row
          width='9-10'
          horizontalAlignment='center'
          style={{ marginTop: `50px` }}
        >

          {/* Personal account details*/}

          <TextView
            text={`Account`}
            heading={1}
            align={`left`}
            style={styles.title}
          />

          <CardView width='1-1' type='default' noPadding style={{ padding: 0 }}>
            <Container noPadding>
              <Row width='1-1' horizontalAlignment='center' >
                <CardView
                  width='6-10'
                  type="transparent"
                  noShadow
                  keepInline
                  style={{ padding: cardPadding }}
                  noPadding
                >
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
                </CardView>
                <CardView
                  width='4-10'
                  type="transparent"
                  noShadow
                  keepInline
                  noPadding
                  style={{ padding: cardPadding }}
                >
                  <ButtonView
                    type="alternate"
                    link={`/logout`}
                    text={`Logout`}
                    style={{
                      float: `right`,
                      cursor: `pointer`,
                    }}
                  />
                </CardView>
              </Row>
            </Container>
          </CardView>

          <TextView
            text={`Permissions`}
            heading={1}
            align={`left`}
            style={styles.title}
          />

          {/* Authorised app details */}

          <CardView
            width='1-1'
            type='default'
            noPadding
            style={{ padding: 0 }}
          >
            {isApps ? (

              /* No apps authorised - suggest ucl assistant */

              <Container
                noPadding
              >
                <Row width='1-1'
                  horizontalAlignment='center'
                  style={{
                    paddingTop: 20,
                    paddingBottom: 20,
                  }}
                >
                  <Column width="1-2" className="default">
                    <ImageView
                      src={uclassistantmarket}
                      width="367px"
                      height="405px"
                      description="ucl asssitant screen shot"
                      centred
                    />
                  </Column>
                  <Column width="1-2" alignItems="column">
                    <TextView
                      text="No authorised apps yet. Try UCL Assistant?"
                      heading="2"
                      align="left"
                    />
                    <TextView
                      text={`UCL Assistant is a productivity app for students and staff at UCL. `
                        + `It has been designed by students to be as reliable and user friendly `
                        + `as possible.`}
                      align="left"
                      heading="5"
                    />
                    <TextView
                      text={`The app has many different features but one of our favourites is `
                        + `the ability to view your timetable in a weekly view. The app highlights your`
                        + `current commitments to save you time as you rush about University. Check it out below!`}
                      align="left"
                      heading="5"
                    />
                    <ButtonView text="Download"
                      type="alternate"
                      link={`/marketplace/uclassistant`}
                      centred
                      containerStyles={{
                        marginTop: `20px`,
                        marginBottom: 0,
                      }}
                    />
                  </Column>
                </Row>
              </Container>
            ) : (

                /* Some apps authorised - display apps */

                <Container noPadding>
                  <Row width='1-1'
                    horizontalAlignment='center'
                    style={{
                      paddingTop: 20,
                      paddingBottom: 20,
                    }}
                    alignItems="column"
                  >
                    {authorised_apps.map((app, i) =>
                      <>
                        {app.active && !isDeleted[i] ? (
                          <Row width="1-1">
                            <CardView
                              width='1-2'
                              type="transparent"
                              noShadow
                              keepInline
                              style={{ padding: cardPadding }}
                              noPadding
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
                              keepInline
                              style={{ padding: cardPadding }}
                              noPadding
                            >
                              <ButtonView
                                type="alternate"
                                onClick={
                                  this.handleChange(app.app.client_id, i)
                                }
                                text={`Revoke Permissions`}
                                style={{
                                  cursor: `pointer`,
                                  float: `right`,
                                }}
                              />
                            </CardView>
                          </Row>
                        ) : null}
                      </>
                    )}
                  </Row>
                </Container>
              )}
          </CardView>
        </Row>
      </Container>
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

  logout = () => {
    if (confirm(`Are you sure you want to logout`)) {
      const path = `/logout`
      const history = useHistory()
      history.push(path)
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
