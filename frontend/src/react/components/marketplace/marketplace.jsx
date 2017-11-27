import React from 'react';

import Intro from "./Intro.jsx";
import Category from "./Category.jsx";
import CategoryList from './CategoryList.jsx';
import FeaturedApps from './FeaturedApps.jsx';


let categories = [
  {
    "name": "Slack Apps",
    "description": "Apps for your slack groups",
    "apps": [
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
  },
  {
    "name": "Slack Apps",
    "description": "Apps for your slack groups",
    "apps": [
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      }
    ]
  },
  {
    "name": "Slack Apps",
    "description": "Apps for your slack groups",
    "apps": [
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      }
    ]
  },
  {
    "name": "Slack Apps",
    "description": "Apps for your slack groups",
    "apps": [
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      },
      {
        "name": "Roombot",
        "description": "Find room bookings for your society",
        "logo": "https://a.slack-edge.com/436da/marketing/img/meta/app-256.png"
      }
    ]
  }
]


let allApps = [];

for (let i=0; i < categories.length; i++) {
  allApps = allApps.concat(categories[i].apps);
}

export default class MarketplaceComponent extends React.Component {

    render () {
      return (
        <div>
          <Intro allApps={allApps} />

          <div className="container">
            <div className="row">

              <div className="col2">
                <CategoryList />
              </div>

              <div className="col10">
                <div className="categories">
                  {
                    categories.map((category, i) => {
                      return <Category
                          key={i}
                          name={category.name}
                          description={category.description}
                          apps={category.apps}/>;
                    })
                  }
                </div>
              </div>

            </div>
          </div>

        </div>
      )
    }

}
