import React from 'react';
import Navbar from '../components/navbar.jsx';

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
  children: React.PropTypes.node
};

export default Layout;
