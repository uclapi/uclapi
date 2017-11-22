import React from 'react';


let categories = [
  {
    name: "Slack Apps",
    link: "#slack"
  },
  {
    name: "Android",
    link: "#slack"
  },
  {
    name: "Timetable",
    link: "#slack"
  },
  {
    name: "Productivity",
    link: "#slack"
  }
]

export default class CategoryList extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="categoryList">
        <h2>Categories</h2>
        {
          categories.map((item, i) => {
            return (<div key={i}>
              <a href={item.link}>
                {item.name}
              </a>
            </div>)
          })
        }
      </div>
    );
  }

}
