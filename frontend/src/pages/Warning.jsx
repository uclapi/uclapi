import warning from 'Images/warning/warning.svg'
import {
  ButtonView,

  Column,
  Container,

  Footer,
  ImageView,
  NavBar,
  Row,
  TextView,
} from 'Layout/Items.jsx'
import React from 'react'
import ReactDOM from 'react-dom'
import 'Styles/common/uclapi.scss'
import 'Styles/navbar.scss'



class Warning extends React.Component {

  constructor(props) {
    super(props)

    this.state = {
      title: window.initialData.title,
      content: window.initialData.content,
    }
  }

  render() {
    const { title, content } = this.state

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
                text={`Home`} 
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
