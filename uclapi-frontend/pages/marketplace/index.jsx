/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types


import "react-responsive-carousel/lib/styles/carousel.min.css"
import styles from "@/styles/Marketplace.module.scss"

// Grab titles and descriptions of app
import { allApps } from '@/components/layout/data/app_pages.jsx'
// Common Components
import {
  CardView, Container,
  Row
} from '@/components/layout/Items.jsx'
// Standard React imports
import React from 'react'
import Image from "next/image";

class Marketplace extends React.Component {
  constructor(props) {
    super(props)
    const DEBUGGING = false

    if (DEBUGGING) { console.log(`All apps loaded in: ` + allApps) }

    // Set up the 'featured' apps section
    const featuredApps = []
    featuredApps.push(allApps[`uclassistant`]);

    // Segregate into groups of applications if needed
    const appsToRender = []
    appsToRender.push(allApps[`unikomet`])
    appsToRender.push(allApps[`uclcssa`])
    appsToRender.push(allApps[`uclassistant`])

    this.state = {
      'featuredApps': featuredApps,
      'appsToRender': appsToRender,
    }
  }

  render() {
    const iconsize = 100
    // const logosize = `150px`
    const {
      featuredApps,
      appsToRender,
    } = this.state

    return (
      <>
        <Container
          height='300px'
          style={{ margin: `60px 0 0 0` }}
          styling='splash-parallax'
        >
          <Row
            width='1-1'
            maxWidth='1000px'
            horizontalAlignment='center'
            verticalAlignment='center'
            alignItems='column'
          >
            <h1>UCL Marketplace</h1>
            <h2>Apps that use UCL API</h2>
          </Row>
        </Container>

        <Container
          styling='secondary'
          heading="Featured App"
        >
          <Row
            width='1-1'
            maxWidth='1000px'
            horizontalAlignment='center'
          >
            {featuredApps.map((app, i) => {
              return (
                <CardView
                  key={`featured-app-` + i}
                  width={`1-1`}
                  type={`emphasis`}
                  link={`/marketplace/` + app.id}
                >
                  <Row
                    width='1-2'
                    horizontalAlignment='center'
                    alignItems='column'
                  >
                    <Image
                      src={app.logolight}
                      width={iconsize}
                      height={iconsize}
                      style={{margin: '20px auto'}}
                    />
                    <h2>{app.name}</h2>
                    <p>{app.description}</p>
                  </Row>
                </CardView>
              )
            })}
          </Row>
        </Container>

        <Container
          styling='splash-parallax'
          heading="All Apps"
        >
          <Row
            width='1-1'
            maxWidth='1000px'
            horizontalAlignment='center'
          >
            {appsToRender.map((app, i) => {
              return (
                <CardView
                  key={`all-apps-` + i}
                  width={`1-2`}
                  type={`alternate`}
                  link={`/marketplace/` + app.id}
                  style={{
                    float: `left`,
                  }}
                >
                  <Row
                    width="9-10"
                    horizontalAlignment="center"
                    alignItems="column"
                  >
                    <Image
                      src={app.logolight}
                      width={iconsize}
                      height={iconsize}
                      style={{margin:'20px auto'}}
                    />
                    <h2 className={styles.app}>{app.name}</h2>
                    <p className={styles.app}>
                      {app.description}
                    </p>
                  </Row>
                </CardView>
              );
            })}
          </Row>
        </Container>
      </>
    )
  }
}

export default Marketplace
