import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


const Example = (title, imageLink, description, link, key) => (
  <Card className="example" key={ key }>
    <CardMedia>
      <img src={ imageLink } />
    </CardMedia>
    <CardTitle title={ title } />
    <CardText>
      { description }
    </CardText>
    <CardActions>
      <a href={ link }>
        <FlatButton label="View" />
      </a>
    </CardActions>
  </Card>
)

let examples = [
  {
    title: "Techsoc",
    imageLink: "https://avatars2.githubusercontent.com/u/3532459?v=3&s=400",
    description: "Used to build an amazing room bookings platform",
    link: "https://enghub.io"
  },
  {
    title: "Techsoc",
    imageLink: "https://avatars2.githubusercontent.com/u/3532459?v=3&s=400",
    description: "Used to build an amazing room bookings platform",
    link: "https://enghub.io"
  },
  {
    title: "Techsoc",
    imageLink: "https://avatars2.githubusercontent.com/u/3532459?v=3&s=400",
    description: "Used to build an amazing room bookings platform",
    link: "https://enghub.io"
  }
]

export default class Examples extends React.Component {

  render () {
    return (
      <div className="container pad">
        <h1 className="center">Built Using UCL API</h1>
        <div className="examples">
          { examples.map((eg, i) => Example(eg.title, eg.imageLink, eg.description, eg.link, i)) }
        </div>
      </div>
    )
  }

}
