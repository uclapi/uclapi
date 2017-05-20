import React from 'react';
import ReactDOM from 'react-dom';
import Navbar from '../components/navbar.jsx';
import AppPermissions from '../components/appPermissions.jsx';

class AuthoriseApp extends React.Component {
  constructor (props) {
    super(props);
    this.state = {data: window.initialData};
  }
  render () {
    return <div>
      <div className="layout">
        <Navbar/>
        <div className="content">
          <h3>An application would like to connect to your UCL Account</h3>
          <AppPermissions
            app_name={this.state.data.app_name}
            creator={this.state.data.creator}
            private_roombookings={this.state.data.scope.private_roombookings}
            private_timetable={this.state.data.scope.private_timetable}
            private_uclu={this.state.data.scope.private_uclu}
          />
        </div>
      </div>
    </div>;
  }
}

ReactDOM.render(
  <AuthoriseApp />,
  document.querySelector('.app')
);
