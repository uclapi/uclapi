import propTypes from 'prop-types'
import React from 'react'
import Cell from './../../Cell.jsx'
import Table from './../../Table.jsx'
import Topic from './../../Topic'

const codeExamples = {
  python: `
  url = "https://uclapi.com/oauth/authorise/?client_id=123&state=1"

  '''
    in a desktop app, script, or for testing
  '''
  import webbrowser
  webbrowser.open_new(url) 
  # note that you will also need some way receive the callback
  # this can be done via a web server (e.g. below)
  
  '''
    on a Flask server
    this example covers both redirecting the user to
    the /authorise page and receiving the callback
  '''
  from flask import Flask, redirect, request
  app = Flask(__name__)

  @app.route('/login')
  def uclapi_login():
      return redirect(url)
  
  @app.route('/callback')
      # receive parameters
      result = request.args.get('result', '')
      code = request.args.get('code', '')
      state = request.args.get('state', '')
      # do something with these parameters
      # e.g. request an auth token from /oauth/token
      return`,

  shell: `
  # linux
  xdg-open "https://uclapi.com/oauth/authorise/?client_id=123.456&state=1"
  
  # WSL
  cmd.exe /c start "https://uclapi.com/oauth/authorise/?client_id=123^&state=1"

  # note that you will also need some way to receive the callback
  `,

  javascript: `
  const url = "https://uclapi.com/oauth/authorise/?client_id=123.456&state=1"

  /* in-browser */
  window.location.href = url
  // note that you will also need some way to receive the callback
  // this can be done via a web server (e.g. below)

  /* Node.JS Express server */
  const express = require('express')
  const app = express()

  app.get('/login', (req, res) => res.redirect(url))
  app.get('/callback', (req, res) => {
    const {
      result,
      code,
      state
    } = req.params
    // do something with these parameters
    // e.g. request an auth token from /oauth/token
  })

  app.listen(3000)
  `,
}

const Authorise = ({ activeLanguage }) => (
  <div>
    <Topic
      activeLanguage={activeLanguage}
      codeExamples={codeExamples}
    >
      <h1 id="oauth/authorise">Authorise</h1>
      <p>
        Endpoint: <code>https://uclapi.com/oauth/authorise</code>
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
          name="state"
          requirement="required"
          example="1"
          description="OAuth state."
        />
      </Table>
    </Topic>

    <Topic noExamples>
      <h2>Response</h2>
      <p>
        Redirections the user to the authorise page.
        If the user signs in successfully,
        they are redirected again to the callback URL
        specified in the&nbsp;
        <a href="/dashboard">Dashboard</a>.
      </p>
      <p>
        The callback URL specified in&nbsp;
        <a href="/dashboard">Dashboard</a>
        &nbsp;will receive the following query parameters:
      </p>
      <Table
        name="Response (Query Parameters)"
      >
        <Cell
          name="client_id"
          extra="string"
          example="123.456"
          description="Client ID of the authenticating app"
        />
        <Cell
          name="state"
          extra="string"
          example="1"
          description="The same state parameter originally sent as a query parameter to /oauth/authorise"
        />
        <Cell
          name="result"
          extra="string"
          example="allowed"
          description="Either 'allowed' or 'denied', depending on whether the user granted permission"
        />
        <Cell
          name="code"
          extra="string"
          example="mysecretcode"
          description="A secret code used to obtain an OAuth token via the /oauth/token endpoint"
        />
      </Table>
    </Topic>

    <Topic noExamples>
      <Table
        name="Errors"
      >
        <Cell
          name="Incorrect parameters supplied."
          description={
            `You did not supply a client_id and a state in your request.`
          }
        />
        <Cell
          name="App does not exist for client id."
          description="You supplied an invalid client_id."
        />
        <Cell
          name="No callback URL set for this app."
          description={
            `You did not set a callback URL for your app.`
          }
        />
        <Cell
          name="UCL has sent incomplete headers"
          description={
            `UCL sent us incomplete headers. `
            + `If the issue persists, please contact the UCL API Team.`
          }
        />
      </Table>
    </Topic>
  </div>
)

export default Authorise

Authorise.propTypes = {
  activeLanguage: propTypes.string,
}

Authorise.defaultProps = {
  activeLanguage: `python`,
}

