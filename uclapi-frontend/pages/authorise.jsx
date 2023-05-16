import Cookies from 'js-cookie'

import Navbar from '../../components/dashboard/navbar.jsx'
import './Authorise.scss'


class AuthoriseApp extends React.Component {
  constructor(props) {
    super(props)
    this.state = { data: window.initialData }
  }
  render() {
    const {
      data: {
        app_name: appName,
        creator,
        user: {
          full_name,
          email,
          department,
          upi,
        },
        scopes,
        signed_data,
      },
    } = this.state
    return (
      <div className="authorise-page">
        <Navbar />
        <div className="content">
          <h2 className="card-title">
            Authorise
            <strong>&nbsp;{appName}&nbsp;</strong>
            to connect to your UCL Account
          </h2>
          <div className="details">
            <p className="creator">Created by <u>{creator}</u></p>
            <hr />
            <p className="will-have-access">
              <strong>{appName}</strong> will have access to:
            </p>
            <ul>
              <li>Your Name ({full_name})</li>
              <li>Your Email Address ({email})</li>
              <li>Your Department ({department})</li>
              <li>Your UPI ({upi})</li>
              {scopes.map(scope => (
                <li key={scope.name}>{scope.description}</li>
              ))}
            </ul>
          </div>

          <div className="authorise-buttons">
            <form
              method="post"
              action="/oauth/user/allow"
            >
              <button
                type="submit"
                className="authorise-button"
              >
                Authorise {appName}
              </button>
              <input
                type="hidden"
                name="signed_app_data"
                value={signed_data}
              />
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={Cookies.get(`csrftoken`)}
              />
            </form>

            <form
              method="post"
              action="/oauth/user/deny"
            >
              <button className="deny-button">Deny</button>
              <input
                type="hidden"
                name="signed_app_data"
                value={signed_data}
              />
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={Cookies.get(`csrftoken`)}
              />
            </form>
          </div>

          <hr />
          <div className="bottom-message">
            <p>
              <strong>{appName}</strong> can only access the data shown above.
            </p>
            <p>
              Have a question? Contact us:&nbsp;
              <a href="mailto:isd.apiteam@ucl.ac.uk">
                isd.apiteam@ucl.ac.uk
              </a>
              .
            </p>
          </div>
        </div>
      </div>
    )
  }
}

export default AuthoriseApp
