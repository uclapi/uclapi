import React from 'react';
import PropTypes from 'prop-types';
import NavbarConsistent from './navbarconsistent.jsx';

class Hub extends React.Component {
  render () {
    return <div className="hub">
      <NavbarConsistent />
      {this.props.children}
    </div>;
  }
}

Hub.propTypes = {
  children: PropTypes.node
};

export default Hub;