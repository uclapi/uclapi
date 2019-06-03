import React from 'react';


export default class Intro extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    var divStyle = {
      height: this.props.h,
    };

    return (
      <div className="wilContainer" style={divStyle}>
        <div className="container">
          <div className="row">
            <div className="col">
              <br />
            </div>
             <div className="col">
              <br />
            </div>
            <div className="col">
              <h1>Father of UCL API</h1>
              <p>On the 8th day, Wilhelm Klopp said let there be access to open data. And there was UCL API. 
              It is hard to imagine a world without the shining light that is UCL API guiding student 
              developers through the horror that is CMIS. But in these dark times boys became men and UCL API
              was born.</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

}
