import React from 'react';

import Intro from './Intro.jsx';
import Goal from './Goal.jsx';
import APIs from './APIs.jsx';
import Demo from './Demo.jsx';
import Marketplace from './Marketplace.jsx';
import Blog from './Blog.jsx';


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
        </div>
      )
    }

}
