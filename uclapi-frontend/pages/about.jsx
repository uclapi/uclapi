// Team descriptions
import { current, previous } from '@/data/team_members'
// Common Components
import {
  CardView, Column, Container,
  Row,
} from '@/components/layout/Items.jsx'
import PropTypes from 'prop-types'
import React from 'react';



const member = ({ github, name, image, title }) => (
  <CardView
    width='1-6'
    type='emphasis'
    link={github}
    style={{ padding: 0 }}
  >
    <Container height='300px'>
      <Column width='1-1' horizontalAlignment='center' style={{ padding: 0 }}>
        <h2>{name}</h2>
        <Container
          height='100px'
          src={image}
          style={{ backgroundSize: `Cover` }}
        ></Container>
        <Container height='30px' style={{ padding: `20px 0` }}>
          <Column
            width='1-1'
            horizontalAlignment='center'
            verticalAlignment='center'
          >
            <h6>{title}</h6>
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
        {/* About us - Landing page */}

        <Container height='600px' styling='team-parallax'>
          <Row
            width='2-3'
            horizontalAlignment='center'
            verticalAlignment='center'
            alignItems='column'
          >
            <h1>
              About Us
            </h1>
            <h2>
              UCL API is a student led project, founded by Wilhelm Klopp,
              that opens up the massive amount of data collected by UCL.
              This allows UCL alumni and staff to develop apps with UCL data
            </h2>
          </Row>
        </Container>

        {/* Current team */}

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

        {/* Alumni */}

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
      </>
    )
  }
}



export default AboutPage
