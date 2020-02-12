// React
import React from 'react'

// Components
import { TextView } from 'Layout/Items.jsx'
import { clipboardIcon, refreshIcon, editIcon, saveIcon, cancelIcon } from 'Layout/Icons.jsx'

/**
A generic field that is styled to fit in with the dashboard, uses the same sort of aesthetic as 
the auto complete form

PROPS:

title => text to be shown above the field
content => whether the content 
icons => A dictionary of icons and their respective action
readonly => Boolean flag of whether user can alter content
meta => A dictionary of auxilliary settings
isMobile => A boolean flag of whether to render the field in a mobile friendly way

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

export default class Field extends React.component {

	constructor(props) {
		super(props)

		const { content } = this.props
		this.save = this.save.bind(this)

		const fieldRefA = React.createRef()
		const fieldRefB = React.createRef()

		this.state = {
			persistedValue: content,
			fieldRefA: fieldRefA,
			fieldRefB: fieldRefB,
		}
	}

	save(shouldPersist) {
		const newValue = fieldRefA
		const { icons } = this.props

		// Call the save button action passed in via the props
		icons.save.action(fieldRefA, shouldPersist)
		icons.save.action(fieldRefB, shouldPersist)
	}

	render() {
		const { readonly, icons, meta, title, content } = this.props
		const { isSaved, fieldRefA, fieldRefB } = this.state
		
		const unsavedColor = `#db4534`
		const savedColor = `#3498DB`

		const fieldStyle = {
			...styles.field,
			backgroundColor : (isSaved ? unsavedColor : savedColor) 
		}

		return (
		<>
			<TextView text={title} heading={5} align={`left`} style={styles.tokenText} />
			                      
			<div className="field" style={fieldStyle} >
			  <div className={meta.isSmall ? `none` : `tablet default`}>
			    <input ref={fieldRefA}
			      type="text"
			      className="token-input"
			      readOnly={!(`save` in icons)} 
			      onChange={ (`save` in icons) ? () => { this.save(false) } : null } 
			      value={content}
			      style={styles.copyableField}
			    />
			  </div>
			  <div className={meta.isSmall ? `tablet mobile default` : `mobile`}>
			    <input ref={fieldRefB}
			      type="text"
			      className="token-input"
			      readOnly={!(`save` in icons)} 
			      onChange={(`save` in icons) ? () => { this.save(false) } : null } 
			      value={content}
			      style={styles.copyableFieldMobile}
			    />
			  </div>

			  {`cancel` in icons ? cancelIcon(icons.cancel.action, false) : null}
			  
			  {`copy` in icons ? clipboardIcon((e) => { icons.copy.action(e, fieldRefA); icons.copy.action(e, fieldRefB) }) : null}
			  
			  {`refresh` in icons ? refreshIcon(icons.refresh.action) : null}
			  
			  {`save` in icons ? saveIcon( () => { this.save(true) } ) : null}
			  
			  {`edit` in icons ? editIcon(icons.edit.action) : null}
			</div>
		</>
		)
	}
}
