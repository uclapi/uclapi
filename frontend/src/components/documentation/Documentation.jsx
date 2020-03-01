// UCL API navbar
import 'Styles/navbar.scss'

import React from 'react'

import { NavBar } from 'Layout/Items.jsx'

import GetInvolved from './GetInvolved/GetInvolved.jsx'
import Welcome from './Meta/Welcome.jsx'
import Authorise from './Routes/OAuth/Authorise.jsx'
import OAuthIntro from './Routes/OAuth/OAuthIntro.jsx'
import StudentNumber from './Routes/OAuth/StudentNumber.jsx'
import Token from './Routes/OAuth/Token.jsx'
import UserData from './Routes/OAuth/UserData.jsx'
import DesktopAvailability from './Routes/Resources/DesktopAvailability.jsx'
import GetBookings from './Routes/RoomBookings/GetBookings.jsx'
import GetEquiment from './Routes/RoomBookings/GetEquipment.jsx'
import GetFreeRooms from './Routes/RoomBookings/GetFreeRooms.jsx'
import GetRooms from './Routes/RoomBookings/GetRooms.jsx'
import Webhooks from './Routes/RoomBookings/Webhooks.jsx'
import GetPeople from './Routes/Search/GetPeople.jsx'
import GetDataCourses from './Routes/Timetable/GetDataCourses.jsx'
import GetDataCoursesModules from './Routes/Timetable/GetDataCoursesModules.jsx'
import GetDataDepartments from './Routes/Timetable/GetDataDepartments.jsx'
import GetDataModules from './Routes/Timetable/GetDataModules.jsx'
import GetPersonalTimetable from './Routes/Timetable/GetPersonalTimetable.jsx'
import GetTimetableByModules from './Routes/Timetable/GetTimetableByModules.jsx'
import WorkspacesGetImage from './Routes/Workspaces/GetImage.jsx'
import WorkspacesGetLastSensorUpdate from './Routes/Workspaces/GetLastSensorUpdate.jsx'
import WorkspacesGetLiveImage from './Routes/Workspaces/GetLiveImage.jsx'
import WorkspacesGetHistoricalTimeData from './Routes/Workspaces/GetSensorHistoricalTimeData.jsx'
import WorkspacesGetSensors from './Routes/Workspaces/GetSensors.jsx'
import WorkspaceGetSensorsSummary from './Routes/Workspaces/GetSensorSummary.jsx'
import WorkspacesGetSurveys from './Routes/Workspaces/GetSurveys.jsx'
import SectionHeader from './SectionHeader.jsx'
import Sidebar from './Sidebar.jsx'

export default class DocumentationComponent extends React.Component {

  render() {
    return (
      <div>
        <NavBar isScroll={false} />
        <Sidebar />
        <div className="main">
          <Welcome key={`Welcome`} />

          <SectionHeader
            key={`SectionHeaderWelcome`}
            link="oauth"
            title="OAuth"
          />
          <OAuthIntro key={`OAuthIntro`} />
          <Authorise key={`Authorise`} />
          <Token key={`Token`} />
          <UserData key={`UserData`} />
          <StudentNumber key={`StudentNumber`} />

          <SectionHeader
            link="roombookings"
            title="Room Bookings"
            key={`SectionHeaderRoomBookings`}
          />
          <GetRooms key={`GetRooms`} />
          <GetBookings key={`GetBookings`} />
          <GetEquiment key={`GetEquiment`} />
          <GetFreeRooms key={`GetFreeRooms`} />
          <Webhooks key={`Webhooks`} />

          <SectionHeader
            link="search"
            title="Search"
            key={`SectionHeaderSearch`}
          />
          <GetPeople key={`GetPeople`} />

          <SectionHeader
            link="timetable"
            title="Timetable"
            key={`SectionHeaderTimetable`}
          />
          <GetPersonalTimetable key={`GetPersonalTimetable`} />
          <GetTimetableByModules key={`GetTimetableByModules`} />
          <GetDataDepartments key={`GetDataDepartments`} />
          <GetDataModules key={`GetDataModules`} />
          <GetDataCourses key={`GetDataCourses`} />
          <GetDataCoursesModules key={`GetDataCoursesModules`} />

          <SectionHeader
            link="resources"
            title="Resources"
            key={`SectionHeaderResources`}
          />
          <DesktopAvailability key={`DesktopAvailability`} />

          <SectionHeader
            link="workspaces"
            title="Workspaces"
            key={`SectionHeaderWorkspaces`}
          />
          <WorkspacesGetSurveys key={`WorkspacesGetSurveys`} />
          <WorkspacesGetSensors key={`WorkspacesGetSensors`} />
          <WorkspacesGetHistoricalTimeData
            key={`WorkspacesGetHistoricalTimeData`}
          />
          <WorkspacesGetLastSensorUpdate
            key={`WorkspacesGetLastSensorUpdate`}
          />
          <WorkspaceGetSensorsSummary key={`WorkspaceGetSensorsSummary`} />
          <WorkspacesGetImage key={`WorkspacesGetImage`} />
          <WorkspacesGetLiveImage key={`WorkspacesGetLiveImage`} />

          <GetInvolved key={`GetInvolved`} />
        </div>
      </div>
    )
  }

}
