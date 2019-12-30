import PropTypes from 'prop-types'
import React from 'react'
import posed from 'react-pose'

const Bounce = posed.div({
  up: { marginTop: `-8px` },
  middle: { marginTop: 0 },
  down: { marginTop: `8px` },
})

class Link extends React.Component {
	constructor(props) {
		super(props)

		this.state = {
			hover: false,
			animation: `middle`,
		}

		this.mInterval = null

		this.onMouseEnterHandler = this.onMouseEnterHandler.bind(this)
		this.onMouseLeaveHandler = this.onMouseLeaveHandler.bind(this)
		this.bounce = this.bounce.bind(this)
	}

	onMouseEnterHandler() {
        this.setState({
            hover: true,
        })

        this.mInterval = window.setInterval(() => {
        	if(this.state.hover) {
        		this.bounce()
        	} 
        }, 450)
    }
    onMouseLeaveHandler() {
		window.clearInterval(this.mInterval)

        this.setState({
            hover: false,
            animation: `middle`,
        })
    }
    bounce() {
    	const { animation } = this.state
    	const newAnimationState = (animation == `middle` || animation == `down`) ? `up` : `down`

    	this.setState({
            animation: newAnimationState,
        })
    }

	render() {
		const { animation } = this.state

		return <div className="link-to-page" onMouseEnter={this.onMouseEnterHandler} onMouseLeave={this.onMouseLeaveHandler} >
					<Bounce className="bounce-image" pose={animation}>
						<img src={require(`../../images/navbar/` + this.props.src + `.svg`)} />
					</Bounce>
					<a href={this.props.link}>
						<h1>{this.props.name}</h1>
					</a>
				</div>
	}
}

export default Link