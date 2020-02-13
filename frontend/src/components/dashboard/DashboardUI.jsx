import React from 'react'

import { styles } from 'Layout/data/dashboard_styles.jsx'

import { CardView, CheckBox, ImageView, TextView, 
  ButtonView, Row, Column, Field} from 'Layout/Items.jsx'

import { clipboardIcon, refreshIcon, editIcon, 
  saveIcon, cancelIcon } from 'Layout/Icons.jsx'

/**
This is used for the scopes and needs to be passed the specifc update event that it is
meant to update
**/
export const CheckBoxView = (text, value, onClick) => (
  <>                      
    <div className="field" style={{...styles.field, marginTop: `12px`}}>
      <CheckBox onClick={onClick} isChecked={value} style={styles.checkBox}/>
      <TextView text={text} heading={5} align={`left`} style={styles.tokenText} /> 
      {saveIcon}
    </div>
  </>
)


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
    this.success = this.success.bind(this)

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

    if(typeof check !== `undefined`) {
      if(value == check) {
        canSubmit = true
      }
    } else if(value != ""){
      canSubmit = true
    }

    if(this.DEBUGGING) { console.log("canSubmit: " + canSubmit + " value: " + value + " against: " + check) }

    this.setState({
      value: value,
      canSubmit: canSubmit, 
    })
  }

  success() {
    const { value, canSubmit } = this.state
    const { success } = this.props

    if(canSubmit) {
      success(value)
    } else {
      alert("Sorry please enter the correct value and try again")
    }
  }

  render() {
    const { text, success, fail } = this.props

    return (
      <div className='overlay-wrapper' style={{ textAlign: `center` }}>
        <CardView width='1-1' type='default' noPadding>
          <Row styling='transparent'>
            <Column width="8-10" horizontalAlignment="center">
              { Field(text, this.state.value, {
                save: {action: (reference, shouldPersist) => { this.saveField(reference.current.value) } }
                }, {})
              }
              <ButtonView text={`Submit`} onClick={this.success} fakeLink style={{ cursor: `pointer` }} />
              <ButtonView text={`Cancel`} type={`alternate`} onClick={fail} fakeLink style={{ cursor: `pointer` }} />
            </Column>
          </Row>
        </CardView>
      </div>
    )
  }
}

export default {
  CheckBoxView,
  OverlayBox
}