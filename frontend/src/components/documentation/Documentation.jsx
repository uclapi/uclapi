import React from 'react';

import SectionHeader from './SectionHeader.jsx';

import Welcome from './Meta/Welcome.jsx';
import VersionInformation from './Meta/VersionInformation.jsx';

import OAuthIntro from './Routes/OAuth/OAuthIntro.jsx';
import Authorise from './Routes/OAuth/Authorise.jsx';
import Token from './Routes/OAuth/Token.jsx';
import UserData from './Routes/OAuth/UserData.jsx';
import StudentNumber from './Routes/OAuth/StudentNumber.jsx';

import RoomBookingsVersionHeader from './Routes/RoomBookings/VersionHeader.jsx';
import GetRooms from './Routes/RoomBookings/GetRooms.jsx';
import GetBookings from './Routes/RoomBookings/GetBookings.jsx';
import GetEquiment from './Routes/RoomBookings/GetEquipment.jsx';
import GetFreeRooms from './Routes/RoomBookings/GetFreeRooms.jsx';
import Webhooks from './Routes/RoomBookings/Webhooks.jsx';

import SearchVersionHeader from './Routes/Search/VersionHeader.jsx';
import GetPeople from './Routes/Search/GetPeople.jsx';

import TimetableVersionHeader from './Routes/Timetable/VersionHeader.jsx';
import GetDataDepartments from './Routes/Timetable/GetDataDepartments.jsx';
import GetDataModules from './Routes/Timetable/GetDataModules.jsx';
import GetPersonalTimetable from './Routes/Timetable/GetPersonalTimetable.jsx';
import GetTimetableByModules from './Routes/Timetable/GetTimetableByModules.jsx';
import GetDataCourses from './Routes/Timetable/GetDataCourses.jsx';
import GetDataCoursesModules from './Routes/Timetable/GetDataCoursesModules.jsx';

import ResourcesVersionHeader from './Routes/Resources/VersionHeader.jsx';
import DesktopAvailability from './Routes/Resources/DesktopAvailability.jsx';

import WorkspacesGetSurveys from './Routes/Workspaces/GetSurveys.jsx';
import WorkspacesGetSensors from './Routes/Workspaces/GetSensors.jsx';
import WorkspacesGetLastSensorUpdate from './Routes/Workspaces/GetLastSensorUpdate.jsx';
import WorkspacesGetHistoricalTimeData from './Routes/Workspaces/GetSensorHistoricalTimeData.jsx';
import WorkspaceGetSensorsSummary from './Routes/Workspaces/GetSensorSummary.jsx';
import WorkspacesGetImage from './Routes/Workspaces/GetImage.jsx';
import WorkspacesGetLiveImage from './Routes/Workspaces/GetLiveImage.jsx';

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

            <SectionHeader link="oauth" title="OAuth" />
            <OAuthIntro />
            <Authorise />
            <Token />
            <UserData />
            <StudentNumber />

            <SectionHeader link="roombookings" title="Room Bookings" />
            <RoomBookingsVersionHeader />
            <GetRooms />
            <GetBookings />
            <GetEquiment />
            <GetFreeRooms />
            <Webhooks />

            <SectionHeader link="search" title="Search" />
            <SearchVersionHeader />
            <GetPeople />

            <SectionHeader link="timetable" title="Timetable" />
            <TimetableVersionHeader />
            <GetPersonalTimetable />
            <GetTimetableByModules />
            <GetDataDepartments />
            <GetDataModules />
            <GetDataCourses />
            <GetDataCoursesModules />

            <SectionHeader link="resources" title="Resources" />
            <ResourcesVersionHeader />
            <DesktopAvailability />

            <SectionHeader link="workspaces" title="Workspaces" />
            <WorkspacesGetSurveys />
            <WorkspacesGetSensors />
            <WorkspacesGetHistoricalTimeData />
            <WorkspacesGetLastSensorUpdate />
            <WorkspaceGetSensorsSummary />
            <WorkspacesGetImage />
            <WorkspacesGetLiveImage />

            <GetInvolved />
          </LanguageTabs>
        </div>
      )
    }

}
