// Imports
import PropTypes from 'prop-types'
import React from 'react'
import { motion } from 'framer-motion'
import about from '../../images/navbar/about.svg'
import dashboard from '../../images/navbar/dashboard.svg'
import docs from '../../images/navbar/docs.svg'
import market from '../../images/navbar/market.svg'
// Images
import menu from '../../images/navbar/menu.svg'
import settings from '../../images/navbar/settings.svg'
import logo from './../../images/simpleAPILogoWhite.svg'
// Components
import Link from './Link.jsx'


const links = [
  {
    name: `settings`,
    link: `/settings`,
    src: settings,
  },
  {
    name: `about`,
    link: `/about`,
    src: about,
  },
  {
    name: `marketplace`,
    link: `/marketplace`,
    src: market,
  },
  {
    name: `documentation`,
    link: `/docs`,
    src: docs,
  },
  {
    name: `dashboard`,
    link: `/dashboard`,
    src: dashboard,
  },
]

const maxScreen = 1030
const menuSize = 189
const navbarHeight = 60

const toast = {
  hidden: { top: `-` + navbarHeight + `px` },
  shown: { top: 0 },
}
const slideDown = {
  shown: { height: menuSize + `px` },
  hidden: { height: 0 },
}

class NavBar extends React.Component {
  static propTypes = {
    isScroll: PropTypes.bool,
  }

  constructor(props) {
    super(props)

    this.DEBUGGING = false

    const { isScroll } = this.props

    this.state = {
      isVisible: !isScroll,
      isSmall: false,
      isMenuHidden: true,
    }
  }

  toggleMenu = () => {
    if (this.DEBUGGING) { console.log(`Menu button clicked...`) }

    const { isMenuHidden } = this.state
    this.setState({
      isMenuHidden: !isMenuHidden,
    })
  }

  handleClick = (event) => {
    if (this.DEBUGGING) {
      console.log(`Click event...`)
      console.log(event)
    }

    if (event.clientY > menuSize + navbarHeight) {
      if (this.DEBUGGING) { console.log(`Attempting to close menu...`) }
      this.forceClose()
    }
  }

  forceClose = () => {
    const { isMenuHidden } = this.state

    if (!isMenuHidden) {
      if (this.DEBUGGING) { console.log(`Closing menu...`) }

      this.setState({
        isMenuHidden: true,
      })
    }
  }

  updateDimensions = () => {
    if (window.innerWidth < maxScreen) {
      this.setState({
        isSmall: true,
        isMenuHidden: true,
      })
    } else {
      this.setState({
        isSmall: false,
        isMenuHidden: true,
      })
    }
  }

  componentDidMount() {
    const { isScroll } = this.props
    if (isScroll) { window.addEventListener(`scroll`, this.updateNavBar) }
    window.addEventListener(`resize`, this.updateDimensions)
    window.addEventListener(`click`, this.handleClick)

    this.updateDimensions()
    this.setState({
      isMenuHidden: true,
    })
  }

  componentWillUnmount() {
    const { isScroll } = this.props
    if (isScroll) { window.removeEventListener(`scroll`, this.updateNavBar) }
    window.removeEventListener(`click`, this.handleClick)
  }

  updateNavBar = () => {
    const scrollTop = window.scrollY
    const { isVisible } = this.state

    if (scrollTop <= navbarHeight && isVisible) {
      this.setState({
        isVisible: false,
        isMenuHidden: true,
      })
    } else if (scrollTop >= navbarHeight && !isVisible) {
      this.setState({
        isVisible: true,
        isMenuHidden: true,
      })
    }
  }

  render() {
    const { isVisible, isSmall, isMenuHidden } = this.state
    return <div className="navbar-extras">
      <motion.div
        className="navbarconsistent centered"
        initial="hidden"
        animate={isVisible ? `shown` : `hidden`}
        variants={toast}
      >
        <a href={`/`}>
          <img src={logo} />
        </a>
        <a href={`/`} style={{ textDecoration: `none` }} >
          <div className="logo-text-white">
            UCL API
          </div>
        </a>

        <div className="link-titles">
          {!isSmall ? (
            links.map(
              (s) => (
                <Link
                  key={s.name}
                  name={s.name}
                  src={s.src}
                  link={s.link}
                />
              )
            )
          ) : (
              <div className="menu-icon">
                <img src={menu} onClick={this.toggleMenu} />
              </div>
            )}
        </div>
      </motion.div>
      {isSmall ? (
        <motion.div
          className="link-titles-menu"
          initial="hidden"
          animate={isMenuHidden ? `hidden` : `shown`}
          variants={slideDown}
        >
          {[...links].reverse().map((s, key) => (
            <Link key={key} name={s.name} src={s.src} link={s.link} isSmall />
          ))}
        </motion.div>
      ) : null}
    </div>
  }
}

export default NavBar
