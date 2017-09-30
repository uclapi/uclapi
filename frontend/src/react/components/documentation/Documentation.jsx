import React from 'react';

import GetRooms from './Routes/RoomBookings/GetRooms.jsx';
import GetBookings from './Routes/RoomBookings/GetBookings.jsx';
import GetEquiment from './Routes/RoomBookings/GetEquipment.jsx';

import GetPeople from './Routes/Search/GetPeople.jsx';

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
            <GetEquiment />
            <GetPeople />
          </LanguageTabs>
        </div>
      )
    }

}
