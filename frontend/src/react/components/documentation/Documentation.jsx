import React from 'react';

import GetRooms from './Examples/GetRooms.jsx';
import GetBookings from './Examples/GetBookings.jsx';
import LanguageTabs from './LanguageTabs.jsx';

export default class DocumentationComponent extends React.Component {

    render () {
      return (
        <div>
          <LanguageTabs>
            <GetRooms />
            <GetBookings />
          </LanguageTabs>
        </div>
      )
    }

}
