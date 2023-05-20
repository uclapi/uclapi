
import {
  CardView, Column,
  Container, ImageView,
  Row,
} from '@/components/layout/Items.jsx'
import React, { useCallback , useState } from 'react'
import Api from '../../lib/Api'
import Image from 'next/image'
import {Button} from 'rsuite'

const styles = {
  noPadding: {
    marginBottom: 0,
    marginLeft: 0,
    textAlign: 'left'
  },
  title: {
    marginLeft: 0,
    margin: `20px 0`,
  },
}

const SettingsLayout = ({
  authorised_apps: authorisedApps,
  fullname,
  department,
}) => {
  const [isDeleted, setIsDeleted] = useState(authorisedApps.map(() => false))

  const appCount = authorisedApps.reduce(
    (prev, curApp) => curApp.active ? (prev + 1) : prev,
    0
  )
  const isApps = appCount === 0

  const cardPadding = `30px`

  const deauthoriseApp = useCallback(async (clientId, index) => {
    await Api.settings.deauthoriseApp(clientId)

    setIsDeleted([
      ...isDeleted.slice(0, index),
      true,
      ...isDeleted.slice(index + 1),
    ])
  }, [isDeleted])

  const handleChange = useCallback((client_id, index) => () => {
    // Add toast to confirm deauthorisation
    const deauthoriseConfirmation = `Are you sure you want to deauthorise `
      + authorisedApps[index].app.name + `? It will probably stop working and `
      + `you'll need to re-authenticate with it again if you want to use it`
    if (confirm(deauthoriseConfirmation)) {
      deauthoriseApp(client_id, index)
    }
  }, [deauthoriseApp, authorisedApps])


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

        <h1 style={styles.title}>
          Account
        </h1>

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
                <h2 style={styles.noPadding}>{fullname}</h2>
                <h4 style={styles.noPadding}>{department}</h4>
              </CardView>
              <CardView
                width='4-10'
                type="transparent"
                noShadow
                keepInline
                noPadding
                style={{ padding: cardPadding }}
              >
                <Button
                  href={`/logout`}
                  style={{
                    float: `right`,
                    cursor: `pointer`,
                  }}
                >
                  Logout
                </Button>
              </CardView>
            </Row>
          </Container>
        </CardView>

        <h1 style={styles.title}>
          Permissions
        </h1>

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
                  <Image
                    src={'/home-page/uclassistantmarket.png'}
                    width={367}
                    height={405}
                  />
                </Column>
                <Column width="1-2" alignItems="column">
                  <h2>
                    No authorised apps yet. Try UCL Assistant?
                  </h2>
                  <p className='description'>
                    UCL Assistant is a productivity app for
                    students and staff at UCL.
                    It has been designed by students to be as
                    reliable and user friendly as possible.
                  </p>
                  <p className='description'>
                    The app has many different features but one
                    of our favourites is
                    the ability to view your timetable in a weekly
                    view. The app highlights your current commitments
                    to save you time as you rush about University.
                    Check it out below!
                  </p>
                  <Button href={`/marketplace/uclassistant`}>
                    Download
                  </Button>
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
                  {authorisedApps.map((app, i) =>
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
                            <h2 style={styles.noPadding}>
                              {app.app.name.toUpperCase()}
                            </h2>
                            <h4 style={styles.noPadding}>
                              {app.app.creator.name}
                            </h4>
                          </CardView>
                          <CardView
                            width='1-2'
                            type="transparent"
                            noShadow
                            keepInline
                            style={{ padding: cardPadding }}
                            noPadding
                          >
                            <Button
                              onClick={handleChange(app.app.client_id, i)}
                              style={{
                                cursor: `pointer`,
                                float: `right`,
                              }}
                            >
                              Revoke Permissions
                            </Button>
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

export default SettingsLayout
