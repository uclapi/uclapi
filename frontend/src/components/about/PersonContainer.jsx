import React from 'react';

import PersonCard from './PersonCard.jsx';

import chris from './../../images/chris.jpeg';
import faiz from './../../images/faiz.jpeg';
import anirudh from './../../images/anirudh.jpeg';
import jaro from './../../images/jaro.jpeg';
import henry from './../../images/henry.jpeg';

let team = [
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
]

export default class PersonContainer extends React.Component {

  render () {
    return (
      <div className="container">
        <div className="personContainer">
          {
            team.map((person, i) => {
              console.log(i);
              return <PersonCard key={i} {...person} />;
            })
          }
        </div>
      </div>
    )
  }

}
