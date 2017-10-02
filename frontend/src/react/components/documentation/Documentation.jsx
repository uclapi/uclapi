import React from 'react';

import SectionHeader from './SectionHeader.jsx';

import Welcome from './Meta/Welcome.jsx';
import VersionInformation from './Meta/VersionInformation.jsx';

import RoomBookingsVersionHeader from './Routes/RoomBookings/VersionHeader.jsx';
import GetRooms from './Routes/RoomBookings/GetRooms.jsx';
import GetBookings from './Routes/RoomBookings/GetBookings.jsx';
import GetEquiment from './Routes/RoomBookings/GetEquipment.jsx';

import SearchVersionHeader from './Routes/Search/VersionHeader.jsx';
import GetPeople from './Routes/Search/GetPeople.jsx';

import GetInvolved from './GetInvolved/GetInvolved.jsx';

import LanguageTabs from './LanguageTabs.jsx';
import Sidebar from './Sidebar.jsx';

export default class DocumentationComponent extends React.Component {

    render () {
      return (
        <div>
          <Sidebar />
          <LanguageTabs>
            <Welcome />
            <VersionInformation />

            <SectionHeader link="roombookings" title="Room Bookings" />
            <RoomBookingsVersionHeader />
            <GetRooms />
            <GetBookings />
            <GetEquiment />

            <SectionHeader link="search" title="Search" />
            <SearchVersionHeader />
            <GetPeople />

            <GetInvolved />
          </LanguageTabs>
        </div>
      )
    }

}
