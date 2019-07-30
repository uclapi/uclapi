import React from 'react';

export default class TextView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var heading_size = "6";
    if(this.props.heading) { heading_size = this.props.heading; }

    const CustomTag = `h${heading_size}`;

    return (
      <CustomTag>{this.props.text}</CustomTag>
    );
  }

}