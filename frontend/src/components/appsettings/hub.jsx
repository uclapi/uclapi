import React from 'react';
import PropTypes from 'prop-types';

// Components
import {NavBar} from 'Layout/Items.jsx';

class Hub extends React.Component {
  render () {
    return <div className="hub">
      <NavBar isScroll={false}/>
      {this.props.children}
    </div>;
  }
}

Hub.propTypes = {
  children: PropTypes.node
};

export default Hub;