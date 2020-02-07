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

    this.handleChange = this.handleChange.bind(this)
    this.deauthoriseApp = this.deauthoriseApp.bind(this)

    const { authorised_apps } = this.props
    const isDeleted = []
    authorised_apps.map(() => { isDeleted.push(false) })

    this.state = {
      isDeleted: isDeleted,
    }
  }

  render () {
    const { authorised_apps } = this.props
    const { isDeleted } = this.state

    let appCount = 0
    authorised_apps.map((app) => { if(app.active) {appCount ++} })
    const isApps = appCount===0

    return <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100vh`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `50px` }} >
            
            <TextView text={`Account`} heading={2} align={`left`} style={styles.title}/>
            
            <CardView width='1-1' type='default' noPadding>
               <Row height='fit-content' noPadding style={{ padding : `20px`}}>
                  <Column width='1-1' horizontalAlignment='center' >
                    <TextView text={this.props.fullname} heading={2} align={`left`} style={styles.noPadding}/>
                    <TextView text={this.props.department} heading={4} align={`left`} style={styles.noPadding}/>
                  </Column>
                </Row>
            </CardView>

            <TextView text={`Permissions`} heading={2} align={`left`} style={styles.title}/>
            
            <CardView width='1-1' type='default' noPadding>
              <Row noPadding>
                <Column width='1-1' horizontalAlignment='center'>
                  {isApps ? (
                        <>
                          <TextView text={`No authorised apps, download UCL Assistant to get started:`} 
                            heading={2}
                            align={`center`}
                            style={styles.noPadding}
                          />
                          <ButtonView text="Download"
                            type="alternate"
                            link={`https://play.google.com/store/apps/details?id=com.uclapi.uclassistant&hl=en_GB`}
                            style={{marginBottom: 0,
cursor: `pointer`}}
                          />
                        </>
                    ) : (
                      <>
                        {authorised_apps.map((app, i) => 
                          <>
                            {app.active && !isDeleted[i] ? (
                              <>
                                <div className="default tablet">
                                  <CardView width='1-2' type="transparent" noShadow>
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
                                  <CardView width='1-2' type="transparent" noShadow>
                                    <ButtonView 
                                      type="alternate"
                                      onClick={() => { this.handleChange(app.app.client_id, i) } } 
                                      text={`Revoke Permissions`}
                                      style={{ float: `right`,
cursor: `pointer` }}
                                    />
                                  </CardView>
                                </div>
                                <div className="mobile">
                                  <CardView width='1-1' type="transparent" noShadow>
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
                                  <CardView width='1-1' type="transparent" noShadow>
                                    <ButtonView 
                                      type="alternate"
                                      onClick={() => { this.handleChange(app.app.client_id, i) } } 
                                      text={`Revoke Permissions`}
                                      style={{cursor: `pointer`}}
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
  }

  handleChange (client_id, index) {
      const { authorised_apps } = this.props

      // Add toast to confirm deauthorisation
      if(confirm(`Are you sure you want to deauthorise ` + authorised_apps[index].app.name + `? WARNING: You will `
       + `need to re-authenticate with the app independently from this page` )){
        this.deauthoriseApp(client_id, index)
      }
  }

  deauthoriseApp(client_id, index) {
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
