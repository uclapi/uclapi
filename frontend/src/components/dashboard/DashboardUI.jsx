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

export default {
  CheckBoxView,
}