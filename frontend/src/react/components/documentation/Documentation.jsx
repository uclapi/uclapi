import React from 'react';

import GetRooms from './Examples/GetRooms.jsx';
import GetBookings from './Examples/GetBookings.jsx';
import LanguageTabs from './LanguageTabs.jsx';
import SideNav from './SideNav.jsx';

export default class DocumentationComponent extends React.Component {

    render () {
      return (
        <div>
          <SideNav />
          <LanguageTabs>
            <GetRooms />
            <GetBookings />
          </LanguageTabs>
        </div>
      )
    }

}
