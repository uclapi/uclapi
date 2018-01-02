import React from 'react';


export default class CategoryList extends React.Component {

  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="categoryList">
        {
          this.props.categories.map((item, i) => {
            return (
              <a
                href={"#" + item.name}
                key={i}
                style={{
                  backgroundColor: item.color
                }}>
                {item.name}
              </a>
            )
          })
        }
      </div>
    );
  }

}
