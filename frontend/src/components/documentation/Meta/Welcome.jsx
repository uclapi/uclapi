import React from 'react'
import Topic from '../Topic'

const Welcome = () => {
  return (
    <Topic
      noExamples
    >
      <h1 id="welcome">Welcome</h1>
      <p>Yay, you made it! 🎉</p>

      <p>
        Welcome to the documentation for UCL’s brand new open API.
        Each service is listed below with examples in three different
        programming languages (Shell script using cURL, Python and JavaScript)
        to help you get going as quickly as possible.
      </p>

      <p>
        The API will be made up of several services,
        each of which will be separately explained.
        Every service will be documented here with important information,
        tips and examples.
      </p>

      <h2 id="get-api-key">Get Your API Key</h2>
      <p>
        Before you can use the API you should head to the API Dashboard
        and sign up using your UCL user account.
        Once logged into the dashboard simply name your app
        and you’ll be given a key that you can use to access all the services.
        Simple!
      </p>

      <h2 id="rate-limits">API Rate Limits</h2>
      <p>
        Rate limiting of the API is primarily on a per-user basis.
        The limit is calculated against the user,
        across all their access tokens.
      </p>
      <p>
        The limit is 10,000 requests per day and resets every day
        at midnight, London time.
      </p>
      <p>
        When a request is throttled, the response returned by the server
        has HTTP Status Code “429 Too Many Requests”.
        It includes a Retry-After header with the number of seconds
        the client is throttled for.
      </p>
      <p>
        If you would like your rate limit to be increased,
        contact us at&nbsp;
        <a href="mailto:isd.apiteam@ucl.ac.uk">isd.apiteam@ucl.ac.uk</a>
      </p>

      <h2 id="expiry-times">API Data Freshness</h2>
      <p>
        Much of the data available from the API is served from cache.
        Bookings and Timetable data are updated every twenty minutes from UCL,
        and we update the&nbsp;
        <a href="#workspaces">Library Study Spaces (Workspaces) API</a>
        &nbsp;every two minutes.
        The <code>Last-Modified</code> header will provide the time that
        the most recent caching operation completed in&nbsp;
        <a href="https://stackoverflow.com/a/21121453">RFC 2616</a>
        &nbsp;format.
        Endpoints that do not rely on cached data will return the
        current timestamp in this field instead.
      </p>
      <p>
        This allows your application to judge whether the data is stale,
        or might need refreshing.
        For example, if a booking is added to the database and the data
        you are using is more than twenty minutes old, it may be that the
        booking is not visible to you yet.
        Consider creating a fresh request in this case.
      </p>
      <p>
        If you notice that the <code>Last-Modified</code> timestamp you see
        is unreasonably old, please&nbsp;
        <a href="mailto:isd.apiteam@ucl.ac.uk">get in contact with us</a>
        &nbsp;ASAP to report this
        as it may indicate very stale data and an issue at our end.
      </p>
    </Topic>
  )
}

export default Welcome