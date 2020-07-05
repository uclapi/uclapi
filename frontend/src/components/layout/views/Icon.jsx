/* eslint-disable react/prop-types */
import { ImageView } from 'Layout/Items.jsx'
import React from 'react'

/**
These are the rounded icons at the end of fields. Can change everything except 
how the actions are linked up

image,
description, 
onClick default: null, 
style default: styles.button
**/

// const styles = {
//   button: {
//     height: `40px`,
//     maxWidth: `40px`,
//     minWidth: `40px`,
//     float: `right`,
//     margin: `5px`,
//     marginLeft: `5px`,
//     cursor: `pointer`,
//   },
//   buttonIcon: {
//     marginTop: `8px`,
//   },
// }

const logosize = `20px`

export default class Icon extends React.Component {

  constructor(props) {
    super(props)
  }

  render() {
    const { image, description, onClick } = this.props

    return (
      <div className='icon-wrapper' onClick={onClick}>
          <ImageView src={image}
            width={logosize}
            height={logosize}
            description={description}
            centred
          />
      </div>
    )
  }

}