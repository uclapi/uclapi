import warning from 'Images/warning/warning.svg'
import {
  Button,
  Column,
  Container,
  Footer,
  ImageView,
  NavBar,
  Row,
  TextView,
} from 'Layout/Items.jsx'
import React from 'react'
import 'Styles/common/uclapi.scss'
import 'Styles/navbar.scss'

const Warning = ({ title, content }) => (
  <>
    <NavBar isScroll={false} />

    {/* Warning message */}

    <Container styling="splash-parallax" height="600px">
      <Row 
        width="2-3"
        horizontalAlignment="center"
        verticalAlignment="center"
      >
        
        <Column width="1-2" className="default">
          <ImageView
            src={warning}
            width="367px"
            height="405px"
            description="large exclamation point, warning!"
          />
        </Column>

        <Column width="1-2" alignItems="column">
          <TextView 
            heading="1"
            text={title}
            align="left"
          />
          {typeof content === `string`
            ? (
              <TextView 
                heading="3"
                text={content}
                align="left"
              />
            )
            : content}
          <Button link={`/`} centred>
            Home
          </Button>
        </Column>
      </Row>
    </Container>
    <Footer />
  </>
)

export default Warning