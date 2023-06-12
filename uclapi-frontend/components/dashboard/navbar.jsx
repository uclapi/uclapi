import React from "react";

class Navbar extends React.Component {
  render () {
    return <div className="navbar centered">
      <img src={'/simpleAPILogoBlack.svg'}/>
      <div className="logo-text"><div>UCL API</div></div>
    </div>
  }
}

export default Navbar
