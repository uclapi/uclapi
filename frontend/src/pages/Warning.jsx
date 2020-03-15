// Standard React imports
// Styles
import 'Styles/common/uclapi.scss'
// Legacy
import 'Styles/navbar.scss'

// Images
import warning from 'Images/warning/warning.svg'

// Components
import {
  ButtonView,
  CardView,
  Column,
  Container,
  Demo,
  Footer,
  ImageView,
  NavBar,
  Row,
  TextView,
} from 'Layout/Items.jsx'
// External dependencies
import React from 'react'
import ReactDOM from 'react-dom'

class Warning extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      type: window.initialData.type,
    }
  }

  render() {
    const { type } = this.state

    var title=""
    var content = []

    switch (type) {
      case "logout_incomplete":
        title = "Please note you are not fully logged out!"
        content = [`You have been logged out from UCL API. However `
                    + `in order to be fully logged out of all UCL services `
                    + `you need to close your browser completely and re open.`,
                    "Thank you! Click here to go back to the front page:"]
        break;

      case "404":
        title = "Error 404"
        content = [`Oops we cannot seem to find that page! `,
                    "Please click below to go back to the front page:"]
        break;

      case "500":
        title = "Error 500"
        content = [`Oops... something went wrong! Sorry for the inconvenience. `,
                    `Our team is working on it, if you have an urgent concern please get `
                    + `in touch with us at isd.apiteam@ucl.ac.uk`,
                    "Please click below to go back to the front page:"]
        break;

      default:
          title = "Error"
          content = [`Oops... something went wrong! Sorry for the inconvenience. `,
                    `Our team is working on it, if you have an urgent concern please get `
                    + `in touch with us at isd.apiteam@ucl.ac.uk`,
                    "Please click below to go back to the front page:"]
        break;
    }

    return (
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
              <ImageView src={warning} width="367px" height="405px" description="large exclamation point, warning!" />
            </Column>

            <Column width="1-2" alignItems="column">
              <TextView 
                heading="1"
                text={title}
                align="left"
              />
              {content.map((line, key) =>
                <TextView 
                  heading="3"
                  text={line}
                  align="left"
                  key={key}
                />
              )}
              <ButtonView 
                text={"Home"} 
                link={`/`} 
                centred 
              />
            </Column>            
          </Row>
        </Container>

        <Footer />

      </>
    )
  }

}

ReactDOM.render(
  <Warning />,
  document.querySelector(`.app`)
)
