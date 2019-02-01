import React from 'react';
import PropTypes from 'prop-types';

class UserApps extends React.Component {
  render () {
    return <div class="sign-in-form">
      {this.props.fullname}
    </div>;
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string
};

export default UserApps;