import React from 'react';

class Profile extends React.Component {
  render () {
    return <div className="card pure-u-1">
      <h2>{this.props.name}</h2>
      <h3>{this.props.cn}</h3>
    </div>;
  }
}

Profile.propTypes = {
  name: React.PropTypes.string.isRequired,
  cn: React.PropTypes.string.isRequired
};

export default Profile;
