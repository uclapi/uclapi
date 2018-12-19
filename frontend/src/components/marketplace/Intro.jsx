import React from 'react';

import FeaturedApps from './FeaturedApps.jsx';

export default class Intro extends React.Component {

  render() {
    return (
      <div className="intro">
        <div className="container">
          <h1>UCL Marketplace</h1>
          <p>Apps to improve student life at UCL</p>
        </div>
        <FeaturedApps allApps={this.props.allApps} />
      </div>
    )
  }

}
