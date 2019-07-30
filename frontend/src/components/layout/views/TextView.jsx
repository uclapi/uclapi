import React from 'react';

export default class TextView extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var heading_size = "6";
    if(this.props.heading) { heading_size = this.props.heading; }

    const CustomTag = `h${heading_size}`;
    var isLink = false;
    if(this.props.link) {isLink = true;}

    return (
      <CustomTag>
        {isLink ? ( 
          <a className="default-transition color-transition"href = {this.props.link}>
            {this.props.text}
          </a> 
        ) : (
          <div>
            {this.props.text}
          </div>
        )}
      </CustomTag>
    );
  }

}