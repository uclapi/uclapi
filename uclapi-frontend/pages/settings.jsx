import {
  CardView,
  Column,
  Container,
  Row,
} from "@/components/layout/Items.jsx";
import React, { useCallback, useState, useEffect } from "react";
import Api from "@/lib/Api";
import Image from "next/image";
import { Button } from "rsuite";
import styles from "@/styles/Settings.module.scss";

const AppSettings = () => {
  const [data, setData] = useState({
    fullname: ``,
    department: ``,
    apps: [],
  })

  const fetchSettings = () =>
    Api.settings.getSettings().then(data => setData(data))

  useEffect(() => {
    fetchSettings()
  }, [])

  const { fullname, department, apps: authorisedApps } = data
  const appCount = authorisedApps.filter(app => app.active).length
  const isApps = appCount === 0

  const cardPadding = `30px`

  const deauthoriseApp = useCallback(async (clientId) => {
    await Api.settings.deauthoriseApp(clientId).then(() => fetchSettings())
  }, [])

  const handleChange = useCallback((client_id, index) => () => {
    const deauthoriseConfirmation = `Are you sure you want to deauthorise `
      + authorisedApps[index].app.name + `? It will probably stop working and `
      + `you'll need to re-authenticate with it again if you want to use it`
    if (confirm(deauthoriseConfirmation)) {
      deauthoriseApp(client_id)
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
        <h1 className={styles.title}>
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
                <h2 className={styles.noPadding}>{fullname}</h2>
                <h4 className={styles.noPadding}>{department}</h4>
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

        <h1 className={styles.title}>
          Permissions
        </h1>
        <CardView
          width='1-1'
          type='default'
          noPadding
          style={{ padding: 0 }}
        >
          {isApps ? (
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
                      {app.active ? (
                        <Row width="1-1">
                          <CardView
                            width='1-2'
                            type="transparent"
                            noShadow
                            keepInline
                            style={{ padding: cardPadding }}
                            noPadding
                          >
                            <h2 className={styles.noPadding}>
                              {app.app.name.toUpperCase()}
                            </h2>
                            <h4 className={styles.noPadding}>
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

export default AppSettings
