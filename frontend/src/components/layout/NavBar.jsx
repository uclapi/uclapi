// Imports
import React from 'react';
import logo from './../../images/simpleAPILogoWhite.svg';
import posed from 'react-pose';
// Components
import Link from './Link.jsx';
// Images
import menu from '../../images/navbar/menu.svg';

const Toast = posed.div({
	hidden: { top: '-60px' },
	shown: { top: 0 }
});

let links = [
	// {
	// 	name: "settings",
	// 	link: "/oauth/myapps",
	// 	src: "settings", 
	// },
	{
		name: "about",
		link: "/about",
		src: "about",
	},
	{
		name: "documentation",
		link: "/docs",
		src: "docs",
	},
	{
		name: "dashboard",
		link: "/dashboard",
		src: "dashboard",
	},
	{
		name: "marketplace",
		link: "/marketplace",
		src: "market",
	},
]
const SlideDown = posed.div({
	shown: { height: "152px"},
	hidden: { height: 0 },
});
const maxScreen = 1030;

class NavBar extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			isVisible: !this.props.isScroll,
			isSmall: false,
			isMenuHidden: true,
		}

		this.updateNavBar = this.updateNavBar.bind(this);
		this.updateDimensions = this.updateDimensions.bind(this);
		this.toggleMenu = this.toggleMenu.bind(this);
		this.navbarHeight = 60;
	}
	toggleMenu() {
		console.log("menu click")
		this.setState({
			isMenuHidden: !this.state.isMenuHidden,
		});
	}
	updateDimensions() {
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
	componentWillMount() {
		this.updateDimensions();
		this.setState({
			isMenuHidden: true,
		});
	}
	componentDidMount() {
		if (this.props.isScroll) { window.addEventListener('scroll', this.updateNavBar); }
		window.addEventListener("resize", this.updateDimensions);
	}
	componentWillUnmount() {
		if (this.props.isScroll) { window.removeEventListener('scroll', this.updateNavBar); }
	}
	updateNavBar() {
		let scrollTop = window.scrollY;

		if (scrollTop <= this.navbarHeight && this.state.isVisible) {
			this.setState({
				isVisible: false,
				isMenuHidden: true,
			})
		} else if (scrollTop >= this.navbarHeight && !this.state.isVisible) {
			this.setState({
				isVisible: true,
				isMenuHidden: true,
			})
		}
	}

	render() {
		return <div className="navbar-extras">
			<Toast className="navbarconsistent centered" pose={this.state.isVisible ? 'shown' : 'hidden'}>
				<a href={"/"}>
					<img src={logo} />
				</a>
				<div className="logoTextWhite"><div>UCL API</div></div>

				<div className="link-titles">
					{!this.state.isSmall ? (
						links.map((s, key) => <Link key={key} name={s.name} src={s.src} link={s.link} />)
					) : (
							<div className="menu-icon"><img src={menu} onClick={this.toggleMenu} /></div>
						)}
				</div>
			</Toast>
			{this.state.isSmall ? (
				<SlideDown className="link-titles-menu" pose={this.state.isMenuHidden ? 'hidden' : 'shown'}>
					{links.map((s, key) => <Link key={key} name={s.name} src={s.src} link={s.link} isSmall/>)}
				</SlideDown>
			) : null}
		</div>
	}
}

export default NavBar;