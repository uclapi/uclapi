// React
import React from 'react';

// Images
// Room Buddy
import roombuddylogo from 'Images/marketplace/roombuddy/logo.png';
import roombuddy_screenshot1 from 'Images/marketplace/roombuddy/screenshot_1.png';
import roombuddy_screenshot2 from 'Images/marketplace/roombuddy/screenshot_2.png';
import roombuddy_screenshot3 from 'Images/marketplace/roombuddy/screenshot_3.png';
// UCL Assistant
import uclassistantlogo from 'Images/marketplace/uclassistant/logo.png';
import uclassistant_screenshot1 from 'Images/marketplace/uclassistant/screenshot_1.png';
import uclassistant_screenshot2 from 'Images/marketplace/uclassistant/screenshot_2.png';
import uclassistant_screenshot3 from 'Images/marketplace/uclassistant/screenshot_3.png';

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, NavBar } from 'Layout/Items.jsx';

// Application config
let roombuddydescription = (
  <div className="roombuddy-full-description" style={ { "display": "inline-block"} } >
       <TextView heading={"3"} text={`Finding a place to get your work done can be hard. Every place you've thought of
         is somehow already filled up: the libraries, the study pods, the benches outside the Print Room Café...`} />
       <TextView heading={"3"} text={`Room Buddy makes use of UCL API to find and direct you to open study spaces
         that aren't widely known. These rooms are scarcely booked up for timetables and sit waiting for you to
         grace them with your glory.`} />
       <TextView heading={"3"} text={`It's simple: install the app, sign in with your UCL ID, and get going to the
         closest available space to your current location!`} />
       <TextView heading={"3"} text={`UCL Room Buddy was built with the UCL API, which gives student developers
         programmatic access to UCL's data in order to improve the UCL experience for everyone.`} />
       <TextView heading={"3"} text={"Want to contribute to room buddy? Submit a pull request:"}/>
       <ButtonView buttonType={"alternate"} text={"VISIT GITHUB"} isCentered={true} link={"https://github.com/uclapi/ucl-assistant-app"} />
       <TextView heading={"3"} text={`This app and its platform have been built by the UCL API Team, a group of students
         working with UCL's Information Services Division (ISD) to provide students with a brand new ecosystem that allows
         anyone within the UCL Community to build apps with UCL data. Interested in building an app just like UCL Room Buddy
         yourself? Head over to uclapi.com and log in with your UCL Account.`}/>
  </div>
);

let uclassistantdescription = (
  <div className="uclassistant-full-description" style={ {"display": "inline-block" } } >
       <TextView heading={"3"} text={"✨✨A brand new and beautiful app to manage your student life at UCL!✨✨"} />
       <TextView heading={"3"} text={"✅ View your personal timetable and get instant directions to your lectures."} />
       <TextView heading={"3"} text={`✅ Check the availability of all UCL libraries and study spaces, including in
         the new Student Centre. Want to know which floor or room has the most seats free? You now have that
         information right in the palm of your hand! Not sure which seats are free? No problem! Just use the live
         seating maps to see every seat that has been unoccupied for over half an hour on whichever library 
         floor you choose`} />
       <TextView heading={"3"} text={`✅ Search for members of the UCL community, including students and lecturers,
         and tap to email them. Nice and easy!`}/>
       <TextView heading={"3"} text={`✅ Find every centrally bookable room at UCL, see how big it is and whether it is 
         currently in use, and then tap to navigate right there.`}/>
       <TextView heading={"3"} text={"✅ Made with love 💖 by and for students"}/>
       <TextView heading={"3"} text={`✅ Fully open source. Got feedback, suggestions or even some new code to improve 
         the app? We welcome it:`}/>
       <ButtonView buttonType={"alternate"} isCentered={true} text={"VISIT GITHUB"} link={"https://github.com/uclapi/ucl-assistant-app"} />
       <TextView heading={"3"} text={`This app and its platform have been built by the UCL API Team, a group of students
         working with UCL's Information Services Division (ISD) to provide students with a brand new ecosystem that allows
         anyone within the UCL Community to build apps with UCL data. Interested in building an app just like UCL Assistant
         yourself? Head over to uclapi.com and log in with your UCL Account.`}/>
  </div>
);

export const allApps = {
  "uclroombuddy": {
    "name": "UCL Room Buddy", "id": "uclroombuddy", "category": "roombookings", "description": "Find the closest free room at UCL", "logo": roombuddylogo,
    "detailedDescription": roombuddydescription, "developerContact": "https://github.com/wilhelmklopp",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclroombuddy",
    "screenshots": [ roombuddy_screenshot1, roombuddy_screenshot2, roombuddy_screenshot3 ]
  },
  "uclassistant": {
    "name": "UCL Assistant", "id": "uclassistant", "category": "productivity", "description": "An app to manage your student life at UCL", "logo": uclassistantlogo,
    "detailedDescription": uclassistantdescription, "developerContact": "https://github.com/uclapi",
    "androidLink": "https://play.google.com/store/apps/details?id=com.uclapi.uclassistant&hl=en_GB",
    "screenshots": [ uclassistant_screenshot1, uclassistant_screenshot2, uclassistant_screenshot3 ]
  },
}

export default {
    allApps,
}