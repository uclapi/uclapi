const {
  location: {
    protocol,
    hostname,
    port,
  },
} = window

const DOMAIN = `${protocol}//${hostname}${(port && port !== `80`) ? `:${port}` : ``}`

export default {
  DOMAIN,
}