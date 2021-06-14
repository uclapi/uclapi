import React from 'react'
import renderer from 'react-test-renderer'
import LogInLayout from '../src/components/appsettings/LogInLayout'
import AccordionIcon from "../src/components/dashboard/AccordionIcon"
import App from "../src/components/dashboard/App"
import SettingsLayout from "../src/components/appsettings/SettingsLayout"
import Navbar from "../src/components/dashboard/navbar"
import Authorise from "../src/pages/Authorise/Authorise"
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
