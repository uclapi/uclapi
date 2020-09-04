// React
// Images
// Room Buddy
import roombuddylogo from 'Images/marketplace/roombuddy/logo.png'
import rbscrn1 from 'Images/marketplace/roombuddy/screenshot_1.png'
import rbscrn2 from 'Images/marketplace/roombuddy/screenshot_2.png'
import rbscrn3 from 'Images/marketplace/roombuddy/screenshot_3.png'
// UCL Assistant
import uclassistantlogo from 'Images/marketplace/uclassistant/logo.png'
import ucascr1 from 'Images/marketplace/uclassistant/screenshot_1.png'
import ucascr2 from 'Images/marketplace/uclassistant/screenshot_2.png'
import ucascr3 from 'Images/marketplace/uclassistant/screenshot_3.png'
// UCLCSSA App
import uclcssalogodark from 'Images/marketplace/uclcssa/logodark.png'
import uclcssalogolight from 'Images/marketplace/uclcssa/logolight.png'
import ucsscr1 from 'Images/marketplace/uclcssa/screenshot_1.png'
import ucsscr2 from 'Images/marketplace/uclcssa/screenshot_2.png'
import ucsscr3 from 'Images/marketplace/uclcssa/screenshot_3.png'
import ucsscr4 from 'Images/marketplace/uclcssa/screenshot_4.png'
import unikomdesktop1 from 'Images/marketplace/unikomet/desktop_screenshot_1.png'
import unikomdesktop2 from 'Images/marketplace/unikomet/desktop_screenshot_2.png'
import unikomdesktop3 from 'Images/marketplace/unikomet/desktop_screenshot_3.png'
import unikomdesktop4 from 'Images/marketplace/unikomet/desktop_screenshot_4.png'
// Unikomet
import unikometlogo from 'Images/marketplace/unikomet/logo.png'
import unikom1 from 'Images/marketplace/unikomet/screenshot_1.png'
import unikom2 from 'Images/marketplace/unikomet/screenshot_2.png'
import unikom3 from 'Images/marketplace/unikomet/screenshot_3.png'
// Common Components
import { Button, TextView } from 'Layout/Items.jsx'
import React from 'react'
import { Carousel } from "react-responsive-carousel"

// Application config
const roombuddydescription = (
  <div className="roombuddy-full-description"
    style={{ "display": `inline-block` }}
  >
    <TextView heading={`5`}
      text={`Finding a place to get your work done 
    can be hard. Every place you've thought of is somehow already filled 
    up: the libraries, the study pods, the benches outside the Print Room 
    Café, etc.`}
    />
    <TextView heading={`5`}
      text={`Room Buddy makes use of UCL API to find
    and direct you to open study spaces that aren't widely known.`}
    />
    <TextView heading={`5`}
      text={`It's simple: install the app, sign in 
    with your UCL ID, and get going to the closest available space to
    your current location!`}
    />
    <TextView heading={`5`}
      text={`UCL Room Buddy was built with the 
    UCL API, which gives student developers programmatic access to UCL's
     data in order to improve the UCL experience for everyone.`}
    />
    <TextView heading={`5`}
      text={`Want to contribute to room buddy? 
    Submit a pull request:`}
    />
    <Button type={`alternate`}
      style={{
        'margin': `auto`,
        'display': `flex`,
      }}
      link={`https://github.com/uclapi/ucl-assistant-app`}
    >
      VISIT GITHUB
    </Button>
    <TextView
      heading={`5`}
      text={`This app and its platform have been 
    built by the UCL API Team, a group of students working with UCL's 
    Information Services Division (ISD) to provide students with a brand 
    new ecosystem that allows anyone within the UCL Community to build 
    apps with UCL data. Interested in building an app just like UCL 
    Room Buddy yourself? Head over to uclapi.com and log in with your 
    UCL Account.`}
    />
  </div>
)

const uclassistantdescription = (
  <div className="uclassistant-full-description"
    style={{ "display": `inline-block` }}
  >
    <TextView heading={`5`}
      text={`✨✨A brand new and beautiful app 
    to manage your student life at UCL!✨✨`}
    />
    <TextView heading={`5`}
      text={`✅ View your personal timetable and 
    get instant directions to your lectures.`}
    />
    <TextView heading={`5`}
      text={`✅ Check the availability of all 
    UCL libraries and study spaces, including in
     the new Student Centre. Want to know which floor or room has the 
     most seats free? You now have that
     information right in the palm of your hand! Not sure which seats 
     are free? No problem! Just use the live
     seating maps to see every seat that has been unoccupied for over 
     half an hour on whichever library 
     floor you choose`}
    />
    <TextView heading={`5`}
      text={`✅ Search for members of the UCL 
    community, including students and lecturers,
     and tap to email them. Nice and easy!`}
    />
    <TextView heading={`5`}
      text={`✅ Find every centrally bookable room 
    t UCL, see how big it is and whether it is 
     currently in use, and then tap to navigate right there.`}
    />
    <TextView heading={`5`}
      text={`✅ Made with love 💖 by and for 
    students`}
    />
    <TextView heading={`5`}
      text={`✅ Fully open source. Got feedback, 
    suggestions or even some new code to improve 
     the app? We welcome it:`}
    />
    <Button type={`alternate`}
      isCentered
      style={{
        'margin': `auto`,
        'display': `flex`,
      }}
      link={`https://github.com/uclapi/ucl-assistant-app`}
    >
      VISIT GITHUB
    </Button>
    <TextView heading={`5`}
      text={`This app and its platform have 
    been built by the UCL API Team, a group of students
     working with UCL's Information Services Division (ISD) to 
     provide students with a brand new ecosystem that allows
     anyone within the UCL Community to build apps with UCL data. 
     Interested in building an app just like UCL Assistant
     yourself? Head over to uclapi.com and log in with your UCL Account.`}
    />
  </div>
)

const uclcssadescription = (
  <div className="uclassistant-full-description"
    style={{ "display": `inline-block` }}
  >
    <iframe width="420"
      height="315"
      style={{
        "margin": `20px 0`,
        'width': `100%`,
      }}
      src="https://www.youtube.com/embed/0Q3WJDENFAM"
    >
    </iframe>
    <TextView heading={`2`}
      text={`Realtime studyspaces seating map`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`
      You can view a live map showing which seats are available on
      each floor in the library. You no longer need walk around the
      library hunting for a vacant seat.`}
    />
    <TextView heading={`2`}
      text={`Timetabling`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`You can 
      view your personal timetable within WeChat. This is much easier then 
      using UCL Go for your timetable.`}
    />
    <TextView heading={`2`}
      text={`Questions and Answers`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`The question and answer section answers 
      common questions such as:`}
    />
    <TextView heading={`5`}
      text={`What is there to do on the weekend in London?`}
    />
    <TextView heading={`5`}
      text={`What good restraunts are there in London?`}
    />
    <TextView heading={`5`}
      text={`What are the best locations in London to rent for students?`}
    />
    <TextView heading={`5`}
      text={`And much more!`}
    />
    <TextView heading={`2`}
      text={`Memes`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`An area dedicated to creating 
      memes of teachers or classmates`}
    />
    <TextView heading={`2`}
      text={`Name search`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`The name search feature 
      allows you to find the name and email of your lecturers or friends. This 
      helps you contact anybody at UCL.`}
    />
    <TextView heading={`2`}
      text={`Job search information`}
      style={{ "textDecoration": `underline` }}
    />
    <TextView heading={`5`}
      text={`The Job search information is a whole 
      section dedicated 
      to providing information about internships and 
      resume advice. It is updated with recruitment information and 
      application deadlines for major companies on a regular basis.`}
    />
    <TextView heading={`5`}
      text={`The internship opportunities come to you!`}
    />
  </div>
)

const unikometdescription = (
  <div className="unikomet-full-description"
    style={{ "display": `inline-block` }}
  >
    <TextView heading={`5`}
      text={`Unikomet is a platform built by students at UCL to enable other students
      to post anonymous reviews of their modules. Through the website all students at UCL
      can visit and post reviews and ratings for other students to see. This allows future
      students to make more informed decisions about`}
    />
    <TextView heading={`5`}
      text={`Unikomet can be used by students to review their modules, 
      as well as see reviews from other students. Some ways the reviews
      can be helpful are: `}
    />
    <TextView heading={`5`}
      text={`🚀 The student satisfaction ratings!`}
    />
    <TextView heading={`5`}
      text={`🚀 The personal student reviews!`}
    />
    <TextView heading={`5`}
      text={`🚀 A platform for giving student cohorts a voice!`}
    />
    <div className="default tablet">
      <Carousel
        showThumbs={false}
        showArrows
        showIndicators
        showStatus
        infiniteLoop
      >
        <div key={`unikomet-desktop-image-1`}>
          <img
            src={unikomdesktop1}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Search`}</p>
        </div>
        <div key={`unikomet-desktop-image-2`}>
          <img
            src={unikomdesktop2}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Rate`}</p>
        </div>
        <div key={`unikomet-desktop-image-3`}>
          <img
            src={unikomdesktop3}
            width="100%"
            height="auto"
          />
          <p className="legend">{`View Reviews`}</p>
        </div>
        <div key={`unikomet-desktop-image-4`}>
          <img
            src={unikomdesktop4}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Sort by department`}</p>
        </div>
      </Carousel>
    </div>
    <TextView heading={`5`}
      text={`We believe Unikomet can be very helpful for many students, from those
       who are looking for that extra guidance to pick the right modules, to applicants 
       who want to find out more about student satisfaction in the modules
       they're interested in. And importantly, Unikomet can also be an extremely 
       valuable tool through which students at large can express their opinions about
       something that is so important.`}
    />
    <TextView heading={`5`}
      text={`Made with love 💖 by and for 
    students`}
    />
    {/* <Button type={`alternate`}
      isCentered
      text={`VISIT GITHUB`}
      style={{
        'margin': `auto`,
        'display': `flex`,
      }}
      link={`https://github.com/uclapi/ucl-assistant-app`}
    /> */}
  </div>
)

export const allApps = {
  "uclroombuddy": {
    "name": `UCL Room Buddy`,
    "id": `uclroombuddy`,
    "category": `roombookings`,
    "description": `Find the closest free room at UCL`,
    "logolight": roombuddylogo,
    "logodark": roombuddylogo,
    "detailedDescription": roombuddydescription,
    "developerContact": `https://github.com/wilhelmklopp`,
    "links": [],
    "screenshots": [
      {
        name: `Room Buddy`,
        img: rbscrn1,
      },
      {
        name: `See the free rooms`,
        img: rbscrn2,
      },
      {
        name: `Navigate to UCL rooms`,
        img: rbscrn3,
      },
    ],
  },
  "uclassistant": {
    "name": `UCL Assistant`,
    "id": `uclassistant`,
    "category": `productivity`,
    "description": `An app to manage your student life at UCL`,
    "logolight": uclassistantlogo,
    "logodark": uclassistantlogo,
    "detailedDescription": uclassistantdescription,
    "developerContact": `https://github.com/uclapi`,
    "links": [
      {
        "name": `android`,
        "link": `https://play.google.com/store/apps/details?id=`
          + `com.uclapi.uclassistant&hl=en_GB`,
      },
      {
        "name": `apple`,
        "link": `https://apps.apple.com/us/app/ucl-assistant/id1462767418`,
      },
    ],
    "screenshots": [
      {
        name: `UCL Assistant`,
        img: ucascr1,
      },
      {
        name: `View your timetable`,
        img: ucascr2,
      },
      {
        name: `Find study spaces`,
        img: ucascr3,
      },
    ],
  },
  "uclcssa": {
    "name": `CSSA App`,
    "id": `uclcssa`,
    "category": `productivity`,
    "description": `Six practical functions to help students`,
    "logolight": uclcssalogolight,
    "logodark": uclcssalogodark,
    "detailedDescription": uclcssadescription,
    // eslint-disable-next-line no-secrets/no-secrets
    "developerContact": `https://mp.weixin.qq.com/s/ndkYgEFwlATvIIcHONG2uA`,
    "links": [
      {
        "name": `WeChat`,
        // eslint-disable-next-line no-secrets/no-secrets
        "link": `https://mp.weixin.qq.com/s/uij8Z05hB7aKJm0Ln0SI8g`,
      },
      {
        "name": `Website`,
        "link": `https://uclcssa.cn/`,
      },
    ],
    "screenshots": [
      {
        name: `UCL CSSA`,
        img: ucsscr1,
      },
      {
        name: `Your profile`,
        img: ucsscr2,
      },
      {
        name: `Find empty library seats`,
        img: ucsscr3,
      },
      {
        name: `View your timetable`,
        img: ucsscr4,
      },
    ],
  },
  "unikomet": {
    "name": `Unikomet`,
    "id": `unikomet`,
    "category": `productivity`,
    "description": `Student reviews of UCL modules`,
    "logolight": unikometlogo,
    "logodark": unikometlogo,
    "detailedDescription": unikometdescription,
    // eslint-disable-next-line no-secrets/no-secrets
    "developerContact": `https://unikomet.com/contact`,
    "links": [
      {
        "name": `Website`,
        "link": `https://unikomet.com`,
      },
    ],
    "screenshots": [
      {
        name: `Search`,
        img: unikom1,
      },
      {
        name: `Reviews`,
        img: unikom2,
      },
      {
        name: `Ratings`,
        img: unikom3,
      },
    ],
  },
}

export default {
  allApps,
}