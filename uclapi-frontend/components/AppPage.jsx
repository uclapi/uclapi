/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types


// Styles
// Grab titles and descriptions of app
import { allApps } from '@/components/layout/data/app_pages.jsx'
// Common Components
import {
  Button, CardView, Column, Container, ImageView,
  Row, TextView,
} from '@/components/layout/Items.jsx'
import React from 'react';
// Standard React imports

// External carousel dependency
import { Carousel } from "react-responsive-carousel"
import "react-responsive-carousel/lib/styles/carousel.min.css"


export class AppPage extends React.Component {
  constructor(props) {
    super(props)
    const { appId } = this.props
    console.log(allApps, appId)
    // Grab the app that this page is dealing with
    const app = allApps[appId]
    this.state = {
      'app': app,
      sizing: `default`,
    }
  }

  updateDimensions = () => {
    if (typeof (window) === `undefined`) {
      return null
    }
    const w = window,
      d = document,
      documentElement = d.documentElement,
      body = d.getElementsByTagName(`body`)[0],
      width = w.innerWidth || documentElement.clientWidth || body.clientWidth
      // height = w.innerHeight ||
      // documentElement.clientHeight || body.clientHeight

    const mobileCutOff = 992
    const tabletCutOff = 1130

    const { sizing } = this.state

    if (width > tabletCutOff) {
      if (sizing != `default`) { this.setState({ sizing: `default` }) }
    } else if (width > mobileCutOff) {
      if (sizing != `tablet`) { this.setState({ sizing: `tablet` }) }
    } else {
      if (sizing != `mobile`) { this.setState({ sizing: `mobile` }) }
    }

    console.log(sizing)
  }

  UNSAFE_componentWillMount() {
    setTimeout(this.updateDimensions, 50)
  }
  componentDidMount() {
    window.addEventListener(`resize`, this.updateDimensions)
  }
  componentWillUnmount() {
    window.removeEventListener(`resize`, this.updateDimensions)
  }

  render() {
    const {
      sizing,
      app: {
        logodark,
        name,
        description,
        screenshots,
        detailedDescription,
        links,
      },
    } = this.state

    const isMobile = sizing == `mobile`

    const contentWidth = isMobile ? `9-10` : `2-3`
    const iconsize = isMobile ? `50px` : `100px`

    const screenshotwidth = isMobile ? `162px` : `216px`
    const screenshotheight = isMobile ? `258px` : `384px`
    const holderWidth = isMobile ? `162px` : `648px`

    return (
      <>
        <Container styling='splash-parallax'>
          <Row
            width={isMobile ? `9-10` : `2-3`}
            horizontalAlignment='center'
          >
            {isMobile ? (
              <>
                <Container styling='transparent'
                  height={`115px`}
                  noPadding
                  style={{
                    padding: `30px 0px 10px`,
                    marginBottom: `20px`,
                  }}
                >
                  <CardView
                    type='default'
                    width={`1-1`}
                    style={{ padding: `10px 0` }}
                    noPadding
                  >
                    <ImageView
                      src={logodark}
                      width={iconsize}
                      height={iconsize}
                      description={name + `logo`}
                      centred
                    />
                    <TextView text={name} heading={2} />
                  </CardView>
                </Container>
                <Container styling='transparent'
                  height={`100px`}
                  noPadding
                  style={{ padding: `0 0 30px 0` }}
                >
                  <Row
                    width='1-1'
                    horizontalAlignment='center'
                    verticalAlignment='center'
                  >
                    {links.map((x, key) => (
                      <Container height="50px" noPadding key={key}>
                        <Row
                          width='2-3'
                          horizontalAlignment='center'
                        >
                          <Button
                            link={x.link}
                            type={`alternate`}
                            key={key}
                            centred
                            style={{ width: `100px` }}
                          >
                            {x.name}
                          </Button>
                        </Row>
                      </Container>
                    ))}
                  </Row>
                </Container>
              </>
            ) : (
                <>
                  <Container styling='transparent' height='140px'>
                    <Row
                      width='1-1'
                      horizontalAlignment='center'
                      verticalAlignment='center'
                    >
                      <Column
                        width='fit-content'
                        minWidth={iconsize}
                        typeOfInline='grid'
                        horizontalAlignment='left'
                      >
                        <ImageView
                          src={logodark}
                          width={iconsize}
                          height={iconsize}
                          description={name + `logo`}
                          centred
                          style={{ 'margin': `0 auto 0 0` }}
                        />
                      </Column>
                      <Column
                        width="auto"
                        horizontalAlignment='left'
                        textAlign='left'
                        style={{
                          paddingLeft: `20px`,
                          flexDirection: `column`,
                        }}
                      >
                        <TextView text={name} heading={2} align="left" />
                        <TextView text={description} heading={5} align="left" />
                      </Column>
                      <Column
                        width='fit-content'
                        horizontalAlignment='left'
                        textAlign='left'
                        style={{ "paddingLeft": `20px` }}
                      >
                        {links.map((x, key) => (
                          <Container
                            height="50px"
                            noPadding
                            key={x.name}
                            style={{ minHeight: `unset` }}
                          >
                            <Button
                              link={x.link}
                              type={`alternate`}
                              key={key}
                              style={{
                                margin: `0`,
                                width: `75px`,
                              }}
                            >
                              {x.name}
                            </Button>
                          </Container>
                        ))}
                      </Column>
                    </Row>
                  </Container>
                </>
              )}
            <CardView width="1-1" noPadding style={{ padding: `20px 0` }}>
              <div className="screenshot-holder"
                style={{
                  width: holderWidth,
                  margin: `auto`,
                }}
              >
                <Carousel
                  showThumbs={false}
                  centerMode={!isMobile}
                  centerSlidePercentage={isMobile ? 100 : 33.33}
                  showArrows
                  showIndicators
                  showStatus
                  infiniteLoop
                >
                  {screenshots.map((screenshot) => (
                    <div key={screenshot.img}>
                      <img
                        src={screenshot.img}
                        width={screenshotwidth}
                        height={screenshotheight}
                      />
                      <p className="legend">{screenshot.name}</p>
                    </div>
                  ))}
                </Carousel>
              </div>
              <Row
                width={contentWidth}
                horizontalAlignment='center'
                textAlign='left'
              >
                {detailedDescription}
              </Row>
            </CardView>
          </Row>
        </Container>
      </>
    )
  }

}
