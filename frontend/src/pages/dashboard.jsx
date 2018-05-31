import React from 'react';
import ReactDOM from 'react-dom';
import Layout from '../components/dashboard/layout.jsx';
import Profile from '../components/dashboard/profile.jsx';
import AppList from '../components/dashboard/appList.jsx';
import moment from 'moment';

import './../sass/dashboard.scss';

class Dashboard extends React.Component {
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
    return <div>
      <Layout>
        <Profile name={this.state.data.name} cn={this.state.data.cn} />
        <AppList apps={this.state.data.apps} />
      </Layout>
    </div>;
  }
}

ReactDOM.render(
  <Dashboard />,
  document.querySelector('.app')
);
