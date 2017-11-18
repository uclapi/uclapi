import React from 'react';

import Category from "./Category.jsx";


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
          <h1>Marketplace</h1>
          <div className="categories">
            {
              testCategories.map((category) => {
                return <Category
                    name={category.name}
                    description={category.description}
                    apps={category.apps}/>;
              })
            }
          </div>
        </div>
      )
    }

}
