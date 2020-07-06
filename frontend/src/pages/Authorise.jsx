import { css } from 'glamor'
import Cookies from 'js-cookie'
import React from 'react'
import ReactDOM from 'react-dom'
import 'Styles/dashboard.scss'
import Navbar from '../components/dashboard/navbar.jsx'



const appNameCSS = css({
  fontWeight: `bold`,
})

const cardTitle = css({
  fontWeight: `normal`,
})

const creatorCSS = css({
  color: `grey`,
})

const willHaveAccess = css({
  fontSize: `larger`,
})

const formButton = css({
  display: `inline`,
})

const bottomMessage = css({
  fontSize: `smaller`,
})


class AuthoriseApp extends React.Component {
  constructor(props) {
    super(props)
    this.state = { data: window.initialData }
  }
  render() {
    const {
      data: {
        appName,
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
    }
    return <div>
      <div className="layout">
        <Navbar />
        <div className="content pure-g">
          <div className="pure-u-md-1-4"></div>
          <div className="pure-u-1 pure-u-md-1-2 card">
            <h2 className={cardTitle}>
              Authorise
              &nbsp;<span className={appNameCSS}>{appName}</span>&nbsp;
              to connect to your UCL Account
            </h2>
            <div className="pure-u-4">
              <h4 className={creatorCSS}>Created by {creator}</h4>
              <hr />
              <em className={willHaveAccess}>
                <span className={appName}>{appName}</span> will have access to:
              </em>
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
            <form
              method="post"
              action="/oauth/user/allow"
              className={formButton}
            >
              <button
                type="submit"
                className="pure-button pure-button-primary padded"
              >
                Authorise {appName}
              </button>
              <input type="hidden" name="signed_app_data" value={signed_data} />
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={Cookies.get(`csrftoken`)}
              />
            </form>

            <form
              method="post"
              action="/oauth/user/deny"
              className={formButton}
            >
              <button className="pure-button padded">Deny</button>
              <input type="hidden" name="signed_app_data" value={signed_data} />
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={Cookies.get(`csrftoken`)}
              />
            </form>
            <hr />
            <em className={bottomMessage}>
              {appName} can only access the data shown above.
              Have a question? Contact us:
              &nbsp;<a href="mailto:isd.apiteam@ucl.ac.uk">
                isd.apiteam@ucl.ac.uk
              </a>
              .
            </em>
          </div>
        </div>
        <div className="pure-u-md-1-4"></div>
      </div>
    </div>
  }
}

ReactDOM.render(
  <AuthoriseApp />,
  document.querySelector(`.app`)
)
