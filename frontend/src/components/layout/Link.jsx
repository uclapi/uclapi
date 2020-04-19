/* eslint-disable react/prop-types */
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
            if (this.state.hover) {
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

        if (this.props.isSmall) {
            return (
                <a href={this.props.link}>
                    <div className="link-to-page"
                      style={{ borderBottom: `solid #ffffff29 2px`,
padding: `10px 0 10px 0` }}
                      onMouseEnter={this.onMouseEnterHandler}
                      onMouseLeave={this.onMouseLeaveHandler}
                    >
                        <h1 style={{ border: `none` }} >{this.props.name}</h1>
                    </div>
                </a>
            )
        } else {
            return (
                <div className="link-to-page" onMouseEnter={this.onMouseEnterHandler} onMouseLeave={this.onMouseLeaveHandler} >
                    <Bounce className="bounce-image" pose={animation}>
                        <img src={this.props.src} />
                    </Bounce>
                    <a href={this.props.link}>
                        <h1>{this.props.name}</h1>
                    </a>
                </div>
            )
        }
    }
}

export default Link