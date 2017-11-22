import React from 'react';

import FeaturedApp from './FeaturedApp.jsx';


let featuredApps = [
  {
    "name": "Roombot",
    "description": "Find room bookings for your society, Find room bookings for your society",
    "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
  },
  {
    "name": "Roombot",
    "description": "Find room bookings for your society, Find room bookings for your society",
    "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
  },
  {
    "name": "Roombot",
    "description": "Find room bookings for your society",
    "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
  }
]

export default class Category extends React.Component {

  render() {
    return (
      <div className="featuredApps">
        <div className="container">
          <div className="row">
            {
              featuredApps.map((app, i) => {
                return (
                  <div key={i} className="col4">
                    <FeaturedApp
                      name={app.name}
                      logo={app.logo}
                      description={app.description}
                    />
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
