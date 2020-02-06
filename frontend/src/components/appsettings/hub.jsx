import React from 'react';
import PropTypes from 'prop-types';

// Components
import { NavBar, Footer } from 'Layout/Items.jsx';

class Hub extends React.Component {
  render () {
    return <>
      <NavBar isScroll={false}/>
      {this.props.children}
      <Footer />
    </>;
  }
}

Hub.propTypes = {
  children: PropTypes.node
};

export default Hub;