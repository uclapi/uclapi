import React from 'react'

import QandA from './QandA.jsx'

class FAQ extends React.Component {
  render() {
    return (
      <div className="FAQ">
        <div className="container">
          <h1>FAQ</h1>
          <QandA
            question={`What is UCL API?`}
            answer={[`UCL API is a platform for interacting with data that is usually difficult to obtain or hidden in internal UCL systems. The aim is to enable student developers to develop tools for other UCL students to enrich their lives at UCL. Almost every API returns JSON which is simple to parse and interpret in most modern programming languages.`]}
          />

          <QandA
            question={`Who is running this?`}
            answer={[`UCL API is a student-built platform, backed and supported by UCL's `, <a href="https://www.ucl.ac.uk/isd/">Information Services Division (ISD)</a>, `. This means that all of the features in UCL API have been developed by students and are aimed at students such as yourself, so jump right in!`]}
          />

          <QandA
            question={`Do I need to be from UCL to use the UCL API?`}
            answer={[`You need to be affiliated with UCL because authentication (for both developers & end users) is done via the UCL login system. `]}
          />

          <QandA
            question={`Do I need to write my apps in a particular programming language?`}
            answer={[`UCL API is a RESTful API hence you can use any language you like. Our `, <a href='/docs'>docs</a>, ` currently includes instructions on how to get up and running with Javascript, Python and the Unix shell using cURL. However, you may use any other programming language so long as it can make HTTP requests.`]}
          />

          <QandA
            question={`How do I get involved?`}
            answer={[`UCL API is open source. Our source code is available on `, <a href="https://github.com/uclapi/uclapi">a public Github repository on</a>, ` for anybody to clone and inspect. Find an bug? Feel free to open an `, <a href="https://github.com/uclapi/uclapi/issues">Issue</a>, ` or even a `, <a href="https://github.com/uclapi/uclapi/pulls">Pull Request</a>, ` with a proposed fix! We also have annual hiring windows to recruit more students as others graduate, so keep an eye on our social media accounts.`]}
          />

          <QandA
            question={`Does this cost anything?`}
            answer={[`UCL API is and will always be a completely free as the platform's purpose is to enable innovation to better the student experience. This cannot be done without amazing developers such as yourself using the API.`]}
          />

          <QandA
            question={`What have other people built?`}
            answer={[`From small Computer Science projects, to running lecture theatre central heating systems right up to UCL Assistant, UCL API is being used across UCL for many projects public and private. A full list of all (known!) applications available to the UCL community can be found at the `, <a href="/marketplace">Marketplace.</a>]}
          />

          <QandA
            question={`How can I get in touch?`}
            answer={[`If you have any other queries get in touch with us on `, <a href="https://www.facebook.com/uclapi/">Facebook</a>, ` or `, <a href="https://twitter.com/uclapi">Twitter</a>, `.  We also respond to emails to `, <a href="mailto:isd.apiteam@ucl.ac.uk">isd.apiteam@ucl.ac.uk</a>, `.`]}
          />

          <QandA
            question={`Who owns the Intellectual Property (IP) of what I build?`}
            answer={[`You do! We have no claim on your IP. However, we do request you include a shoutout somewhere. This helps raise awareness of UCL API and the vast amount of data available. It may not always be possible to include this attribution in an unintrusive manner (e.g. in a Slack bot), so we're flexible on this. The more people aware of UCL API and who use apps powered by UCL API, the better the platform will be. If you have any questions please feel free to reach out!`]}
          />
        </div>
      </div>
    )
  }

}

export default FAQ
