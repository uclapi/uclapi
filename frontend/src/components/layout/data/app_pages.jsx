// React
import React from 'react'

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
// UCL Assistant
import uclcssalogo from 'Images/marketplace/uclcssa/logo.jpg'
import ucsscr1 from 'Images/marketplace/uclcssa/screenshot_1.jpg'
import ucsscr2 from 'Images/marketplace/uclcssa/screenshot_2.jpg'
import ucsscr3 from 'Images/marketplace/uclcssa/screenshot_3.jpg'
// Common Components
import { ButtonView, TextView } from 'Layout/Items.jsx'

// Application config
const roombuddydescription = (
  <div className="roombuddy-full-description" 
    style={ { "display": `inline-block`} }
  >
   <TextView heading={`3`} text={`Finding a place to get your work done 
    can be hard. Every place you've thought of is somehow already filled 
    up: the libraries, the study pods, the benches outside the Print Room 
    Café...`}
   />
   <TextView heading={`3`} text={`Room Buddy makes use of UCL API to find
    and direct you to open study spaces that aren't widely known. These 
    rooms are scarcely booked up for timetables and sit waiting for you to
     grace them with your glory.`}
   />
   <TextView heading={`3`} text={`It's simple: install the app, sign in 
   with your UCL ID, and get going to the closest available space to
    your current location!`}
   />
   <TextView heading={`3`} text={`UCL Room Buddy was built with the 
    UCL API, which gives student developers programmatic access to UCL's
     data in order to improve the UCL experience for everyone.`}
   />
   <TextView heading={`3`} text={`Want to contribute to room buddy? 
    Submit a pull request:`}
   />
   <ButtonView type={`alternate`} text={`VISIT GITHUB`} 
     style={ { "margin" : `0 0 20px 0` } } 
     link={`https://github.com/uclapi/ucl-assistant-app`}
   />
   <TextView heading={`3`} text={`This app and its platform have been 
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
    style={ {"display": `inline-block` } }
  >
   <TextView heading={`3`} text={`✨✨A brand new and beautiful app 
    to manage your student life at UCL!✨✨`}
   />
   <TextView heading={`3`} text={`✅ View your personal timetable and 
    get instant directions to your lectures.`}
   />
   <TextView heading={`3`} text={`✅ Check the availability of all 
    UCL libraries and study spaces, including in
     the new Student Centre. Want to know which floor or room has the 
     most seats free? You now have that
     information right in the palm of your hand! Not sure which seats 
     are free? No problem! Just use the live
     seating maps to see every seat that has been unoccupied for over 
     half an hour on whichever library 
     floor you choose`}
   />
   <TextView heading={`3`} text={`✅ Search for members of the UCL 
    community, including students and lecturers,
     and tap to email them. Nice and easy!`}
   />
   <TextView heading={`3`} text={`✅ Find every centrally bookable room 
    t UCL, see how big it is and whether it is 
     currently in use, and then tap to navigate right there.`}
   />
   <TextView heading={`3`} text={`✅ Made with love 💖 by and for 
    students`}
   />
   <TextView heading={`3`} text={`✅ Fully open source. Got feedback, 
    suggestions or even some new code to improve 
     the app? We welcome it:`}
   />
   <ButtonView type={`alternate`} isCentered text={`VISIT GITHUB`} 
     style={ { "margin" : `0 0 20px 0` } } 
     link={`https://github.com/uclapi/ucl-assistant-app`}
   />
   <TextView heading={`3`} text={`This app and its platform have 
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
    style={ {"display": `inline-block` } }
  >
    <TextView heading={`2`} text={`Real-time library seat map`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`This is a feature that you do not 
      get on UCL Go. 
      You can click on specific floors of each library to view a 
      seating map. You no longer
      have to worry about running into the library and discovering 
      there is no space. The
      seating map is updated every 2 minutes reducing the chance of 
      false positives.`}
    />
    <TextView heading={`2`} text={`Timetabling`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`Just log in with UCL and you can 
      view your personal timetable to 
      be able to view your personal timetable using WeChat. This 
      avoids the problems with trying to use UCL Go.`}
    />
    <TextView heading={`2`} text={`Questions and Answers`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`There is a whole section dedicated 
      to answering questions from 
      what to do on the weekend in London all the way to what food to 
      eat and where good places
      to rent are.`}
    />
    <TextView heading={`2`} text={`Memes`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`An area dedicated to creating 
      memes of teachers or classmates during 
      your day for others to enjoy`}
    />
    <TextView heading={`2`} text={`Name search`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`You can use the name search feature 
      to remind yourself of people's names
    or for finding out the name and email of your lecturers. This 
    allows you to always be able to get into contact 
    with both people you meet as well as your lecturers.`}
    />
    <TextView heading={`2`} text={`Job search information`} 
      style={ { "textDecoration": `underline` } }
    />
    <TextView heading={`3`} text={`There is a whole section dedicated 
      to providing information about internships and 
      resume advice. It is updated with recruitment information and 
      timings for major companies on a regular basis. 
      The internship opportunities come to you as opposed to you finding
       the opportunities!`}
    />
  </div>
)

export const allApps = {
  "uclroombuddy": {
    "name": `UCL Room Buddy`,
"id": `uclroombuddy`,
"category": `roombookings`,
"description": `Find the closest free room at UCL`,
"logo": roombuddylogo,
    "detailedDescription": roombuddydescription,
"developerContact": `https://github.com/wilhelmklopp`,
    "links": [],
    "screenshots": [ rbscrn1, rbscrn2, rbscrn3 ],
  },
  "uclassistant": {
    "name": `UCL Assistant`,
"id": `uclassistant`,
"category": `productivity`,
"description": `An app to manage your student life at UCL`,
"logo": uclassistantlogo,
    "detailedDescription": uclassistantdescription, 
    "developerContact": `https://github.com/uclapi`,
    "links": [ 
        {
          "name": `android`, 
          "link": `https://play.google.com/store/apps/details?id=com.
          uclapi.uclassistant&hl=en_GB`,
        },
        {
          "name": `apple`, 
          "link": `https://play.google.com/store/apps/details?id=com.
          uclapi.uclassistant&hl=en_GB`,
        },
    ],
    "screenshots": [ ucascr1, ucascr2, ucascr3 ],
  },
  "uclcssa": {
    "name": `CSSA App`,
"id": `uclcssa`,
"category": `productivity`,
"description": `Six practical functions to help students`,
"logo": uclcssalogo,
    "detailedDescription": uclcssadescription, 
    "developerContact": `https://mp.weixin.qq.com/s/ndkYgEFwlATvIIcHON
    G2uA`,
    "links": [ 
        {
          "name": `web`, 
          "link": `https://mp.weixin.qq.com/s/ndkYgEFwlATvIIcHONG2uA`,
        },
    ],
    "screenshots": [ ucsscr1, ucsscr2, ucsscr3 ],
  },
}

export default {
    allApps,
}