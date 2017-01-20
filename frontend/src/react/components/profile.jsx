import React from 'react';

class Profile extends React.Component {
  render () {
    return <div className="card pure-u-1">
      <h2>{this.props.username}</h2>
      <h3>{this.props.email}</h3>
    </div>;
  }
}

Profile.propTypes = {
  username: React.PropTypes.string.isRequired,
  email: React.PropTypes.string.isRequired
};

export default Profile;
