import React from 'react';
import ReactDOM from 'react-dom';
import Layout from '../components/layout.jsx';
import Profile from '../components/profile.jsx';
import AppList from '../components/appList.jsx';

class Dashboard extends React.Component {
  constructor (props) {
    super(props);
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
