import {
  Column,
  Container,
  ImageView,
  Row,
  TextView,
} from '@/components/layout/Items.jsx'
import Image from 'next/image'
import { Button } from 'rsuite'

// import '@/styles/common/uclapi.scss'
// import '@/styles/navbar.scss'

const Warning = ({ title, content }) => (
  <>
    {/* Warning message */}
    <Container styling="splash-parallax" height="600px">
      <Row
        width="2-3"
        horizontalAlignment="center"
        verticalAlignment="center"
      >

        <Column width="1-2" className="default">
          <Image
            src={'/warning/warning/svg'}
            width={367}
            height={405}
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
          <Button href={`/`} className='grey-btn'>
            Home
          </Button>
        </Column>
      </Row>
    </Container>
  </>
)

export default Warning
