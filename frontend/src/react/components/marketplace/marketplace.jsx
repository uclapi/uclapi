import React from 'react';

import Intro from "./Intro.jsx";
import Category from "./Category.jsx";
import CategoryList from './CategoryList.jsx';
import FeaturedApps from './FeaturedApps.jsx';


let testCategories = [
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


export default class MarketplaceComponent extends React.Component {

    render () {
      return (
        <div>
          <Intro />
          <FeaturedApps />

          <div className="container">
            <div className="row">

              <div className="col4">
                <CategoryList />
              </div>

              <div className="col8">
                <div className="categories">
                  {
                    testCategories.map((category, i) => {
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
