import React from 'react';

import Topic from './../Topic.jsx';


export default class Welcome extends React.Component {

    render () {
      return (
        <Topic
          noExamples={true}>
          <h1 id="welcome">Welcome</h1>
          <p>Yay, you made it! 🎉</p>

          <p>Welcome to the documentation for UCL’s brand new open API. Each service is listed below with examples in three different programming languages (Shell script using cURL, Python and JavaScript) to help you get going as quickly as possible.</p>

          <p>The API will be made up of several services, each of which will be separately versioned and explained. Every service will be documented here with important information, tips and examples.</p>

          <h2 id="get-api-key">Get Your API Key</h2>
          <p>
            Before you can use the API you should head to the API Dashboard and sign up using your UCL user account. Once logged into the dashboard simply name your app and you’ll be given a key that you can use to access all the services. Simples!
          </p>

          <h2 id="api-rate-limits">API Rate Limits</h2>
          <p>
            Rate limiting of the API is primarily on a per-user basis. The limit is calculated against user’s ID (e-mail) across all access tokens.
          </p>
          <p>
            The limit is 10 000 requests per day and resets every day midnight London time. (00:00 GMT)
          </p>
          <p>
            When a request is throttled, the response returned by the server has HTTP Status Code “429 Too Many Requests”. It includes a Retry-After header with the number of seconds the client is throttled for.
          </p>
          <p>
            If you would like your rate limit to be increased, contact us at isd.apiteam@ucl.ac.uk
          </p>

          <h2 id="api-expiry-times">API Data Freshness</h2>
          <p>
            Data from the API is cached on the server. The date when this cache happened is stored in the Last-Modified header.
          </p>
          <p>
            This allows you to judge if you think the data is stale or not. Therefore allowing you to know if you have the most recent bookings for example or if there might be ones not in the most recent cache.
          </p>
          <p>
            If you notice this date is severly out of date, please let us know at isd.apiteam@ucl.ac.uk.
          </p>
        </Topic>
      )
    }

}
