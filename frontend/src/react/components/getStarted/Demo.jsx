import React from 'react';
import {GridList, GridTile} from 'material-ui/GridList';
import {Tabs, Tab} from 'material-ui/Tabs';

import SyntaxHighlighter from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/styles';


let languages = [
  {
    "name": "python",
    "code": `from twilio.rest import TwilioRestClient

# put your own credentials here
ACCOUNT_SID = "AC5ef872f6da5a21de157d80997a64bd33"
AUTH_TOKEN = "[AuthToken]"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

client.messages.create(
  to="+16518675309",
  from_="+14158141829",
  body="Tomorrow forecast in Financial District, San Francisco is Clear.",
  media_url="https://climacons.herokuapp.com/clear.png",
)`
  },

  {
    "name": "javascript",
    "code": `import SyntaxHighlighter, { registerLanguage } from "react-syntax-highlighter/dist/light"
import js from 'react-syntax-highlighter/dist/languages/javascript';
import docco from 'react-syntax-highlighter/dist/styles/docco';

registerLanguage('javascript', js);`
  }
]

export default class Demo extends React.Component {

  render () {
    return (
      <div className="demo">
        <div className="text">

        </div>
        <div className="code">
          <Tabs>
            {
              languages.map((language, index) => (
                <Tab key={index} label={ language.name }>
                  <div>
                    <SyntaxHighlighter language={language.name}
                      style={dracula}>{language.code}</SyntaxHighlighter>
                  </div>
                </Tab>
              ))
            }
          </Tabs>
        </div>
      </div>
    )
  }

}
