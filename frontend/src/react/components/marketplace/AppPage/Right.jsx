import React from 'react';


export default class Right extends React.Component {

  render() {
    return (
      <div className="right">
        <h1>{this.props.app.name}</h1>
        <p>{this.props.app.detailedDescription}</p>
        {this.props.app.screenshots.map((link, i) => (
          <img src={link} key={i} />
        ))}
      </div>
    )
  }

}
