
import logo from './../../images/simpleAPILogoBlack.svg'



class Navbar extends React.Component {
  render () {
    return <div className="navbar centered">
      <img src={logo}/>
      <div className="logo-text"><div>UCL API</div></div>
    </div>
  }
}

export default Navbar
