/* eslint-disable react/prop-types */
import React from 'react'


/*
  Each cell has the folling props:
  name: name of the attribute
  requirement: whether the attribute is required or optional
  extra: extra info about the attribute like type

  description: description of the attribute
  example: example which is rendered below the description
*/

export default class Cell extends React.Component {

  render() {
    return (
      <div className="row cell">
        <div className="col4 attribute">
          <p>{this.props.name}</p>
          <p className={this.props.requirement}>{this.props.requirement}</p>
          <p className="extra">{this.props.extra}</p>
        </div>
        <div className="col8">
          <p>{this.props.description}</p>
          <code>{this.props.example}</code>
        </div>
      </div>
    )
  }

}
