import React from 'react'

import logo from 'Images/home-page/logo.svg'
// Common Components
import { Column, ImageView, Row, TextView } from 'Layout/Items.jsx'

export default class Footer extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    const iconsize = `100px`

    return (
      <Row styling={`secondary`} height={`fit-content`} >
        <Column width='1-2' horizontalAlignment='center'>
          <TextView text={`UCL API`} heading={1} align={`center`} />

          <TextView text={`github `} heading={5} align={`center`} style={{ 'display': `inline-block` }} link={`https://github.com/uclapi/uclapi`} />
          <TextView text={`-`} heading={5} align={`center`} style={{ 'display': `inline-block` }} />
          <TextView text={` twitter`} heading={5} align={`center`} style={{ 'display': `inline-block` }} link={`https://twitter.com/uclapi?lang=en`} />
          <TextView text={`-`} heading={5} align={`center`} style={{ 'display': `inline-block` }} />
          <TextView text={` facebook`} heading={5} align={`center`} style={{ 'display': `inline-block` }} link={`https://www.facebook.com/uclapi/`} />

          <ImageView src={logo} width={iconsize} height={iconsize} description={`ucl api logo`} isCentered />
        </Column>
      </Row>
    )
  }

}
