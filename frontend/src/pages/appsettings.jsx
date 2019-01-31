import React from 'react';
import ReactDOM from 'react-dom';
import Layout from '../components/dashboard/layout.jsx';
import Profile from '../components/dashboard/profile.jsx';
import AppList from '../components/dashboard/appList.jsx';
import LogInButton from '../components/appsettings/loginbutton.jsx';
import moment from 'moment';

import './../sass/dashboard.scss';

class AppSettings extends React.Component {
  constructor (props) {
    super(props);
    window.initialData.apps.sort((a, b) => {
      let dateA = moment(a.created);
      let dateB = moment(b.created);

      if(dateA.isBefore(dateB)){
        return -1;
      } else if (dateB.isBefore(dateA)){
        return 1;
      } else {
        return 0;
      }
    });
    this.state = {data: window.initialData};
  }
  render () {
    if(this.state.data.status!="ONLINE") {
      return <div>
        <Layout>   
          <LogInButton />
        </Layout>
      </div>;
    } else {
      return <div>
        <Layout>   
        </Layout>
      </div>;
    }
  }
}

ReactDOM.render(
  <AppSettings />,
  document.querySelector('.app')
);
