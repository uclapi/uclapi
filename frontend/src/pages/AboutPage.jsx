// Standard React imports
import React from 'react';
import ReactDOM from 'react-dom';

// Images
import chris from 'Images/team/chris.jpeg';
import faiz from 'Images/team/faiz.jpeg';
import anirudh from 'Images/team/anirudh.jpeg';
import jaro from 'Images/team/jaro.jpeg';
import henry from 'Images/team/henry.jpeg';
import harry from 'Images/team/harry.jpg';
import huey from 'Images/team/huey.jpg';
import kimia from 'Images/team/kimia.jpg';
import anush from 'Images/team/anush.jpg';
import alex from 'Images/team/alex.jpg';
import zak from 'Images/team/zak.jpg';

import splash_screen from 'Images/home-page/splash_screen.png';

let previous = [
  {
    "name": "Chris",
    "startYear": "2016",
    "endYear": "2019",
    "title": "DevOps Ninja Extraordinaire",
    "email": "chris@ucl.ac.uk",
    "github": "https://github.com/ChristopherHammond13",
    "image": chris
  },
  {
    "name": "Faiz",
    "startYear": "2016",
    "endYear": "2019",
    "title": "API Wizard",
    "email": "faiz@ucl.ac.uk",
    "github": "https://github.com/faiz",
    "image": faiz
  },
  {
    "name": "Anirudh",
    "startYear": "2017",
    "endYear": "2018",
    "title": "Software Developer",
    "email": "ani@ucl.ac.uk",
    "github": "https://github.com/anirudhpillai",
    "image": anirudh
  },
  {
    "name": "Jaro",
    "startYear": "2016",
    "endYear": "2018",
    "title": "Software Architect",
    "email": "jaro@ucl.ac.uk",
    "github": "https://github.com/jermenkoo",
    "image": jaro
  },
  {
    "name": "Henry",
    "startYear": "2016",
    "endYear": "2017",
    "title": "Code Artisan",
    "email": "henry@ucl.ac.uk",
    "github": "https://github.com/hennersz",
    "image": henry
  }
]

let current = [
  {
      "name": "Zak",
      "startYear": "2019",
      "endYear": "Present",
      "title": "Commander General",
      "email": "zak.morgan.17@ucl.ac.uk",
      "github": "https://github.com/zipy124",
      "image": zak
    },
    {
      "name": "Alex",
      "startYear": "2019",
      "endYear": "Present",
      "title": "Russian Hacker",
      "email": "alexander.saoutkin.17@ucl.ac.uk",
      "github": "https://github.com/FeverFew",
      "image": alex
    },
    {
      "name": "Huey",
      "startYear": "2019",
      "endYear": "present",
      "title": "Senior React Developer",
      "email": "huey.lee.18@ucl.ac.uk",
      "github": "https://github.com/hueyy",
      "image": huey
    },
    {
      "name": "Kimia",
      "startYear": "2019",
      "endYear": "present",
      "title": "People Stuff",
      "email": "kimia.pirouzkia.17@ucl.ac.uk",
      "github": "https://github.com/kimia84",
      "image": kimia
    },
    {
      "name": "Anush",
      "startYear": "2019",
      "endYear": "present",
      "title": "Medic",
      "email": "anush.shashidhara.15@ucl.ac.uk",
      "github": "https://github.com/anushhks",
      "image": anush
    },
    {
      "name": "Harry",
      "startYear": "2019",
      "endYear": "present",
      "title": "Part Timer",
      "email": "harry.liversedge.17@ucl.ac.uk",
      "github": "https://github.com/TuxedoFish",
      "image": harry
    }
]

// Common Components
import { Row, Column, TextView, ButtonView, CardView, ImageView, Demo, NavBar, Footer } from 'Layout/Items.jsx';

// Styles
import 'Styles/common/uclapi.scss';

// Legacy
import 'Styles/navbar.scss';

const member = (info) => (
    <CardView style="alternate" width="1-3" minWidth="500px" >
          <Row src={info.image} height="400px">
            <Column style="1-1" isCentered={true} isCenteredText={true} isVerticalAlign={true}>
              <TextView text={info.name} heading={1} align={"center"}/>
              <TextView text={info.title} heading={2} align={"center"}/>
              <TextView text={info.email} heading={"p"} align={"center"}/>
              <TextView text={`${info.startYear} - ${info.endYear}`} heading={3} align={"center"}/>
              <TextView text="View GitHub" heading={2} align="center" link={info.github}/>
            </Column>
          </Row>
    </CardView>
);

class AboutPage extends React.Component {

  constructor (props) {
    super(props);

    this.state = {
      DEBUGGING: false,
    };
  }

  render () {
      return (
        <React.Fragment>
          <NavBar isScroll={"false"}/>

          <Row height = "600px" src={splash_screen}>         
            <Column style="1-1" isCentered={true} isVerticalAlign={true} isCenteredText={true}>
              <TextView text={"The Team"} heading={1} align={"center"}/>
              <TextView text={`UCL API is a student led project founded by Wilhelm Klopp that opens up the massive amount of
                              data collected by UCL and allows UCL students and staff access to develop with it.`} 
                              heading={2} align={"center"}/>
            </Column>
          </Row>

          <Row isPadded = {true} color="dark-grey">         
            <Column style="9-10" isCentered={true} >
              <TextView text={"Current Team"} heading={1} align={"center"}/>
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">
            <Column style="2-3" widthOverride="auto" isCentered={true} isCenteredText={true}>
              {current.map(x =>  member(x) )}
            </Column>
          </Row>

          <Row isPadded = {true} color="dark-grey">         
            <Column style="9-10" isCentered={true} >
              <TextView text={"Previous developers"} heading={1} align={"center"}/>
            </Column>
          </Row>
          <Row isPaddedBottom={true} color="dark-grey">
            <Column style="2-3" widthOverride="auto" isCentered={true} isCenteredText={true}>
              {previous.map(x => member(x) )}
            </Column>
          </Row>

          <Footer />

        </React.Fragment>
      );
  }
}

ReactDOM.render(
  <AboutPage />,
  document.querySelector('.app')
);
