import propTypes from 'prop-types'
import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'
import Constants from '../../../../lib/Constants'

const codeExamples = {
  python: `import requests

params = {
  "client_id": "123.456",
  "code": "1",
  "client_secret": "secret",
}
r = requests.get("${Constants.DOMAIN}/oauth/token", params=params)
print(r.json())`,

  shell: `curl -G ${Constants.DOMAIN}/oauth/token \
-d code=mysecretcode \
-d client_id=123.456 \\
-d client_secret=secret`,

  javascript: `fetch("${Constants.DOMAIN}/oauth/token?code=mysecretcode&client_id=123.456&client_secret=secret")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`,
}

const response = `{
    "scope": "[]",
    "state": "1",
    "ok": true,
    "client_id": "123.456",
    "token": "uclapi-user-abc-def-ghi-jkl",
}
`

const responseCodeExample = {
  python: response,
  javascript: response,
  shell: response,
}

const Token = ({ activeLanguage }) => (
  <div>
    <Topic
      activeLanguage={activeLanguage}
      codeExamples={codeExamples}
    >
      <h1 id="oauth/token">Token</h1>
      <p>
        Endpoint: <code>{Constants.DOMAIN}/oauth/token</code>
      </p>

      <p>
        Tokens uniquely identify an app that
        is requesting data from the API.
      </p>

      <p>
        Tokens are a long string variable of numbers and letters.
        e.g. <code>
          uclapi-5d58c3c4e6bf9c-c2910ad3b6e054-7ef60f44f1c14f-a05147bfd17fdb
        </code>
      </p>

      <p>
        There are two different kinds of tokens you can work with:
      </p>

      <p>
        1.    Generic Tokens:
        These are tokens that are used to request non-personal data.
        These tokens are used between applications and the API to request
        any sort of data that the app may need that is not tied to a specific
        student.
        For example,&nbsp;
        <a href="/docs#roombookings">UCL API’s Room booking service</a>
        &nbsp;uses tokens to return information about rooms -
        when they are booked and which UCL rooms are free.
      </p>

      <p>
        2.    OAuth Tokens:
        This type of token is used when an app requires
        personal data from users.
        One of the most common uses of this type of token
        is when you sign in via UCL on an app.&nbsp;
        The app will then use a token to request a user’s personal data such as:
      </p>
      <ul>
        <li>Department</li>
        <li> Email </li>
        <li> Full name </li>
        <li> Given name </li>
        <li> UPI </li>
        <li> If they are a student or not </li>
        <li> Student number<sup>*</sup></li>
      </ul>
      <p>
        <sup>*</sup>
        &nbsp;To get this, you need to tick the
        relevant scope in the dashboard before a user logs in.
        More on scopes <a href="/docs#oauth/meta">here</a>.
      </p>

      <p>
        Note that you can also use OAuth Tokens to access
        all the same data that generic app tokens can access.
      </p>

      <p>
        Each token is uniquely generated for each user logging into each app.
      </p>

      <p>
        Please note, access to any of this data
        needs to be approved by the user first.
      </p>

      <p>
        To use this type of token for your app,
        you need to redirect the user to the
        &quot;Authorise&quot; endpoint at:&nbsp;
        <code>{Constants.DOMAIN}/oauth/authorise</code>&nbsp;
        which can be done directly or by including a “Sign in With UCL Button”
        in your app, such as the one provided below,
        which links users to the authorisation endpoint with
        your app’s Client ID (accessible via the dashboard)
        and a random state number included in the GET parameters.
      </p>

      <p>
        The users then sign in with their UCL credentials and,
        if they authorise your app to use their personal data,
        a token will be generated which your app can use to get
        user’s personal data in JSON format from the oauth/user/data.

        Your application will receive the token at the callback URL
        you provided in the <a href="/dashboard">Dashboard</a>.
      </p>

      <Table
        name="Query Parameters"
      >
        <Cell
          name="client_id"
          requirement="required"
          example="123.456"
          description="Client ID of the authenticating app."
        />
        <Cell
          name="code"
          requirement="required"
          example="mysecretcode"
          description="Secret code obtained from the authorise endpoint."
        />
        <Cell
          name="client_secret"
          requirement="required"
          example="mysecret"
          description="Client secret of the authenticating app."
        />
      </Table>
    </Topic>

    <Topic
      activeLanguage={activeLanguage}
      codeExamples={responseCodeExample}
    >
      <h2>Response</h2>
      <p>
        Redirection to authorise page.
      </p>
    </Topic>

    <Topic
      noExamples
    >
      <Table
        name="Errors"
      >
        <Cell
          name="The client did not provide requisite data to get the token."
          description={
            `Gets returned when you have not supplied a client_id,`
            + ` code, client_secret in your request.`
          }
        />
        <Cell
          name={
            `The code received was invalid, or has expired.`
            + `Please try again.`
          }
          description="As error message."
        />
        <Cell
          name="Client secret incorrect."
          description="Gets returned when the client secret was incorrect."
        />
      </Table>
    </Topic>
  </div>
)


Token.propTypes = {
  activeLanguage: propTypes.string,
}

Token.defaultProps = {
  activeLanguage: `python`,
}

export default Token
