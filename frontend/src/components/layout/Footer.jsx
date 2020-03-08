import React from 'react'

// Social Media
import facebook from 'Images/home-page/facebook.png'
import github from 'Images/home-page/github.png'
// UCL API Logo
import twitter from 'Images/home-page/twitter.png'
// Common Components
import { CardView, Column, ImageView, Container } from 'Layout/Items.jsx'

export default class Footer extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    const logosize = `20px`

    return (
      <Container 
        styling='secondary' 
        height="80px"
        noPadding
        style={{ paddingTop: `20px` }}
      >
        <div className="social-media-holder">
          <a href="https://github.com/uclapi">
            <div className="uclapi-card-github" style={{ width: logosize, height: logosize}} >
              <ImageView src={github} width={logosize} height={logosize} description={`github logo`} isCentered />
            </div>
          </a>

          <a href="https://www.facebook.com/uclapi/">
            <div className="uclapi-card-facebook" style={{ width: logosize, height: logosize}} >
              <ImageView src={facebook} width={logosize} height={logosize} description={`facebook logo`} isCentered />
            </div>
          </a>

          <a href="https://twitter.com/uclapi">
            <div className="uclapi-card-twitter" style={{ width: logosize, height: logosize}} >
              <ImageView src={twitter} width={logosize} height={logosize} description={`twitter logo`} isCentered />
            </div>
          </a>
        </div>
      </Container >
    )
  }

}