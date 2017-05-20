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
                (!(this.props.private_roombookings || this.props.private_timetable || this.props.private_uclu)) &&
                <em>
                    This app has not requested access to any of your personal UCL data. It will only be able to see public data, such as the public timetable and room bookings information. If you are expecting this app to show you any personal data, please contact the vendor.
                </em>
            }
            <ul>
                {
                    this.props.private_roombookings && 
                    <li>
                        Information on which <strong>rooms you have booked</strong>
                    </li>
                }

                {
                    this.props.private_timetable &&
                    <li>
                        Your <strong>personal timetable</strong>
                    </li>
                }

                {
                    this.props.private_uclu &&
                    <li>
                        Your <strong>personal UCL Union (UCLU)</strong> data, including information on which societies you are part of.
                        If you are a president or treasurer of a society, the app will be able to submit receipts, fetch member data and more, all on your behalf.
                    </li>
                }
            </ul>

            </div>;
    }
}

AppPermissions.propTypes = {
    app_name: React.PropTypes.string.isRequired,
    creator: React.PropTypes.string.isRequired,
    private_roombookings: React.PropTypes.bool.isRequired,
    private_timetable: React.PropTypes.bool.isRequired,
    private_uclu: React.PropTypes.bool.isRequired,
    user_full_name: React.PropTypes.string.isRequired,
    user_email: React.PropTypes.string.isRequired,
    user_department: React.PropTypes.string.isRequired,
    user_upi: React.PropTypes.string.isRequired
};

export default AppPermissions;