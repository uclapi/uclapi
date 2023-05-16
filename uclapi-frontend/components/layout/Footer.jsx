import { Container } from './Items.jsx'
import React from "react";
import Image from 'next/image'

export default class Footer extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    const logosize = 20

    return (
      <Container
        styling='secondary'
        height="80px"
        noPadding
        style={{ paddingTop: `20px` }}
      >
        <div className="social-media-holder">
          <a href="https://github.com/uclapi">
            <div className="uclapi-card-github"
              style={{ width: logosize,
height: logosize }}
            >
              <Image src={'/home-page/github.png'} width={logosize} height={logosize} />
            </div>
          </a>

          <a href="https://www.facebook.com/uclapi/">
            <div className="uclapi-card-facebook"
              style={{ width: logosize,
height: logosize }}
            >
              <Image src={'/home-page/facebook.png'} width={logosize} height={logosize}/>
            </div>
          </a>

          <a href="https://twitter.com/uclapi">
            <div className="uclapi-card-twitter"
              style={{ width: logosize,
height: logosize }}
            >
              <Image src={'/home-page/twitter.png'} width={logosize} height={logosize} />
            </div>
          </a>
        </div>
      </Container >
    )
  }

}
