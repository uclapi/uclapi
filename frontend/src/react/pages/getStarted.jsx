import React from 'react';
import ReactDOM from 'react-dom';

class GetStarted extends React.Component {

  render () {
    return <div>
      <h2>Get Started</h2>
      <p>React</p>
    </div>;
  }

}

ReactDOM.render(
  <GetStarted />,
  document.querySelector('.app')
);
