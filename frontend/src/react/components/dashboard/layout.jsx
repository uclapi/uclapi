import React from 'react';
import PropTypes from 'prop-types';
import Navbar from './navbar.jsx';

class Layout extends React.Component {
  render () {
    return <div className="layout">
      <Navbar />
      <div className="content pure-g">
        <div className="pure-u-md-1-4"></div>
        <div className="pure-u-1 pure-u-md-1-2">
          <div className="pure-g">{this.props.children}</div>
        </div>
        <div className="pure-u-md-1-4"></div>
      </div>
    </div>;
  }
}

Layout.propTypes = {
  children: PropTypes.node
};

export default Layout;
