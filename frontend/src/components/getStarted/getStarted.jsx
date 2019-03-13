import React from 'react';

import Intro from './Intro.jsx';
import Goal from './Goal.jsx';
import APIs from './APIs.jsx';
import Demo from './Demo.jsx';
import Marketplace from './Marketplace.jsx';
import Blog from './Blog.jsx';
import GitHub from './GitHub.jsx';
import StagingBanner from './StagingBanner.jsx';
import NavbarConsistent from '../appsettings/navbarconsistent.jsx';

export default class GetStartedComponent extends React.Component {
    constructor(props){
      super(props);
      this.host = window.location.hostname;
    }
    render () {
      return (
        <div>
          {this.host == "staging.ninja" && <StagingBanner />}
          <NavbarConsistent isScroll={true} />
          <Intro />
          <Goal />
          <APIs />
          <Demo />
          <Blog />
          <Marketplace />
          <GitHub />
        </div>
      )
    }

}
