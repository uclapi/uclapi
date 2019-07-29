// Standard React importss
import React from 'react';
import ReactDOM from 'react-dom';

// Styles
import './../sass/getStarted.scss';
import './../sass/navbar.scss';

// Common Components
import SingleCentralColumn from '../components/layout/container/SingleCentralColumn.jsx';

class HomePage extends React.Component {

  render () {
    return (
      <div className = "home-page">
        <SingleCentralColumn 
          child = "" />
      </div>
    );
  }

}

ReactDOM.render(
  <HomePages />,
  document.querySelector('.app')
);
