import React from 'react';
import {
  Card,
  CardActions,
  CardMedia,
  CardTitle,
  CardText
} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


const Example = (title, imageLink, description, link, key) => (
  <Card className="example" zDepth={2} key={key}>
    <CardMedia>
      <img src={imageLink}/>
    </CardMedia>
    <CardTitle title={title}/>
    <CardText>
      {description}
    </CardText>
    <CardActions>
      <a href={link}>
        <FlatButton label="View"/>
      </a>
    </CardActions>
  </Card>
);

const staticRoot = `${location.protocol}//${location.hostname}${location.port ? ':' + location.port : ''}/static/`;

const examples = [
  {
    title: 'Veruto',
    imageLink: `${staticRoot}github-logo.png`,
    description: 'A mobile app that finds the closest free room in UCL',
    link: 'https://github.com/uclapi/veruto'
  }, {
    title: 'Society Visualisation',
    imageLink: `${staticRoot}github-logo.png`,
    description: 'A calendar visualisation of Society Room Bookings at UCL',
    link: 'https://github.com/uclapi/society-visualisation'
  }, {
    title: 'RB Calendar',
    imageLink: `${staticRoot}github-logo.png`,
    description: 'Turn UCL API room bookings into ics calendar events.',
    link: 'http://rbcalendar.uclapi.com'
  }, {
    title: 'UCLKit',
    imageLink: `${staticRoot}swift-logo.png`,
    description: 'UCL API wrapper in Swift',
    link: 'https://github.com/tiferrei/UCLKit'
  }, {
    title: 'uclapi-go',
    imageLink: `${staticRoot}go-logo.png`,
    description: 'A wrapper library in Go for uclapi',
    link: 'https://github.com/Maaarcocr/uclapi-go'
  }, {
    title: 'uclapi-javascript',
    imageLink: `${staticRoot}npm-logo.png`,
    description: 'JavaScript wrapper for the UCL API. Works both in the browser and in Node.',
    link: 'https://github.com/HugoDF/uclapi-javascript'
  }
];


export default class Examples extends React.Component {

  render() {
    return (
      <div className="container pad">
        <h1 className="center">Built Using UCL API</h1>
        <div className="examples">
          {examples.map((eg, i) => Example(eg.title, eg.imageLink, eg.description, eg.link, i))}
        </div>
      </div>
    );
  }

}
