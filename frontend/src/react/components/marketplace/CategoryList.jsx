import React from 'react';


export default class CategoryList extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="categoryList">
        <h2>Categories</h2>
        {
          this.props.categories.map((item, i) => {
            return (<div key={i}>
              <a href={"#" + item.name}>
                {item.name}
              </a>
            </div>)
          })
        }
      </div>
    );
  }

}
