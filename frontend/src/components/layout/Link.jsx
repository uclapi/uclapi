/* eslint-disable react/prop-types */
import React from 'react'
import { motion } from 'framer-motion'

const bounceTransition = {
    y: {
        type: `spring`,
        stiffness: 100,
        duration: 0.4,
    },
}

class Link extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            hover: false,
        }

        this.onMouseEnterHandler = this.onMouseEnterHandler.bind(this)
        this.onMouseLeaveHandler = this.onMouseLeaveHandler.bind(this)
    }

    onMouseEnterHandler() {
        this.setState({
            hover: true,
        })
    }

    onMouseLeaveHandler() {
        this.setState({
            hover: false,
        })
    }

    render() {
        const { hover } = this.state
        const {src, link, name} = this.props

        if (this.props.isSmall) {
            return (
                <a href={link}>
                    <div className="link-to-page"
                      style={{ borderBottom: `solid #ffffff29 2px`,
                               padding: `10px 0 10px 0` }}
                      onMouseEnter={this.onMouseEnterHandler}
                      onMouseLeave={this.onMouseLeaveHandler}
                    >
                        <img style={{ paddingLeft: `5px`}} src={src} />
                        <h1 style={{ border: `none`}} >{name}</h1>
                    </div>
                </a>
            )
        } else {
            return (
                <div className="link-to-page" onMouseEnter={this.onMouseEnterHandler} onMouseLeave={this.onMouseLeaveHandler} >
                    <motion.div className="bounce-image" transition={bounceTransition} animate={hover ? {y: [`0%`, `-50%`]} : {y: `0%`}}>
                        <img src={src} />
                    </motion.div>
                    <a href={link}>
                        <h1>{name}</h1>
                    </a>
                </div>
            )
        }
    }
}

export default Link