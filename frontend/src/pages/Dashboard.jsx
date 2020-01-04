import 'Styles/common/uclapi.scss'

import dayjs from 'dayjs'
import React from 'react'
import ReactDOM from 'react-dom'

// Components
import { CardView, Column,
  Footer, NavBar, Row, TextView } from 'Layout/Items.jsx'

const styles = {
  baseText: {
    color: `white`,
    fontWeight: `300`,
  },
  lightText: {
    color: `#ddd`,
    fontWeight: `100`,
  },
  dates: {
    color: `#ddd`,
    fontWeight: `100`,
    margin: `0`,
  },
  appHolder: {
    marginTop: `80px`,
  },
  tokenHolder: {
    borderRadius: `0`,
  },
  tokenCopyField: {
    marginTop: `0`,
    width: `50%`,
    padding: `15px`,
    textAlign: `left`,
  },
  tokenText: {
    float: `left`,
    margin: `6px 10px 0 0`,
    color: `white`,
    fontWeight: `300`,
  },
}

class Dashboard extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

    this.timeSince = this.timeSince.bind(this)

    // Sort the apps by last updated property
    window.initialData.apps.sort((a, b) => {
      const dateA = dayjs(a.created)
      const dateB = dayjs(b.created)

      if (dateA.isBefore(dateB)) {
        return -1
      } else if (dateB.isBefore(dateA)) {
        return 1
      } else {
        return 0
      }
    })

    this.state = { data: window.initialData }
  }
  render() {
    const { data: { name, cn, apps } } = this.state 

    return (
      <>
        <NavBar isScroll={false} />

        <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100%`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `80px` }}>
            <TextView text={`Welcome, ` + name}
              heading={1}
              align={`left`} 
              style={styles.baseText}
            />
            <TextView text={`Your username is: ` + cn}
              heading={2}
              align={`left`} 
              style={styles.lightText}
            />

            <div className="app-holder" style={styles.appHolder}>
              {apps.map( (app, index) => {
                const updated = this.timeSince(new Date(app.updated))
                const created = this.timeSince(new Date(app.updated))

                return (
                  <CardView width='1-1' minWidth='280px' type='default' key={index} noPadding>
                    <Row styling='transparent' noPadding>
                      <CardView width='1-2' minWidth="100px" type="no-bg" snapAlign>
                        <TextView text={app.name}
                          heading={3}
                          align={`left`} 
                          style={styles.baseText}
                        />
                      </CardView>
                      <CardView width='1-2' minWidth="100px" type="no-bg" snapAlign>
                        <TextView text={`Created: ` + created + ` ago`}
                          heading={5}
                          align={`right`} 
                          style={styles.dates}
                        />
                        <TextView text={`Updated: ` + updated + ` ago`}
                          heading={5}
                          align={`right`}
                          style={styles.dates}
                        />
                      </CardView>
                    </Row>
                    <Row styling='transparent' noPadding>
                      <CardView width='1-1' type="no-bg" style={styles.tokenHolder}>
                        <TextView text={`API Token:`} heading={3} align={`left`} style={styles.tokenText} />
                        <input type="text" className="token-input" readOnly value={app.token} style={styles.tokenCopyField}/>
                      </CardView>
                    </Row>
                  </CardView>
                  )
              }
              )}
            </div>
          </Column>
        </Row>

        <Footer />
      </>
    )
  }

  timeSince(date) {
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

ReactDOM.render(
  <Dashboard />,
  document.querySelector(`.app`)
)
