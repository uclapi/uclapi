// React
import React from 'react'

// Components
import { TextView, Container } from 'Layout/Items.jsx'
import { refreshIcon, editIcon, saveIcon, 
	cancelIcon, copyIcon } from 'Layout/Icons.jsx'

/**
A generic field that is styled to fit in with the dashboard, uses the same sort of aesthetic as 
the auto complete form

PROPS:

title => text to be shown above the field
content => the initial content of the field
canCopy => If true will add button to copy value to clipboard
isSmall => A boolean flag of whether to render the field in a mobile friendly way

onSave => Makes field editable and will be the function called when user clicks save
onRefresh => Will add a refresh button allowing any extra functionality

style

**/


export default class Field extends React.Component {

	constructor(props) {
		super(props)

		const fieldRefA = React.createRef()
		const fieldRefB = React.createRef()
		const { content } = this.props

		this.DEBUGGING=true

		this.state = {
			value: content,
			fieldRefA: fieldRefA,
			fieldRefB: fieldRefB,
			isSaved: true,
			isEditing: false,
		}
	}

	componentDidUpdate(prevProps) {
		const { content, onSave } = this.props
		// If this is an uneditable field then the value needs to 
		// be updated when the parent changes the content
		if(content !== prevProps.content) { 
			this.setState({value: content}) 
		}
	}

	save = (shouldPersist) => {
		const { onSave } = this.props
		const { fieldRefA, fieldRefB } = this.state

		const newValueA = fieldRefA.current.value
		const newValueB = fieldRefB.current.value

		var newValue = newValueA
		const { value } = this.state
		if(newValueA == value) { newValue = newValueB }

		if(this.DEBUGGING) { console.log("new value: " + newValue) }
		
		// Call the save button action passed in via the props
		if(shouldPersist) {
			onSave(newValue)
			this.setState({ isEditing: false })
		}

		this.setState({
			value: newValue,
			isSaved: shouldPersist,
		})
	}

	toggleEditing = () => { 
		const { onSave } = this.props
		const { isEditing, fieldRefB, fieldRefA } = this.state 

		if(this.doesExist(onSave)) {
			if(isEditing) {
				this.cancel()
			} else {
				this.setState({ isEditing: !isEditing }) 
				fieldRefB.current.focus()
				fieldRefA.current.focus()
			}
		}
	}
	cancel = () => { 
		const { content } = this.props

		this.setState({ 
			isEditing: false, 
			value: content, 
			isSaved: true,
		}) 
	}

	doesExist = (variable) => {
		return typeof variable !== 'undefined'
	}

	copy = (isReferenceA) => {
		const { fieldRefA, fieldRefB } = this.state

	    if(this.DEBUGGING) { console.log(`Copy to clipboard`) }
	    
	    if(isReferenceA) {
	    	fieldRefA.current.select()
	    } else {
	    	fieldRefB.current.select()
    	}

	    try {
	      document.execCommand(`copy`)
	    } catch (err) {
	      alert(`Error: please press Ctrl/Cmd+C to copy`)
	    }
	}

	render() {
		const { onSave, onRefresh, style,
		 title, content, isSmall, canCopy } = this.props
		const { isSaved, fieldRefA, fieldRefB, value, 
			isEditing} = this.state

		const fieldClass = "field-input"
		const fieldHeight = "55px"

		return (
		<>
			{/*<TextView text={title} color="white" heading={6} align={`left`} />*/}
			                      
			<Container styling="primary" height={fieldHeight} noPadding>
			  	<div 
				  className={isSmall ? `none` : `tablet default`} 
				  onClick={this.toggleEditing} 
				  style={{ cursor: `pointer` }}
				>
					<input ref={fieldRefA}
					type="text"
					className={fieldClass}
					readOnly={!isEditing} 
					onChange={isEditing ? () => { this.save(false) } : null } 
					value={value}
					style={{ height: fieldHeight }}
					/>
					{canCopy ? copyIcon(() => { this.copy(true) }) : null}
			 	</div>
			  	<div 
					className={isSmall ? `tablet mobile default` : `mobile`} 
					onClick={this.toggleEditing} 
					style={{ cursor: `pointer` }}
				>
					<input ref={fieldRefB}
					type="text"
					className={fieldClass}
					readOnly={!isEditing} 
					onChange={isEditing ? () => { this.save(false) } : null } 
					value={value}
					style={{ height: fieldHeight }}
					/>
					{canCopy ? copyIcon(() => { this.copy(false) }) : null}
			  	</div>
			  
				{this.doesExist(onSave) && isEditing ? saveIcon( () => { this.save(true) } ) : null}
				{this.doesExist(onSave) && isEditing ? cancelIcon(this.cancel) : null}
				{this.doesExist(onSave) && !isEditing ? editIcon(this.toggleEditing) : null}
				{this.doesExist(onRefresh) ? refreshIcon(onRefresh) : null}
			</Container>
		</>
		)
	}
}
