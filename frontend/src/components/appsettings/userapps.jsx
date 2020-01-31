import React from 'react';
import PropTypes from 'prop-types';
import AuthAppRow from './authapprow.jsx';
// Components
import { ButtonView, CardView, Column, Demo, Footer, ImageView, NavBar, Row, TextView } from 'Layout/Items.jsx'

class UserApps extends React.Component {
  render () {
    const { authorised_apps } = this.props

    return <Row height='fit-content' styling='splash-parallax' style={{ minHeight : `100vh`}}>
          <Column width='2-3' horizontalAlignment='center' style={{ marginTop: `50px` }} >
            <TextView text={`Account`} heading={2} align={`center`} />
            <CardView width='1-1' type='default'>
              <div className="profile-card">
                <TextView text={this.props.fullname} heading={3} align={`center`} />
                <TextView text={this.props.department} heading={3} align={`center`} />
              </div>
            </CardView>

            <TextView text={`Permissions`} heading={2} align={`center`} />
            <CardView width='1-1' type='default'>
              {authorised_apps.length===0 ? (
                  <TextView text={"No authorised apps"} heading={3} align={`center`} />
                ) : (
                  authorised_apps.map((app, i) => 
                    <AuthAppRow app_name={app.app.name}
                      app_created={app.app.creator.name}
                      app_is_auth={app.active}
                      app_id={app.app.id}
                      app_client_id={app.app.client_id}
                      key={i}
                    />
                  )
                )
              }
            </CardView>
          </Column>
        </Row>;
  }
}

UserApps.propTypes = {
  fullname: PropTypes.string,
  department: PropTypes.string,
  authorised_apps: PropTypes.array
};

export default UserApps;
