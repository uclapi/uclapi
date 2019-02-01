import React from 'react';
import PropTypes from 'prop-types';
import Navbar from '../dashboard/navbar.jsx';

class Hub extends React.Component {
  render () {
    return <div className="hub">
      <Navbar />
      <div className="content pure-g">
        <div className="pure-u-md-1-6"></div>
        <div className="pure-u-1 pure-u-md-2-3">
          {this.props.children}
        </div>
        <div className="pure-u-md-1-6"></div>
      </div>
    </div>;
  }
}

Hub.propTypes = {
  children: PropTypes.node
};

export default Hub;