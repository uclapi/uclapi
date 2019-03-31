import React from 'react';
import QandA from './QandA.jsx';
import Collapse from 'rc-collapse';


class FAQ extends React.Component {
  render() {
    return (
      <div className="FAQ">
        <div className="container">
          <h1>FAQ</h1>
          <QandA 
          question={"Do I need to be from UCL to develop?"}
          answer={["Currently to develop applications you must be affiliated with UCL as authentication is done via UCL login. Without an appropriate login you will be unable to develop applications using UCL API."]}
          id={"1"} />

          <QandA 
          question={"Do I need to use a particlar language?"}
          answer={["UCL API is a RESTful API meaning that you are not restricted to using any specific language. Our ", <a href='/docs'>documentation</a>, " currently includes instructions on how to get up and running with Javascript, Python and the Unix shell using cURL. However, you may use any other programming language so long as it can make web requests."]}
          id={"2"} />

          <QandA 
          question={"What is UCL API?"}
          answer={["UCL API is a platform for interacting with data that is usually difficult to obtain or hidden in internal UCL systems. The aim is to enable student developers to develop tools for other UCL students to enrich their lives at UCL. Almost every API returns JSON which is simple to parse and interpret in most modern programming languages."]}
          id={"3"} />

          <QandA 
          question={"Who is running this?"}
          answer={["UCL API is a student-built platform, backed and supported by UCL's Information Services Division (ISD). This means that all of the features in UCL API have been both developed by students and aimed at students such as yourself, so jump right in!"]}
          id={"4"} />

          <QandA 
          question={"How do I get involved?"}
          answer={["UCL API is available as a public repository on ", <a href="https://github.com/uclapi/uclapi">GitHub</a>, " for anybody to clone and inspect. Find an issue? Feel free to open an ", <a href="https://github.com/uclapi/uclapi/issues">Issue</a>, " or even a ", <a href="https://github.com/uclapi/uclapi/pulls>Pull Request</a>, " with a proposed fix! We also have annual hiring windows to recruit more students as others graduate, so keep an eye on our social media accounts."]}
          id={"5"} />

          <QandA 
          question={"Does this cost anything?"}
          answer={["UCL API is and will always be a completely free as the platform's purpose is to enable innovation to better the student experience. This cannot be done without amazing developers such as yourself using the API."]}
          id={"6"} />

          <QandA 
          question={"What have other people built?"}
          answer={["From small Computer Science projects, to running lecture theatre central heating systems right up to UCL Assistant, UCL API is being used across UCL for many projects public and private. A full list of all (known!) applications available to the UCL community can be found at the ", <a href="/marketplace">Marketplace.</a>]}
          id={"7"} />

          <QandA 
          question={"How can I get in touch?"}
          answer={["If you have any other queries get in touch with us on ", <a href="https://www.facebook.com/uclapi/">Facebook</a>, " or ", <a href="https://twitter.com/uclapi">Twitter</a>, ".  We also respond to emails to ", <a href="mailto:isd.apiteam@ucl.ac.uk">isd.apiteam@ucl.ac.uk</a>, "."]}
          id={"8"} />
          
          <QandA
          question={"Who owns the Intellectual Property (IP) of what I build?"}
          answer={["You do! We have no claim on your IP. However, we would ask that, if possible, you place somewhere in any apps you write with UCL API a mention that the data came from us; this it helps to raise awareness of this service for any student developers who might make use of your app. This is not strictly enforced though, as it may not be possible to include this attribution in an unintrusive manner (e.g. in a Slack bot). If you have any questions please feel free to reach out! We are very flexible on this as we want you to focus on creating great apps that will improve the lives of students at UCL."]}
          id={"9"} />
        </div>
      </div>
    )
  }

}

export default FAQ;
