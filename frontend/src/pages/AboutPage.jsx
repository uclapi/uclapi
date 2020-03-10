// Standard React imports
// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

import PropTypes from 'prop-types'
import React from 'react'
import ReactDOM from 'react-dom'

// Team descriptions
import { current, previous } from 'Layout/data/team_members.jsx'
// Common Components
import { CardView, Column, Footer, NavBar, 
  Container, TextView, Row } from 'Layout/Items.jsx'

const member = ({ github, name, image, title }) => (
  <CardView 
    width='1-6'
    type='emphasis' 
    link={github} 
    style={{ padding: 0 }}
  >
    <Container height='300px' style={{ padding: `20px 0` }}>
      <Column width='1-1' horizontalAlignment='center' style={{ padding: 0 }}>
        <TextView text={name} heading={2} align={`center`} color={`white`} />
        <Container height='100px' src={image} style={{ backgroundSize: `Cover` }}></Container>
        <Container height='30px' style={{ padding: `20px 0` }}>
          <Column width='1-1' horizontalAlignment='center' verticalAlignment='center'>
            <TextView text={title} heading={6} align={`center`} color={`white`} />
          </Column>
        </Container>
      </Column>
    </Container>
  </CardView>
)

member.propTypes = {
  name: PropTypes.string,
  github: PropTypes.string,
  image: PropTypes.string,
  title: PropTypes.string,
}

class AboutPage extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      DEBUGGING: false,
    }
  }

  render() {
    return (
      <>
        <NavBar isScroll={false} />

        <Container height='600px' styling='team-parallax'>
          <Row 
            width='2-3' 
            horizontalAlignment='center' 
            verticalAlignment='center'
            alignItems='column'
          >
            <TextView text={`About Us`} heading={1} align={`center`} />
            <TextView text={`UCL API is a student led project, founded by Wilhelm Klopp, that opens up the massive amount of ` +
              `data collected by UCL. This allows UCL alumni and staff to develop apps with UCL data.`}
              heading={2}
              align={`center`}
            />
          </Row>
        </Container>

        <Container 
          styling='secondary'
          heading='Current Team'
        >
          <Row
            width='1-1'
            horizontalAlignment='center'
          >
            {current.map(x => member(x))}
          </Row>
        </Container>

        <Container 
          styling='team-parallax'
          heading='Alumni'
        >
          <Row
            width='1-1'
            horizontalAlignment='center'
          >
            {previous.map(x => member(x))}
          </Row>
        </Container>

        <Footer />

      </>
    )
  }
}

ReactDOM.render(
  <AboutPage />,
  document.querySelector(`.app`)
)
