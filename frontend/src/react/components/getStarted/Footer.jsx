import React from 'react';

import Jumbotron from './Jumbotron.jsx';


export default class Footer extends React.Component {

  render() {
    return (
      <div className="footer">
        <div className="container">
          <h1>We can’t wait to see what you build.</h1>
          <div className="row">
            <div className="col">
              <h3>Links</h3>
              <a href={"https://twitter.com/uclapi"}>Twitter</a>
              <a href={"https://facebook.com"}>Facebook</a>
              <a href={"https://github.com/uclapi"}>GitHub</a>
            </div>
            <div className="col">
              <h3>On The Blog</h3>
              <a href={"https://medium.com/ucl-api/the-launch-of-ucl-api-e835d7c80925"}>
                The Launch of UCL API
              </a>
              <a href={"https://medium.com/ucl-api/accessing-oracle-database-via-a-cisco-vpn-via-ldap-on-linux-5bf17ba84a57"}>
                Accessing Oracle Database via a Cisco VPN (via LDAP) on Linux
              </a>
              <a href={"https://medium.com/ucl-api/adventures-in-shibboleth-and-nginx-part-1-of-2-6e7ea25ff48b"}>
                Adventures in Shibboleth and Nginx (Part 1 of 2)
              </a>
            </div>
          </div>
        </div>
      </div>
    )
  }

}
