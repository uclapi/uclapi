import React from 'react';

import SectionHeader from './SectionHeader.jsx';

import Welcome from './Meta/Welcome.jsx';
import VersionInformation from './Meta/VersionInformation.jsx';

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
            <SectionHeader title="Welcome" />
            <Welcome />
            <VersionInformation />
            <SectionHeader title="Room Bookings" />
            <GetRooms />
            <GetBookings />
            <GetEquiment />
            <SectionHeader title="Search" />
            <GetPeople />
          </LanguageTabs>
        </div>
      )
    }

}
