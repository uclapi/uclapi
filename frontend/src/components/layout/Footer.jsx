import React from 'react'

// Social Media
import facebook from 'Images/home-page/facebook.png'
import github from 'Images/home-page/github.png'
// UCL API Logo
import twitter from 'Images/home-page/twitter.png'
// Common Components
import { CardView, Column, ImageView, Row } from 'Layout/Items.jsx'

export default class Footer extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    const logosize = `20px`

    return (
      <Row styling='secondary' style={{ padding: `20px 0` }}>
        <Column width='1-1' horizontalAlignment='center' className="column-horizontal">
          <CardView width='1-3' type='github' link='https://github.com/uclapi'>
            <ImageView src={github} width={logosize} height={logosize} description={`github logo`} isCentered />
          </CardView>

          <CardView width='1-3' type='facebook' link='https://www.facebook.com/uclapi/'>
            <ImageView src={facebook} width={logosize} height={logosize} description={`facebook logo`} isCentered />
          </CardView>

          <CardView width='1-3' type='twitter' link='https://twitter.com/uclapi'>
            <ImageView src={twitter} width={logosize} height={logosize} description={`twitter logo`} isCentered />
          </CardView>
        </Column>
      </Row >
    )
  }

}