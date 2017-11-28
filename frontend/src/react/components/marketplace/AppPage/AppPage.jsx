import React from 'react';


export default class AppPageComponent extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="">
        <h1>App Page for {this.props.appId}</h1>
      </div>
    )
  }

}
