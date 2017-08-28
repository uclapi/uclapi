import React from 'react';

class AppPermissions extends React.Component {
    render() {
        return <div className="pure-u-4">
            <h2>{this.props.app_name}</h2>
            <h4><em>Written by {this.props.creator}</em></h4>
            <hr/>
            <h3>Permissions</h3>
            <h4>Standard Permissions</h4>
            <em>
                All UCL API apps that use this system are provided with this data.
            </em>
            <ul>
                <li>Your Name ({this.props.user_full_name})</li>
                <li>Your Email Address ({this.props.user_email})</li>
                <li>Your Department ({this.props.user_department})</li>
                <li>Your UPI ({this.props.user_upi})</li>
            </ul>

            <h4>Personal Data Permissions</h4>
             {
                (this.props.scopes.length == 0) &&
                <em>
                    Apart from the data listed above, this app has not requested access to any of your personal UCL data. It will only be able to see public data, such as room bookings and the public timetable.
                </em>
            }
            <ul>
                {
                    this.props.scopes.map(function(scope) {
                        return <li key={scope.name}>{scope.description}</li>
                    })
                }
            </ul>
        </div>;
    }
}

AppPermissions.propTypes = {
    app_name: React.PropTypes.string.isRequired,
    creator: React.PropTypes.string.isRequired,
    scopes: React.PropTypes.arrayOf(React.PropTypes.object).isRequired,
    user_full_name: React.PropTypes.string.isRequired,
    user_email: React.PropTypes.string.isRequired,
    user_department: React.PropTypes.string.isRequired,
    user_upi: React.PropTypes.string.isRequired
};

export default AppPermissions;