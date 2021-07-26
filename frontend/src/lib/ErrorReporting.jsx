import * as Sentry from '@sentry/react'
import { Integrations } from '@sentry/tracing'

if (process.env.NODE_ENV === `production` && process.env.SENTRY_DSN_REACT) {
  Sentry.init({
    dsn: process.env.SENTRY_DSN_REACT,
    environment: process.env.SENTRY_DSN_ENV,
    integrations: [
      new Integrations.BrowserTracing(),
    ],
    tracesSampleRate: 0.01,
  })
}



