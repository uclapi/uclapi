import React from 'react';

import Topic from './Topic.jsx';


export default class SectionHeader extends React.Component {

    render () {
      return (
        <Topic
          noExamples={true}>
          <h1 className="sectionHeader">{this.props.title}</h1>
        </Topic>
      )
    }

}
