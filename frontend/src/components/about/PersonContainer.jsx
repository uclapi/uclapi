import React from 'react';

import PersonCard from './PersonCard.jsx';

import chris from './../../images/chris.jpeg';
import faiz from './../../images/faiz.jpeg';
import anirudh from './../../images/anirudh.jpeg';
import jaro from './../../images/jaro.jpeg';
import henry from './../../images/henry.jpeg';

import harry from './../../images/harry.jpg';
import huey from './../../images/huey.jpg';
import kimia from './../../images/kimia.jpg';
import anush from './../../images/anush.jpg';
import alex from './../../images/alex.jpg';
import zak from './../../images/zak.jpg';

let team_16 = [
    {
      "name": "Chris",
      "startYear": "2016",
      "endYear": "Present",
      "title": "DevOps Ninja Extraordinaire",
      "email": "chris@ucl.ac.uk",
      "github": "https://github.com/ChristopherHammond13",
      "image": chris
    },
    {
      "name": "Faiz",
      "startYear": "2016",
      "endYear": "Present",
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
];

let team_19 = [ 
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
      "startYear": "2016",
      "endYear": "2018",
      "title": "People Stuff",
      "email": "kimia.pirouzkia.17@ucl.ac.uk",
      "github": "https://github.com/kimia84",
      "image": kimia
    },
    {
      "name": "Anush",
      "startYear": "2019",
      "endYear": "2017",
      "title": "Medic",
      "email": "anush.shashidhara.15@ucl.ac.uk",
      "github": "https://github.com/anushhks",
      "image": anush
    },
    {
      "name": "Harry",
      "startYear": "2019",
      "endYear": "2017",
      "title": "Part Timer",
      "email": "harry.liversedge.17@ucl.ac.uk",
      "github": "https://github.com/TuxedoFish",
      "image": harry
    }
];

export default class PersonContainer extends React.Component {
  constructor(props) {
    super(props);
  }

  render () {
    var title = "err";
    if(this.props.index==0) {
      // '16-'18
      title="2016 - 2018"

    } else if(this.props.index==1) {
      // '18-'19
      title="2018 - 2019"

    }

    var index = this.props.index;
    var team = [];
    switch(index) {
      case 0:
        team = team_16;
        break;
      case 1:
        team = team_19;
        break;
    }

    return (
      <div className="lineContainer">
        <div className="container pcContainer">
          <h1>{title}</h1>
          <div className="personContainer">
            {
              team.map((person, i) => {
                return <PersonCard key={i} {...person} />;
              })
            }
          </div>
        </div>
      </div>
    )
  }

}
