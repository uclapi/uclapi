// React
import React from 'react'

// Components
import { TextView } from 'Layout/Items.jsx'
import { refreshIcon, editIcon, saveIcon, 
	cancelIcon, copyIcon } from 'Layout/Icons.jsx'

/**
A generic field that is styled to fit in with the dashboard, uses the same sort of aesthetic as 
the auto complete form

PROPS:

title => text to be shown above the field
content => the initial content of the field

onSave => Makes field editable and will be the function called when user clicks save
onRefresh => Will add a refresh button allowing any extra functionality

canCopy => If true will add button to copy value to clipboard

readonly => Boolean flag of whether user can alter content
isSmall => A boolean flag of whether to render the field in a mobile friendly way

**/

const styles = {
	copyableField: {
		marginTop: `0`,
		width: `80%`,
		padding: `15px`,
		textAlign: `left`,
		backgroundColor: `transparent`,
	},
	copyableFieldMobile: {
		marginTop: `0`,
		width: `auto`,
		padding: `15px`,
		textAlign: `left`,
		maxWidth: `30%`,
		backgroundColor: `transparent`,
	},
	tokenText: {
		float: `left`,
		margin: `6px 10px 0 0`,
		color: `white`,
		fontWeight: `300`,
	},
	fieldHolder: {
		height: `50px`,
		paddingBottom: `20px`,
	},
	field: {
		backgroundColor: `#3498db`,
		height: `50px`,
		float: `left`,
		paddingRight: `10px`,
		width: `100%`,
		transition: `background-color 0.2s`,
	}
}

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
		if(!this.doesExist(onSave) && content !== prevProps.content) { this.setState({value: content}) }
	}

	save = (shouldPersist) => {
		const { onSave } = this.props
		const { fieldRefA, fieldRefB } = this.state

		const newValueA = fieldRefA.current.value
		const newValueB = fieldRefB.current.value

		var newValue = newValueA
		const { value } = this.state
		if(newValueA == value) { newValue = newValueB }

		console.log(newValueA)
		console.log(newValueB)
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

	edit = () => {
		this.setState({ isEditing: true })
	}

	doesExist = (variable) => {
		return typeof variable !== 'undefined'
	}

	copy = () => {
		const { fieldRefA, fieldRefB } = this.state
		const value = fieldRefA.current.value

	    if(this.DEBUGGING) { console.log(`Copy to clipboard`) }
	    if(this.DEBUGGING) { console.log(value) }
	    
	    fieldRefA.current.select()

	    try {
	      document.execCommand(`copy`)
	    } catch (err) {
	      alert(`Error: please press Ctrl/Cmd+C to copy`)
	    }
	}

	render() {
		const { readonly, onSave, onEdit, onRefresh, onCancel,
		 title, content, isSmall, canCopy } = this.props
		const { isSaved, fieldRefA, fieldRefB, value, 
			isEditing} = this.state
		
		const unsavedColor = `#db4534`
		const savedColor = `#2ecc71`
		const defaultColor = `#3498DB`

		var color = defaultColor
		if(isEditing) { color = isSaved ? savedColor : unsavedColor }

		const fieldStyle = {
			...styles.field,
			backgroundColor : color
		}

		return (
		<>
			<TextView text={title} heading={5} align={`left`} style={styles.tokenText} />
			                      
			<div className="field" style={fieldStyle} >
			  <div className={isSmall ? `none` : `tablet default`}>
			    <input ref={fieldRefA}
			      type="text"
			      className="token-input"
			      readOnly={!isEditing} 
			      onChange={isEditing ? () => { this.save(false) } : null } 
			      value={value}
			      style={styles.copyableField}
			    />
			  </div>
			  <div className={isSmall ? `tablet mobile default` : `mobile`}>
			    <input ref={fieldRefB}
			      type="text"
			      className="token-input"
			      readOnly={!isEditing} 
			      onChange={isEditing ? () => { this.save(false) } : null } 
			      value={value}
			      style={styles.copyableFieldMobile}
			    />
			  </div>
			  {canCopy ? copyIcon(this.copy) : null}

			  {this.doesExist(onSave) && isEditing ? saveIcon( () => { this.save(true) } ) : null}
			  {this.doesExist(onSave) && !isEditing ? editIcon(this.edit) : null}

			  {this.doesExist(onEdit) ? editIcon() : null}
			  {this.doesExist(onCancel) ? cancelIcon() : null}
			  {this.doesExist(onRefresh) ? refreshIcon(onRefresh) : null}
			</div>
		</>
		)
	}
}
