/* eslint-disable react/prop-types */

// React
import {
  cancelIcon,
  copyIcon,
  editIcon,
  refreshIcon,
  saveIcon,
} from 'Layout/Icons.jsx'
// Components
import { Container } from 'Layout/Items.jsx'
import React from 'react'

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

    const fieldRef = React.createRef()
    const { content } = this.props

    this.DEBUGGING=true

    this.state = {
      value: content,
      fieldRef: fieldRef,
      isSaved: true,
      isEditing: false,
    }
  }

  componentDidUpdate(prevProps) {
    const { content } = this.props
    // If this is an uneditable field then the value needs to 
    // be updated when the parent changes the content
    if(content !== prevProps.content) { 
      this.setState({value: content}) 
    }
  }

  onKeyDown = (event) => {
    // 'keypress' event misbehaves on mobile so we track 'Enter' key via 'keydown' event
    if (event.key === `Enter`) {
      event.preventDefault()
      event.stopPropagation()
      this.save(true)
    }
  }

  save = (shouldPersist) => {
    const { onSave } = this.props
    const { fieldRef } = this.state

    const newValue = fieldRef.current.value

    if(this.DEBUGGING) { console.log(`new value: ` + newValue) }
    
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
    const { isEditing, fieldRef } = this.state 

    if(this.doesExist(onSave)) {
      if(isEditing) {
        this.cancel()
      } else {
        this.setState({ isEditing: !isEditing }) 
        fieldRef.current.focus()
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
    return typeof variable !== `undefined`
  }

  copy = () => {
    const { fieldRef } = this.state

      if(this.DEBUGGING) { console.log(`Copy to clipboard`) }
      
      fieldRef.current.select()

      try {
        document.execCommand(`copy`)
      } catch (err) {
        alert(`Error: please press Ctrl/Cmd+C to copy`)
      }
  }

  render() {
    const {
      onSave,
      onRefresh,
      title,
      canCopy,
    } = this.props
    const {
      fieldRef,
      value, 
      isEditing,
    } = this.state

    const state = this.doesExist(onSave) ? (
      isEditing ? `editing` : `not-editing`
    ) : `uneditable`
    const fieldClass = `field-container-` + state
    const fieldInputClass = `field-input-` + state
    const fieldHeight = `55px`

    return (
    <>
      {/*<TextView text={title} color="white" heading={6} align={`left`} />*/}
                            
      <Container 
        className={fieldClass}
        height={fieldHeight} 
        onClick={this.toggleEditing}
        noPadding
      >
        <div className="field-label">{title}</div>

        <input ref={fieldRef}
          type="text"
          className={fieldInputClass}
          readOnly={!isEditing} 
          // eslint-disable-next-line react/jsx-no-bind
          onChange={isEditing ? () => { this.save(false) } : null } 
          onKeyDown={this.onKeyDown}
          value={value}
          style={{ height: fieldHeight }}
        />

        {canCopy ? copyIcon(() => { this.copy() }) : null}
        
        {this.doesExist(onSave) && isEditing ? saveIcon( () => { this.save(true) } ) : null}
        {this.doesExist(onSave) && isEditing ? cancelIcon(this.cancel) : null}
        {this.doesExist(onSave) && !isEditing ? editIcon(this.toggleEditing) : null}
        {this.doesExist(onRefresh) ? refreshIcon(onRefresh) : null}
      </Container>
    </>
    )
  }
}
