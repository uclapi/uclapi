import React from 'react';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';
import Navbar from '../components/dashboard/navbar.jsx';
import { css } from 'glamor';

import './../sass/dashboard.scss';

const appName = css({
  fontWeight: 'bold',
});

const cardTitle = css({
  fontWeight: 'normal',
});

const creator = css({
  color: 'grey',
});

const willHaveAccess = css({
  fontSize: 'larger',
});

const formButton = css({
  display: 'inline',
});

const bottomMessage = css({
  fontSize: 'smaller',
});


class AuthoriseApp extends React.Component {
  constructor (props) {
    super(props);
    this.state = {data: window.initialData};
  }
  render () {
    return <div>
      <div className="layout">
        <Navbar/>
        <div className="content pure-g">
          <div className="pure-u-md-1-4"></div>
          <div className="pure-u-1 pure-u-md-1-2 card">
            <h2 className={cardTitle}>
              Authorise <span className={appName}>{this.state.data.app_name}</span> to connect to your UCL Account
            </h2>
            <div className="pure-u-4">
              <h4 className={creator}>Created by {this.state.data.creator}</h4>
              <hr/>
              <em className={willHaveAccess}>
                <span className={appName}>{this.state.data.app_name}</span> will have access to:
              </em>
              <ul>
                  <li>Your Name ({this.state.data.user.full_name})</li>
                  <li>Your Email Address ({this.state.data.user.email})</li>
                  <li>Your Department ({this.state.data.user.department})</li>
                  <li>Your UPI ({this.state.data.user.upi})</li>
                  {this.state.data.scopes.map(scope => (
                    <li key={scope.name}>{scope.description}</li>
                  ))}
              </ul>
            </div>
            <form method="post" action="/oauth/user/allow" className={formButton}>
              <button type="submit" className="pure-button pure-button-primary padded">Authorise {this.state.data.app_name}</button>
              <input type="hidden" name="signed_app_data" value={this.state.data.signed_data}/>
              <input type="hidden" name="csrfmiddlewaretoken" value={Cookies.get('csrftoken')}/>
            </form>

            <form method="post" action="/oauth/user/deny" className={formButton}>
              <button className="pure-button padded">Deny</button>
              <input type="hidden" name="signed_app_data" value={this.state.data.signed_data}/>
              <input type="hidden" name="csrfmiddlewaretoken" value={Cookies.get('csrftoken')}/>
            </form>
            <hr/>
            <em className={bottomMessage}>
              {this.state.data.app_name} can only access the data shown above. Have a question? Contact us: <a href="mailto:isd.apiteam@ucl.ac.uk">isd.apiteam@ucl.ac.uk</a>.
            </em>
          </div>
          </div>
        <div className="pure-u-md-1-4"></div>
      </div>
    </div>;
  }
}

ReactDOM.render(
  <AuthoriseApp />,
  document.querySelector('.app')
);
