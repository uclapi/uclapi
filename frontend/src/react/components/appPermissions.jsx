import React from 'react';

class AppPermissions extends React.Component {
    render() {
        return <div className="card pure-u-4">
            <h2>{this.props.app_name}</h2>
            <h4><em>Written by {this.props.creator}</em></h4>
            <hr/>
            <h3>Requested Permissions</h3>
            {
                (!(this.props.private_roombookings || this.props.private_timetable || this.props.private_uclu)) &&
                <em>
                    This app has not requested access to any of your personal UCL data.
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
    private_uclu: React.PropTypes.bool.isRequired
};

export default AppPermissions;