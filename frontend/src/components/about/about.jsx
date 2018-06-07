import React from 'react';

import Wil from './Wil.jsx';
import PersonContainer from './PersonContainer.jsx';


export default class AboutComponent extends React.Component {

  render () {
    return (
      <div>
        <Wil />
        <PersonContainer />
      </div>
    )
  }

}
