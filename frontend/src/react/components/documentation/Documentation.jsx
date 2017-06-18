import React from 'react';

import GetRooms from './Examples/GetRooms.jsx';
import GetBookings from './Examples/GetBookings.jsx';
import LanguageTabs from './LanguageTabs.jsx';
import Sidebar from './Sidebar.jsx';

export default class DocumentationComponent extends React.Component {

    render () {
      return (
        <div>
          <Sidebar />
          <LanguageTabs>
            <GetRooms />
            <GetBookings />
          </LanguageTabs>
        </div>
      )
    }

}
