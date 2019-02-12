import React from 'react';


export default class FAQ extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="FAQ">
        <div className="container">
          <h1>FAQ</h1>

          <h2>What is UCL API?</h2>
          <h3>UCL API is a platform for interacting with 
          various data usually hidden away by UCL systems.  
          The aim is to enable skilled developers 
          to develop tools for other UCL students to enrich their
          lives at UCL.</h3>

          <h2>Who is running this?</h2>
          <h3>UCL API is a student-built platform. This means 
          all of the features open to you as developers have
          been developed by students as well!</h3>

          <h2>How do i get involved?</h2>
          <h3>UCL API is available as a public repository on github
          for anybody to clone and then make a pull request from. 
          It can be found <a href="https://github.com/uclapi/uclapi">here</a>.</h3>

          <h2>Does this cost anything?</h2>
          <h3>UCL API is and will always be a completely free platform 
          as the purpose is to enable innovation to better the student experience. 
          This cannot be done without amazing developers using the API and so we 
          will never make this monetized.</h3>

          <h2>What have other people built?</h2>
          <h3>Other people have developed applications such as Room Buddy for UCL 
          which helps students to find the closest free room in UCL for studying. A 
          full list of all of the applications created can be found on the
          <a href="/marketplace"> marketplace.</a></h3>

          <h2>Do I need to be from UCL to develop?</h2>
          <h3>Currently to develop applications you must be affiliated with UCL as 
          the authentication is done via UCL login. Without an appropriate login you 
          will be unable to develop applications using UCL API.</h3>

          <h2>Do I need to use a particlar language?</h2>
          <h3>UCL API is a RESTful API meaning that you are not restricted to using any 
          specific language.  Our <a href="/docs">documentation</a> currently includes instructions on how 
          to get up and running with Javascript, Python and Shell. However there is no
          restraints on the language you could use.</h3>
        
          <h2>How can I get in touch?</h2>
          <h3>If you have any other quieries get in touch with us on <a href="https://www.facebook.com/uclapi/">facebook </a> 
          or <a href="https://twitter.com/uclapi">twitter</a>.  We also respond to emails to isd.apiteam@ucl.ac.uk .</h3>
        </div>
      </div>
    )
  }

}
