import { Column, Container, Row } from "@/components/layout/Items.jsx";
import Image from "next/image";
import { Button } from "rsuite";

// import '@/styles/common/uclapi.scss'
// import '@/styles/navbar.scss'

const Warning = ({ title, content }) => (
  <>
    {/* Warning message */}
    <Container styling="splash-parallax" height="600px">
      <Row width="2-3" horizontalAlignment="center" verticalAlignment="center">
        <Column width="1-2" className="default">
          <Image
            src={"/warning/warning.svg"}
            width={367}
            height={405}
            description="large exclamation point, warning!"
          />
        </Column>

        <Column width="1-2" alignItems="column" style={{ textAlign: "left" }}>
          <h1>{title}</h1>
          {typeof content === "string" ? <h3>{content}</h3> : content}
          <Button href={"/"} className="grey-btn">
            Home
          </Button>
        </Column>
      </Row>
    </Container>
  </>
);

export default Warning;
