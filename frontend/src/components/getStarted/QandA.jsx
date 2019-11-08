import Collapse, { Panel } from 'rc-collapse'
import React from 'react'

export default class QandA extends React.Component {
	render() {
		return (
			<Collapse>
				<Panel header={this.props.question} showArrow>
					<p>{this.props.answer}</p>
				</Panel>
			</Collapse>
		)
	}
}
