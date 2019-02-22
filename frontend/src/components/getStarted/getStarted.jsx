import React from 'react';

import Intro from './Intro.jsx';
import Goal from './Goal.jsx';
import APIs from './APIs.jsx';
import Demo from './Demo.jsx';
import Marketplace from './Marketplace.jsx';
import Blog from './Blog.jsx';
import FAQ from './FAQ.jsx';
import GitHub from './GitHub.jsx';


export default class GetStartedComponent extends React.Component {

    render () {
      return (
        <div>
          <Intro />
          <Goal />
          <APIs />
          <Demo />
          <Blog />
          <Marketplace />
          <FAQ />
          <GitHub />
        </div>
      )
    }

}
