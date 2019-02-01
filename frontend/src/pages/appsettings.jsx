import React from 'react';
import ReactDOM from 'react-dom';
import Hub from '../components/appsettings/hub.jsx';
import LogInButton from '../components/appsettings/loginbutton.jsx';
import moment from 'moment';

import './../sass/dashboard.scss';
import './../sass/hub.scss';

class AppSettings extends React.Component {
  constructor (props) {
    super(props);
    this.state = {data: window.initialData};
  }
  render () {
    if(this.state.data.status!="ONLINE") {
      return <div>
        <Hub>   
          <LogInButton url={this.state.data.url} />
        </Hub>
      </div>;
    } else {
      return <div>
        <Hub>   
        </Hub>
      </div>;
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector('.app')
);
