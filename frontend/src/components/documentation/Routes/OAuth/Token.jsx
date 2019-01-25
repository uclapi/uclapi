import React from 'react';

import Topic from './../../Topic.jsx';
import Table from './../../Table.jsx';
import Cell from './../../Cell.jsx';


let codeExamples = {
  python: `import requests

params = {
  "client_id": "123.456",
  "code": "1",
  "client_secret": "secret",
}
r = requests.get("https://uclapi.com/oauth/token", params=params)
print(r.json())`,

  shell: `curl -G https://uclapi.com/oauth/token \
-d code=mysecretcode \
-d client_id=123.456
-d client_secret=secret`,

  javascript: `fetch("https://uclapi.com/oauth/token?code=mysecretcode&client_id=123.456&client_secret=secret")
.then((response) => {
  return response.json()
})
.then((json) => {
  console.log(json);
})`
}

let response = `{
    "scope": "[]",
    "state": "1",
    "ok": true,
    "client_id": "123.456",
    "token": "uclapi-user-abc-def-ghi-jkl",
}
`

let responseCodeExample = {
  python: response,
  javascript: response,
  shell: response
}


export default class Token extends React.Component {

    render () {
      return (
        <div>
          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={codeExamples}>
            <h1 id="oauth/token">Token</h1>
            <p>
              Endpoint: <code>https://uclapi.com/oauth/token</code>
            </p>

            <Table
              name="Query Parameters">
              <Cell
                name="client_id"
                requirement="required"
                example="123.456"
                description="Client ID of the authenticating app." />
              <Cell
                name="code"
                requirement="required"
                example="mysecretcode"
                description="Secret code obtained from the authorise endpoint." />
              <Cell
                name="client_secret"
                requirement="required"
                example="mysecret"
                description="Client secret of the authenticating app." />
            </Table>
          </Topic>

          <Topic
            activeLanguage={this.props.activeLanguage}
            codeExamples={responseCodeExample}>
            <h2>Response</h2>
            <p>
              Redirection to authorise page.
            </p>
          </Topic>

          <Topic
            noExamples={true}>
            <Table
              name="Errors">
              <Cell
                name="The client did not provide requisite data to get the token."
                description="Gets returned when you have not supplied a client_id, code, client_secret in your request." />
              <Cell
                name="The code received was invalid, or has expired. Please try again."
                description="As error message." />
              <Cell
                name="Client secret incorrect."
                description="Gets returned when the client secret was incorrect." />
              </Table>
          </Topic>
        </div>
      )
    }

}
