import React from 'react';

import FeaturedApp from './FeaturedApp.jsx';


export default class FeaturedApps extends React.Component {

  constructor(props) {
    super(props);

    let featuredApps = this.getRandom(this.props.allApps, 3);

    this.state = {
      featuredApps,
    }
  }

  getRandom(arr, n) {
    if (arr.length < n) {
      return arr;
    }

    let result = [], taken = [];

    while (n > 0) {
      let x = Math.floor(Math.random() * arr.length);

      if (taken.indexOf(x) === -1) {
        result.push(arr[x]);
        taken.push(x);
        n -= 1;
      }
    }

    return result;
  }

  render() {
    return (
      <div className="featuredApps">
        <div className="container">
          <div className="row">
            {
              this.state.featuredApps.map((app, i) => {
                return (
                  <div key={i} className="col4">
                    <FeaturedApp {...app} />
                  </div>
                )
              })
            }
          </div>
        </div>
      </div>
    )
  }

}
