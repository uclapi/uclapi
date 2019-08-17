import React from 'react';
import PropTypes from 'prop-types';
import posed from 'react-pose';

const Bounce = posed.div({
  up: { marginTop: "-3px" },
  down: { marginTop: "3px" }
});

class Link extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			hover: false,
			isUp: false,
		}

		this.mInterval = null;

		this.onMouseEnterHandler = this.onMouseEnterHandler.bind(this);
		this.onMouseLeaveHandler = this.onMouseLeaveHandler.bind(this);
		this.bounce = this.bounce.bind(this);
	}

	onMouseEnterHandler() {
        this.setState({
            hover: true,
        });

        this.mInterval = window.setInterval(() => {
        	if(this.state.hover) {
        		this.bounce();
        	} 
        }, 400);
    }
    onMouseLeaveHandler() {
		window.clearInterval(this.mInterval);

        this.setState({
            hover: false,
            isUp: false,
        });
    }
    bounce() {
    	this.setState({
            isUp: !this.state.isUp,
        });
    }

	render() {
		return <div className="link-to-page" onMouseEnter={this.onMouseEnterHandler} onMouseLeave={this.onMouseLeaveHandler} >
					<Bounce className="bounce-image" pose={this.state.isUp ? 'up' : 'down'}>
						<img src={require('../../images/navbar/' + this.props.src + '.svg')} />
					</Bounce>
					<a href={this.props.link}>
						<h1>{this.props.name}</h1>
					</a>
				</div>;
	}
}

export default Link;