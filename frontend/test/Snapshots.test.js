import React from 'react'
import renderer from 'react-test-renderer'
import LogInLayout from '../src/components/appsettings/LogInLayout'
import AccordionIcon from "../src/components/dashboard/AccordionIcon"
import App from "../src/components/dashboard/App"
import SettingsLayout from "../src/components/appsettings/SettingsLayout"
import Navbar from "../src/components/dashboard/navbar"
import MostPopularMethod from "../src/components/documentation/Routes/Analytics/MostPopularMethod"
import MostPopularService from "../src/components/documentation/Routes/Analytics/MostPopularService"
import RemainingQuota from "../src/components/documentation/Routes/Analytics/RemainingQuota"
import TotalNumRequests from "../src/components/documentation/Routes/Analytics/TotalNumRequests"
import UsersPerApp from "../src/components/documentation/Routes/Analytics/UsersPerApp"
import UsersPerAppPerDept from "../src/components/documentation/Routes/Analytics/UsersPerAppPerDept"
import Authorise from "../src/components/documentation/Routes/OAuth/Authorise"
import OAuthIntro from "../src/components/documentation/Routes/OAuth/OAuthIntro"
import StudentNumber from "../src/components/documentation/Routes/OAuth/StudentNumber"
import Token from "../src/components/documentation/Routes/OAuth/Token"
import UserData from "../src/components/documentation/Routes/OAuth/UserData"
import DesktopAvailability from "../src/components/documentation/Routes/Resources/DesktopAvailability"
import GetBookings from "../src/components/documentation/Routes/RoomBookings/GetBookings"
import GetEquipment from "../src/components/documentation/Routes/RoomBookings/GetEquipment"
import GetFreeRooms from "../src/components/documentation/Routes/RoomBookings/GetFreeRooms"
import GetRooms from "../src/components/documentation/Routes/RoomBookings/GetRooms"
import Webhooks from "../src/components/documentation/Routes/RoomBookings/Webhooks"
import GetPeople from "../src/components/documentation/Routes/Search/GetPeople"
import GetDataCourses from "../src/components/documentation/Routes/Timetable/GetDataCourses"
import GetDataCoursesModules from "../src/components/documentation/Routes/Timetable/GetDataCoursesModules"
import GetDataDepartments from "../src/components/documentation/Routes/Timetable/GetDataDepartments"
import GetDataModules from "../src/components/documentation/Routes/Timetable/GetDataModules"
import GetPersonalTimetable from "../src/components/documentation/Routes/Timetable/GetPersonalTimetable"
import GetTimetableByModules from "../src/components/documentation/Routes/Timetable/GetTimetableByModules"
import GetImage from "../src/components/documentation/Routes/Workspaces/GetImage"
import GetLastSensorUpdate from "../src/components/documentation/Routes/Workspaces/GetLastSensorUpdate"
import GetLiveImage from "../src/components/documentation/Routes/Workspaces/GetLiveImage"
import GetSensorHistoricalTimeData from "../src/components/documentation/Routes/Workspaces/GetSensorHistoricalTimeData"
import GetSensors from "../src/components/documentation/Routes/Workspaces/GetSensors"
import GetSensorSummary from "../src/components/documentation/Routes/Workspaces/GetSensorSummary"
import GetSurveys from "../src/components/documentation/Routes/Workspaces/GetSurveys"
import Welcome from "../src/components/documentation/Meta/Welcome"
import GetInvolved from "../src/components/documentation/GetInvolved/GetInvolved"
import MenuContent from "../src/components/documentation/Sidebar/MenuContent"
import Section from "../src/components/documentation/Sidebar/Section"
import Sidebar from "../src/components/documentation/Sidebar"
import Topic from "../src/components/documentation/Topic"
import Cell from "../src/components/documentation/Cell"
import LanguageTabs from "../src/components/documentation/LanguageTabs"
import SectionHeader from "../src/components/documentation/SectionHeader"
import Table from "../src/components/documentation/Table"
import Dashboard from "../src/pages/Dashboard/Dashboard"
import HomePage from "../src/pages/Home/HomePage"
import Marketplace from "../src/pages/Marketplace/Marketplace"
import NotFoundPage from "../src/pages/404/404"
import InternalServerErrorPage from "../src/pages/500/500"
import AboutPage from "../src/pages/AboutPage/AboutPage"
import AppSettings from "../src/pages/AppSettings/AppSettings"
import Documentation from "../src/pages/Documentation/Documentation"
import Warning from "../src/pages/Warning/Warning"

describe(`Components`, () => {

  describe(`Appsettings`, () => {
    it(`LogInLayout`, () => {
      const tree = renderer.create(<LogInLayout url="https://www.uclapi.com"/>).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`SettingsLayout`, () => {
      const tree = renderer.create(
        <SettingsLayout authorised_apps={[`app1`]}/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })
  })

  describe(`Dashboard`, () => {
    it(`AccordionIcon`, () => {
      const tree = renderer.create(
        <AccordionIcon isActive/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`App`, () => {
      const tree = renderer.create(
        <App app={{
          "name": `sample-project`,
          "id": `sample-log`,
          "token": `uclapi-token`,
          "created": `2020-10-21T11:15:46.932`,
          "updated": `2020-10-21T11:16:38.648`,
          "oauth": {
            "client_id": `123.456`,
            "client_secret": `secrets`,
            "callback_url": ``,
            "scopes": [
              {
                "name": `timetable`,
                "description": `Personal Timetable`,
                "enabled": true,
              },
              {
                "name": `student_number`,
                "description": `Student Number`,
                "enabled": false,
              },
            ],
          },
          "webhook": {
            "verification_secret": `secrets`,
            "url": ``,
            "siteid": ``,
            "roomid": ``,
            "contact": ``,
          },
          "analytics": {
            "requests": 392,
            "remaining_quota": 10000,
            "users": 0,
            "users_per_dept": [],
          },
        }}
        />,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`Navbar`, () => {
      const tree = renderer.create(
        <Navbar/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })
  })

  describe(`Documentation`, () => {
    describe(`GetInvolved`, () => {
      it(`GetInvolved`, () => {
        const tree = renderer.create(
          <GetInvolved/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })
    })

    describe(`Meta`, () => {
      it(`Welcome`, () => {
        const tree = renderer.create(
          <Welcome/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })
    })

    describe(`Routes`, () => {
      const routes = {
        "Analytics": [[`MostPopularMethod`, MostPopularMethod], [`MostPopularService`, MostPopularService],
          [`RemainingQuota`, RemainingQuota], [`TotalNumRequests`, TotalNumRequests], [`UsersPerApp`, UsersPerApp],
          [`UsersPerAppPerDept`, UsersPerAppPerDept]],
        "OAuth": [[`Authorise`, Authorise], [`OAuthIntro`, OAuthIntro], [`StudentNumber`, StudentNumber],
          [`Token`, Token], [`UserData`, UserData]],
        "Resources": [[`DesktopAvaliability`, DesktopAvailability]],
        "RoomBookings": [[`GetBookings`, GetBookings], [`GetEquipment`, GetEquipment], [`GetFreeRooms`, GetFreeRooms],
          [`GetRooms`, GetRooms], [`Webhooks`, Webhooks]],
        "Search": [[`GetPeople`, GetPeople]],
        "Timetable": [[`GetDataCourses`, GetDataCourses], [`GetDataCoursesModule`, GetDataCoursesModules],
          [`GetDataDepartments`, GetDataDepartments], [`GetDataModules`, GetDataModules],
          [`GetPersonalTimetable`, GetPersonalTimetable], [`GetTimetableByModules`, GetTimetableByModules]],
        "Workspaces": [[`GetImage`, GetImage], [`GetLastSensorUpdate`, GetLastSensorUpdate],
          [`GetLiveImage`, GetLiveImage], [`GetSensorHistoricalTimeData`, GetSensorHistoricalTimeData],
          [`GetSensors`, GetSensors], [`GetSensorSummary`, GetSensorSummary], [`GetSurveys`, GetSurveys]],
      }

      for (const route in routes) {
        describe(route, () => {
          it.each(routes[route])(`%s`, (name, component) => {
            const tree = renderer.create(
              <component/>,
            ).toJSON()
            expect(tree).toMatchSnapshot()
          })
        })
      }
    })

    describe(`Sidebar`, () => {
      it(`MenuContent`, () => {
        const tree = renderer.create(
          <MenuContent/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })

      it(`Section`, () => {
        const tree = renderer.create(
          <Section/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })

      it(`Sidebar`, () => {
        const tree = renderer.create(
          <Sidebar/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })
    })

    describe(`Topic`, () => {
      it(`Topic`, () => {
        const tree = renderer.create(
          <Topic/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })
    })

    it(`Cell`, () => {
      const tree = renderer.create(
        <Cell/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`LanguageTabs`, () => {
      const tree = renderer.create(
        <LanguageTabs/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`SectionHeader`, () => {
      const tree = renderer.create(
        <SectionHeader/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })

    it(`Table`, () => {
      const tree = renderer.create(
        <Table/>,
      ).toJSON()
      expect(tree).toMatchSnapshot()
    })
  })
})

describe(`Pages`, () => {
  const pages = {
    "Authorise": [[`Authorise`, Authorise]],
    "Dashboard": [[`Dashboard`, Dashboard]],
    "Home": [[`HomePage`, HomePage]],
    "Marketplace": [[`Marketplace`, Marketplace]],
    "404": [[`NotFoundPage`, NotFoundPage]],
    "505": [[`InternalServerErrorPage`, InternalServerErrorPage]],
    "AboutPage": [[`AboutPage`, AboutPage]],
    "AppSettings": [[`AppSettings`, AppSettings]],
    "Documentation": [[`Documentation`, Documentation]],
    "Warning": [[`Warning`, Warning]],
  }

  for (const page in pages) {
    describe(page, () => {
      // eslint-disable-next-line sonarjs/no-identical-functions
      it.each(pages[page])(`%s`, (name, component) => {
        const tree = renderer.create(
          <component/>,
        ).toJSON()
        expect(tree).toMatchSnapshot()
      })
    })
  }
})
