export const endpoints = [
  {
    name: `/oauth`,
    description: `Let your users sign in with their UCL credentials`,
    link: `/docs#operations-tag-OAuth`,
  },
  {
    name: `/roombookings`,
    description: `Get details of all bookable rooms at UCL`,
    link: `/docs#operations-tag-Room_Bookings`,
  },
  {
    name: `/search`,
    description: `Find people at UCL`,
    link: `/docs#operations-tag-Search`,
  },
  {
    name: `/timetable`,
    description: `Access personal and module timetables`,
    link: `/docs#operations-tag-Timetable`,
  },
  {
    name: `/resources`,
    description: `Find out how many UCL desktops are free`,
    link: `/docs#operations-tag-Resources`,
  },
  {
    name: `/workspaces`,
    description: `See how busy the libraries are right now`,
    link: `/docs#operations-tag-Workspaces`,
  },
  {
    name: `/libcal`,
    description: `Manage and make seat reservations on the library booking system`,
    link: `/docs#operations-tag-LibCal`,
  },
  {
    name: `/analytics`,
    description: `View analytics and stats about your app or API service`,
    link: `/docs#operations-tag-Analytics`,
  },
]

const linkclass = `alt-text color-transition default-transition`

export const FAQ = [
  {
    'question': `What is UCL API?`,
    'answer': (
      <>
        <p>
          UCL API is a platform for interacting with data that is usually
          difficult to obtain or hidden in internal UCL systems. The aim is to
          enable student developers to develop tools for other UCL students to
          enrich their lives at UCL. Almost every API returns JSON which is
          simple to parse and interpret in most modern programming languages.
        </p>
        <p>
          It is student-built platform, backed and supported by UCL&apos;s&nbsp;
          <a className={linkclass} href="https://www.ucl.ac.uk/isd/">
            Information Services Division (ISD)
          </a>
          . This means that all of the features in UCL API
          have been developed by
          students and are aimed at students such as yourself, so jump right in!
      </p>
      </>
    ),
  },
  {
    'question': `Do I need to be from UCL to use the UCL API?`,
    'answer': (
      <p>
        You need to be affiliated with UCL because authentication (for both
       developers &amp; end users) is done via the UCL login system.
      </p>
    ),
  },
  {
    'question': `How do I get involved?`,
    'answer': (
      <p>
        UCL API is open source. Our source code is available on&nbsp;
        <a className={linkclass} href="https://github.com/uclapi/uclapi">
          a public Github repository
        </a>
        &nbsp;for anybody to clone and inspect.
        Find an bug? Feel free to open an&nbsp;
        <a className={linkclass} href="https://github.com/uclapi/uclapi/issues">
          Issue
        </a>
        &nbsp;or even a&nbsp;
        <a className={linkclass} href="https://github.com/uclapi/uclapi/pulls">
          Pull Request
        </a>
        &nbsp;with a proposed fix!
        We also have annual hiring windows to recruit more
        students as others graduate, so keep an
        eye on our social media accounts.
      </p>
    ),
  },
  {
    'question': `Does this cost anything?`,
    'answer': (
      <p>UCL API is and always will be completely free to use.</p>
    ),
  },
  {
    'question': `Who owns the Intellectual Property (IP) of what I build?`,
    'answer': (
      <p>
        You do! We have no claim on your IP. However, we do request you include
        a shoutout somewhere. This helps raise awareness of UCL API and the vast
        amount of data available. It may not always be possible to include this
        attribution in an unintrusive manner (e.g. in a Slack bot), so
        we&apos;re flexible on this. The more people aware of UCL API and who
        use apps powered by UCL API, the better the platform will be. If you
        have any questions please feel free to reach out!
      </p>
    ),
  },
]

export default {
  FAQ,
  endpoints,
}
