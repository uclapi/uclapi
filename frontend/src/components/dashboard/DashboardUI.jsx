import React from 'react'

// Images
import clipboardImage from 'Images/dashboard/clipboard.svg'
import editImage from 'Images/dashboard/edit.svg'
import refreshImage from 'Images/dashboard/refresh.svg'
import saveImage from 'Images/dashboard/save.svg'
import deleteImage from 'Images/dashboard/trash.svg'
import { styles } from 'Layout/data/dashboard_styles.jsx'
import { CardView, CheckBox, ImageView, TextView, ButtonView, Row} from 'Layout/Items.jsx'

const logosize = `20px`

/**
These are the rounded icons at the end of fields. Can change everything except 
how the actions are linked up
**/
export const Icon = (image, description, onClick=null, style=styles.button) => (
  <div className='icon-wrapper' onClick={onClick}>
    <CardView width='1-3' type='emphasis' style={style} fakeLink>
      <ImageView src={image}
        width={logosize}
        height={logosize}
        description={description} 
        style={styles.buttonIcon}
        isCentered
      />
    </CardView>
  </div>
)

export const clipboardIcon = (onClick) => Icon(clipboardImage, `copy token to clipboard`, onClick)
export const refreshIcon = (onClick) => Icon(refreshImage, `refresh token`, onClick)
export const editIcon = (onClick) => Icon(editImage, `edit title of app`, onClick, {...styles.button,
float : `left`})
export const saveIcon = (onClick) => Icon(saveImage, `save details for future`, onClick)
export const cancelIcon = (onClick) => Icon(deleteImage, `cancel action`, onClick)

/**
This is used for the scopes and needs to be passed the specifc update event that it is
meant to update
**/
export const CheckBoxView = (text, value, onClick) => (
  <>                      
    <div className="field" style={styles.field}>
      <CheckBox onClick={onClick} isChecked={value} style={styles.checkBox}/>
      <TextView text={text} heading={5} align={`left`} style={styles.tokenText} /> 
      {saveIcon}
    </div>
  </>
)

/**
A generic field that is styled to fit in with the dashboard, uses the same sort of aesthetic as 
the auto complete form
**/ 
export const Field = (title, content, icons, meta) => {
  const fieldRefA = React.createRef()
  const fieldRefB = React.createRef()

  const unsavedColor = `#db4534`
  const savedColor = `#3498DB`

  return (
  <>
    <TextView text={title} heading={5} align={`left`} style={styles.tokenText} />
                          
    <div className="field"
      style={{ ...styles.field,
backgroundColor : (meta.isNotSaved ? unsavedColor : savedColor) }}
    >
      <div className={meta.isSmall ? `none` : `tablet default`}>
        <input ref={fieldRefA}
          type="text"
          className="token-input"
          readOnly={!(`save` in icons)} 
          onChange={ (`save` in icons) ? () => { icons.save.action(fieldRefA, false ) } : null } 
          value={content}
          style={styles.copyableField}
        />
      </div>
      <div className={meta.isSmall ? `tablet mobile default` : `mobile`}>
        <input ref={fieldRefB}
          type="text"
          className="token-input"
          readOnly={!(`save` in icons)} 
          onChange={(`save` in icons) ? () => { icons.save.action(fieldRefB, false ) } : null } 
          value={content}
          style={styles.copyableFieldMobile}
        />
      </div>
      {`cancel` in icons ? cancelIcon(icons.cancel.action) : null}
      {`copy` in icons ? clipboardIcon((e) => { icons.copy.action(e, fieldRefA); icons.copy.action(e, fieldRefB) }) : null}
      {`refresh` in icons ? refreshIcon(icons.refresh.action) : null}
      {`save` in icons ? saveIcon(() => { icons.save.action(fieldRefA, true); icons.save.action(fieldRefB, true) }) : null}
      {`edit` in icons ? editIcon(icons.edit.action) : null}
    </div>
  </>
  )
}



/**
This has the multipurpose of being both for the confirm button and
also for the add new app button:

REQUIRED:

this.props.text => Description of what to do
this.props.value => Value needing to be entered
this.props.success => Function to be called on a successful click
this.props.fail => Function to be called on an unsuccessful click
**/
export class OverlayBox extends React.Component {
  constructor(props) {
    super(props)

    this.saveField = this.saveField.bind(this)

    this.DEBUGGING = true

    this.state = {
      canSubmit: false,
      value: "", 
    }
  }

  saveField(value) {
    if(this.DEBUGGING) { console.log(value) }

    const { value: check } = this.props
    var canSubmit = false

    if(value) {
      if(value == check) {
        canSubmit = true
      }
    } else if(value != ""){
      canSubmit = true
    }

    this.setState({
      value: value,
      canSubmit: canSubmit, 
    })
  }

  render() {
    const { text, success, fail } = this.props

    return (
      <div className='overlay-wrapper' style={{ textAlign: `center` }}>
        <CardView width='1-1' type='default' noPadding>
          <Row styling='transparent' noPadding>
            { Field(text, this.state.value, {
              save: {action: (reference, shouldPersist) => { this.saveField(reference.current.value) } }
              }, {})
            }
            <ButtonView text={`Submit`} onClick={this.success} fakeLink />
            <ButtonView text={`Cancel`} type={`alternate`} onClick={this.fail} fakeLink />
          </Row>
        </CardView>
      </div>
    )
  }
}

export default {
  Icon,
  CheckBoxView,
  Field,
  clipboardIcon,
  refreshIcon,
  editIcon,
  saveIcon,
  OverlayBox
}