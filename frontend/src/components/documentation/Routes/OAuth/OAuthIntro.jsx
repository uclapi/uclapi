import React from 'react'
import signInButton from './../../../../images/signInWithUCLAPI.png'
import Topic from './../../Topic'
import './OAuthIntro.scss'
import Constants from '../../../../lib/Constants'


const codeExamples = {
  html: `<a href="${Constants.DOMAIN}/oauth/authorise?client_id=CLIENT_ID&state=STATE">
  <img src="https://s3.eu-west-2.amazonaws.com/uclapi-static/SignInWithUCLSmall.png">
</a>`,
}

const OAuthIntro = ({ activeLanguage }) => (
  <>
    <Topic
      activeLanguage={activeLanguage}
      codeExamples={codeExamples}
    >
      <p>
        This is a quick guide to OAuth support in UCL API for developers.
        OAuth is a protocol that lets external apps request secure access to
        private UCL account data without getting your password.
        This can be done with a &quot;Sign In With UCL&quot; button on your
        website or app which saves UCL users the trouble of registering a
        new account with you.
        It also allows your app or website to retrieve a user&apos;s
        personal timetable.
      </p>
      <p>
        Check out a JS web app demo&nbsp;
        <a href="https://uclapi-oauth-demo.glitch.me/">here</a>.
        The source code for the demo is available&nbsp;
        <a href="https://glitch.com/edit/#!/uclapi-oauth-demo">here</a>.
      </p>

      <p>
        For an example of a mobile app implementation, check out&nbsp;
        <a href="https://github.com/uclapi/ucl-assistant-app">
          UCL Assistant
        </a>
        &nbsp;(written in React Native) and the accompanying&nbsp;
        <a href="https://github.com/uclapi/ucl-assistant-api/tree/master/src/oauth">
          UCL Assistant API
        </a>
        &nbsp;backend (written in Node.JS).
      </p>

      <h1>Sign In With UCL Button</h1>
      <p>
        If you want to add a &quot;Sign In With UCL&quot; button to your site,
        which looks like this:
      </p>

      <img className="sign-in-with-ucl" src={signInButton} />

      <p>
        you can copy the following the code below and replace&nbsp;
        <code>CLIENT_ID</code> and <code>STATE</code> by the
        &nbsp;<code>client_id</code> of your app
        and a random <code>state</code>.
      </p>
    </Topic>
    <Topic noExamples>
      <h1 id="oauth/scopes">Scopes</h1>
      <p>
        OAuth scopes specify what access your app needs to a UCL user’s account.
        As an app developer, you set the desired scopes in the&nbsp;
        <a href="/dashboard">API Dashboard</a>.
        When a user is responding to your authorisation request,
        the requested scopes will be displayed to the user.
      </p>

      <h1 id="oauth/workflow">OAuth Workflow</h1>
      <p>
        If your application uses OAuth, you must set a callback URL
        in the dashboard.
        Then the app should follow this procedure:
      </p>
      <p>
        1. Redirect the user to&nbsp;
        <code>{Constants.DOMAIN}/oauth/authorise</code>&nbsp;
        with <code>state</code> and the application’s <code>client_id</code> as
        query parameters.
      </p>
      <p>
        2. The user logs in with their UCL credentials on the
        UCL Single Sign-on website (if not logged in already).
      </p>
      <p>
        3. The user reviews the OAuth scopes requested and either
        authorises or denies the application&apos;s request.
        If the application is authorised, the callback URL receives&nbsp;
        <code>client_id</code>, <code>state</code> (specified in 1.),&nbsp;
        <code>result</code>, and <code>code</code>.
      </p>

      <p>
        If the application is denied, the callback URL receives
        &nbsp;<code>result</code> and <code>state</code>, and no private data
        will be provided to the application.
      </p>
      <p>
        1. To obtain a OAuth user token
        (necessary for retrieving personal data and certain API endpoints),
        we require <code>code</code> (from 3.),&nbsp;
        <code>client_id</code>, and <code>client_secret</code>.
        These should then be sent to&nbsp;
        <code>{Constants.DOMAIN}/oauth/token</code>,
        which will return a response containing&nbsp;
        <code>state</code>, <code>ok</code>, <code>client_id</code>,&nbsp;
        <code>token</code> (OAuth user token), and <code>scope</code>&nbsp;
        (OAuth scopes the app can access on the user’s behalf).
      </p>
      <p>
        <b>Note:</b> OAuth tokens and general API tokes are different.
        Whilst general API tokens can be used for all non-personal,
        generic data (such as room bookings),
        OAuth tokens must be used with an app&apos;s&nbsp;
        <code>client_secret</code>
        &nbsp;in order to retrieve personal data for a user.
        To make things easier, you can use personal OAuth tokens in place of
        general tokens once a user has logged into your app to
        retrieve generic data too.
      </p>
    </Topic>
  </>
)

export default OAuthIntro