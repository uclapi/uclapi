import React from 'react';

export default class QandA extends React.Component {
	constructor(props) {
	    super(props);

	    this.state = { isHidden: true };
	    this.showhide = this.showhide.bind(this);
	    this.slideBox = this.slideBox.bind(this);
	    this.noBox = this.noBox.bind(this);
    }

    slideBox() {
    	return <div className="answer" key={this.props.id}><h3>{this.props.answer}</h3></div>;
    }
    noBox() {
    	return <div className="answer" key={this.props.id}></div>;
    }

    render() {
    	let answer = this.state.isHidden ? this.noBox() : this.slideBox();
    	return (
    		<div className="question-and-answer">
	    	    <div className="question" onClick={this.showhide}><h2>{this.props.question}</h2></div>
                {answer}
	        </div>
    	);
	}

    showhide() {
		this.setState({
		    isHidden: !this.state.isHidden
		});
    }
}