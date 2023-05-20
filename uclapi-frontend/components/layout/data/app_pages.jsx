// Common Components
import { Button } from 'rsuite'
import { Carousel } from "react-responsive-carousel"

// Application config
const roombuddydescription = (
  <div style={{ "margin-top": `2em` }}>
    <p className='description'>
      Finding a place to get your work done
      can be hard. Every place you've thought of is somehow already filled
      up: the libraries, the study pods, the benches outside the Print Room
      Café, etc.
    </p>

    <p className='description'>
      Room Buddy makes use of UCL API to find
      and direct you to open study spaces that aren't widely known.
    </p>

    <p className='description'>
      It's simple: install the app, sign in
      with your UCL ID, and get going to the closest available space to
      your current location!
    </p>

    <p className='description'>
      UCL Room Buddy was built with the
      UCL API, which gives student developers programmatic access to UCL's
     data in order to improve the UCL experience for everyone.`
    </p>

    <p className='description'>
      Want to contribute to room buddy? Submit a pull request:
    </p>

    <Button
      style={{'margin': `auto`,'display': `flex`, width: '110px'}}
      href={`https://github.com/uclapi/ucl-assistant-app`}
    >
      VISIT GITHUB
    </Button>
    <br/>
    <p className='description'>
      This app and its platform have been
      built by the UCL API Team, a group of students working with UCL's
      Information Services Division (ISD) to provide students with a brand
      new ecosystem that allows anyone within the UCL Community to build
      apps with UCL data. Interested in building an app just like UCL
      Room Buddy yourself? Head over to uclapi.com and log in with your
      UCL Account.
    </p>
  </div>
)

const uclassistantdescription = (
  <div style={{ "margin-top": `2em` }}>
    <p className='description'>
      ✨✨A brand new and beautiful app
      to manage your student life at UCL!✨✨
    </p>
    <p className='description'>
      ✅ View your personal timetable and
      get instant directions to your lectures.
    </p>
    <p className='description'>
      ✅ Check the availability of all
      UCL libraries and study spaces, including in
      the new Student Centre. Want to know which floor or room has the
      most seats free? You now have that
      information right in the palm of your hand! Not sure which seats
      are free? No problem! Just use the live
      seating maps to see every seat that has been unoccupied for over
      half an hour on whichever library
      floor you choose
    </p>
    <p className='description'>
      ✅ Search for members of the UCL
      community, including students and lecturers,
      and tap to email them. Nice and easy!
    </p>
    <p className='description'>
      ✅ Find every centrally bookable room
      t UCL, see how big it is and whether it is
      currently in use, and then tap to navigate right there.
    </p>
    <p className='description'>
      ✅ Made with love 💖 by and for
      students
    </p>
    <p className='description'>
      ✅ Fully open source. Got feedback,
      suggestions or even some new code to improve
      the app? We welcome it:
    </p>

    <Button
      style={{'margin': `auto`,'display': `flex`, width: '110px'}}
      href={`https://github.com/uclapi/ucl-assistant-app`}
    >
      VISIT GITHUB
    </Button>
    <br/>
    <p className='description'>
      This app and its platform have
      been built by the UCL API Team, a group of students
      working with UCL's Information Services Division (ISD) to
      provide students with a brand new ecosystem that allows
      anyone within the UCL Community to build apps with UCL data.
      Interested in building an app just like UCL Assistant
      yourself? Head over to uclapi.com and log in with your UCL Account.
    </p>
  </div>
)

const uclcssadescription = (
   <div style={{ "margin-top": `2em` }}>
    <iframe width="420"
      height="315"
      style={{
        "margin": `20px 0`,
        'width': `100%`,
      }}
      src="https://www.youtube.com/embed/0Q3WJDENFAM"
    >
    </iframe>
    <h2 style={{ "textDecoration": `underline` }}>
      Realtime studyspaces seating map
    </h2>
    <p className='description'>
      You can view a live map showing which seats are available on
      each floor in the library. You no longer need walk around the
      library hunting for a vacant seat.
    </p>

    <h2 style={{ "textDecoration": `underline` }}>
      Timetabling
    </h2>
    <p className='description'>
    You can
      view your personal timetable within WeChat. This is much easier then
      using UCL Go for your timetable.
    </p>

    <h2 style={{ "textDecoration": `underline` }}>
      Questions and Answers
    </h2>
    <p className='description'>
      The question and answer section answers
      common questions such as:
      <ul>
        <li>
          What is there to do on the weekend in London?
        </li>
        <li>
          What good restraunts are there in London?
        </li>
        <li>
          What are the best locations in London to rent for students?
        </li>
        <li>
          And much more!
        </li>
      </ul>
    </p>

    <h2 style={{ "textDecoration": `underline` }}>
      Memes
    </h2>
    <p className='description'>
      An area dedicated to creating memes of teachers or classmates
    </p>

    <h2 style={{ "textDecoration": `underline` }}>
      Name search
    </h2>
    <p className='description'>
      The name search feature
      allows you to find the name and email of your lecturers or friends. This
      helps you contact anybody at UCL.
    </p>

    <h2 style={{ "textDecoration": `underline` }}>
      Job search information
    </h2>
    <p className='description'>
      The Job search information is a whole section dedicated
      to providing information about internships and
      resume advice. It is updated with recruitment information and
      application deadlines for major companies on a regular basis.
    </p>
    <p className='description'>
      The internship opportunities come to you!
    </p>
  </div>
)

const unikometdescription = (
  <div style={{ "margin-top": `2em` }}>
    <p className="description">
      Unikomet is a platform built by students at UCL to enable other students
      to post anonymous reviews of their modules. Through the website all
      students at UCL can visit and post reviews and ratings for other students
      to see. This allows future students to make more informed decisions about
    </p>
    <p className="description">
      Unikomet can be used by students to review their modules, as well as see
      reviews from other students. Some ways the reviews can be helpful are:
    </p>
    <ul className="description" style={{color: 'white'}}>
      <li>🚀 The student satisfaction ratings!</li>
      <li>🚀 The personal student reviews!</li>
      <li>🚀 A platform for giving student cohorts a voice!</li>
    </ul>

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
            src={'/marketplace/unikomet/desktop_screenshot_1.png'}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Search`}</p>
        </div>
        <div key={`unikomet-desktop-image-2`}>
          <img
            src={'/marketplace/unikomet/desktop_screenshot_2.png'}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Rate`}</p>
        </div>
        <div key={`unikomet-desktop-image-3`}>
          <img
            src={'/marketplace/unikomet/desktop_screenshot_3.png'}
            width="100%"
            height="auto"
          />
          <p className="legend">{`View Reviews`}</p>
        </div>
        <div key={`unikomet-desktop-image-4`}>
          <img
            src={'/marketplace/unikomet/desktop_screenshot_4.png'}
            width="100%"
            height="auto"
          />
          <p className="legend">{`Sort by department`}</p>
        </div>
      </Carousel>
    </div>

    <br />
    <p className='description'>
      We believe Unikomet can be very helpful for many students, from those
      who are looking for that extra guidance to pick the right modules, to applicants
      who want to find out more about student satisfaction in the modules
      they're interested in. And importantly, Unikomet can also be an extremely
      valuable tool through which students at large can express their opinions about
      something that is so important.
    </p>
    <p className='description'>
      Made with love 💖 by and for students
    </p>
  </div>
);

export const allApps = {
  "uclroombuddy": {
    "name": `UCL Room Buddy`,
    "id": `uclroombuddy`,
    "category": `roombookings`,
    "description": `Find the closest free room at UCL`,
    "logolight": '/marketplace/roombuddy/logo.png',
    "logodark": '/marketplace/roombuddy/logo.png',
    "detailedDescription": roombuddydescription,
    "developerContact": `https://github.com/wilhelmklopp`,
    "links": [],
    "screenshots": [
      {
        name: `Room Buddy`,
        img: '/marketplace/roombuddy/screenshot_1.png',
      },
      {
        name: `See the free rooms`,
        img: '/marketplace/roombuddy/screenshot_2.png',
      },
      {
        name: `Navigate to UCL rooms`,
        img: '/marketplace/roombuddy/screenshot_3.png',
      },
    ],
  },
  "uclassistant": {
    "name": `UCL Assistant`,
    "id": `uclassistant`,
    "category": `productivity`,
    "description": `An app to manage your student life at UCL`,
    "logolight": '/marketplace/uclassistant/logo.png',
    "logodark": '/marketplace/uclassistant/logo.png',
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
        img: '/marketplace/uclassistant/screenshot_1.png',
      },
      {
        name: `View your timetable`,
        img: '/marketplace/uclassistant/screenshot_2.png',
      },
      {
        name: `Find study spaces`,
        img: '/uclassistant/screenshot_3.png',
      },
    ],
  },
  "uclcssa": {
    "name": `CSSA App`,
    "id": `uclcssa`,
    "category": `productivity`,
    "description": `Six practical functions to help students`,
    "logolight": '/marketplace/uclcssa/logolight.png',
    "logodark": '/marketplace/uclcssa/logodark.png',
    "detailedDescription": uclcssadescription,
    "developerContact": `https://mp.weixin.qq.com/s/ndkYgEFwlATvIIcHONG2uA`,
    "links": [
      {
        "name": `WeChat`,
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
        img: '/marketplace/uclcssa/screenshot_1.png',
      },
      {
        name: `Your profile`,
        img: '/marketplace/uclcssa/screenshot_2.png',
      },
      {
        name: `Find empty library seats`,
        img: '/marketplace/uclcssa/screenshot_3.png',
      },
      {
        name: `View your timetable`,
        img: '/marketplace/uclcssa/screenshot_4.png',
      },
    ],
  },
  "unikomet": {
    "name": `Unikomet`,
    "id": `unikomet`,
    "category": `productivity`,
    "description": `Student reviews of UCL modules`,
    "logolight": '/marketplace/unikomet/logo.png',
    "logodark": '/marketplace/unikomet/logo.png',
    "detailedDescription": unikometdescription,
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
        img: '/marketplace/unikomet/screenshot_1.png',
      },
      {
        name: `Reviews`,
        img: '/marketplace/unikomet/screenshot_2.png',
      },
      {
        name: `Ratings`,
        img: '/marketplace/unikomet/screenshot_3.png',
      },
    ],
  },
}

export default {
  allApps,
}
