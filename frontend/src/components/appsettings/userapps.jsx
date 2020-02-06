import PropTypes from 'prop-types'
import React from 'react'

// Components
import { ButtonView, CardView, Column, Demo, Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

import AuthAppRow from './authapprow.jsx'

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

class UserApps extends React.Component {
  render () {
    const { authorised_apps } = this.props
    authorised_apps.map((app, i) => { console.log(app); })

    return <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100vh`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `50px` }} >
            
            <TextView text={`Account`} heading={2} align={`left`} style={styles.title}/>
            
            <CardView width='1-1' type='default' noPadding>
               <Row height='fit-content' noPadding style={{ padding : `20px`}}>
                  <Column width='1-1' horizontalAlignment='center' >
                    <TextView text={this.props.fullname} heading={2} align={`left`} style={styles.noPadding}/>
                    <TextView text={this.props.department} heading={3} align={`left`} style={styles.noPadding}/>
                  </Column>
                </Row>
            </CardView>

            <TextView text={`Permissions`} heading={2} align={`left`} style={styles.title}/>
            
            <CardView width='1-1' type='default' noPadding>
              <Row height='40px' noPadding style={{ padding : `40px 0`}}>
                <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
                  {authorised_apps.length===0 ? (
                        <>
                          <TextView text={`No authorised apps, download UCL Assistant to get started:`} 
                            heading={3}
                            align={`center`}
                            style={styles.noPadding}
                          />
                          <ButtonView text="Download"
                            type="alternate"
                            link={`https://play.google.com/store/apps/details?id=com.uclapi.uclassistant&hl=en_GB`}
                            style={{marginBottom: 0}}
                          />
                        </>
                    ) : (
                      <>
                        {authorised_apps.map((app, i) => 
                          <>
                            <CardView width='1-2' type="transparent" noShadow>
                              <TextView text={app.app.name} 
                                heading={3}
                                align={`left`}
                                style={styles.noPadding}
                              />
                              <TextView text={app.app.creator.name} 
                                heading={3}
                                align={`left`}
                                style={styles.noPadding}
                              />
                            </CardView>
                            <CardView width='1-2' type="transparent" noShadow>
                              <ButtonView 
                                type="alternate"
                                onClick={() => { this.handleChange(app.app.client_id) } } 
                                text={app.active ? "Revoke Permissions" : "App Disabled"}
                              />
                            </CardView>
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

  handleChange (client_id) {
      // Add toast to confirm deauthorisation
      if(confirm('Are you sure you want to deauthorise this app?')){
        this.deauthoriseApp();
      }
  }

  deauthoriseApp(client_id) {
      // Call function in back end to delete scope
      axios.get('/oauth/deauthorise', {
        params: {
          client_id: client_id
        },
        xsrfHeaderName: "X-CSRFToken",
      }).then(response => {
          // Log success in console
          console.log("Successfully de-authorised app: ")
          console.log(response)

          this.setState({
            isVisible: false,
          })
      }).catch(error => {
          // Handle error
          console.log(error);
      })
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string,
  department: PropTypes.string,
  authorised_apps: PropTypes.array,
}

export default UserApps
