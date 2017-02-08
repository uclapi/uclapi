import React from 'react';

class Navbar extends React.Component {
  render () {
    return <div className="navbar centered">
      <img src={window.staticURL + 'simpleAPILogoBlack.svg'}/>
      <div className="logoText"><div>UCL API</div></div>
    </div>;
  }
}

export default Navbar;
