/* eslint-disable react/prop-types */
// Components
import {
  Button, CardView, Column,
  Container, Field, Row, TextView,
} from '@/components/layout/Items.jsx'
import React from "react";


/**
This has the multipurpose of being both for the confirm button and
also for the add new app button:

REQUIRED:

this.props.text => Description of what to do
this.props.value => Value needing to be entered
this.props.shouldCheckValue => Whether or not to check the value
  (default - false)
this.props.success => Function to be called on a successful click
this.props.fail => Function to be called on an unsuccessful click
**/
export default class ConfirmBox extends React.Component {

  constructor(props) {
    super(props)

    this.DEBUGGING = true

    this.state = {
      canSubmit: false,
      value: ``,
    }
  }

  saveField = (value) => {
    if(this.DEBUGGING) { console.log(value) }

    const { value: check, shouldCheckValue } = this.props
    let canSubmit = false

    if(shouldCheckValue && value == check) {
      canSubmit = true
    } else if(value === ``){
      canSubmit = false
    }

    if(!shouldCheckValue){
      canSubmit = true
    }

    if(this.DEBUGGING) {
      console.log(`canSubmit: ${canSubmit} value: ${value} against: ${check}, should check: ${shouldCheckValue}`)
    }

    this.setState({
      value: value,
      canSubmit: canSubmit,
    })
  }

  success = () => {
    const { value, canSubmit } = this.state
    const { success, shouldCheckValue, value: check} = this.props

    if(canSubmit) {
      success(value)
    } else {
      alert(
        (shouldCheckValue
          ? `Sorry please enter the correct value (${check}) and try again`
          : `Please enter a valid name and try again`
        )
        + ` (remember to click save)`
      )
    }
  }

  render() {
    const { text, fail } = this.props
    const { value } = this.state

    return (
      <div className='overlay-wrapper' style={{ textAlign: `center` }}>
        <CardView width='1-1' type='default' noPadding>
          <Container styling='transparent' className="confirm-box-container">
            <Row
              width="8-10"
              horizontalAlignment="center"
            >
              <TextView
                heading="3"
                align="left"
                text={text}
              />
              <Field
                title={`Click to edit`}
                content={value}
                onSave={this.saveField}
                isSmall
              />
              <Column
                width="1-1"
                keepInline
              >
                <Button
                  type={`alternate`}
                  onClick={this.success}
                  fakeLink
                  style={{ cursor: `pointer` }}
                >
                  Submit
                </Button>
                <Button
                  type={`remove`}
                  onClick={fail}
                  fakeLink
                  style={{ cursor: `pointer` }}
                >
                  Cancel
                </Button>
              </Column>
            </Row>
          </Container>
        </CardView>
      </div>
    )
  }
}
