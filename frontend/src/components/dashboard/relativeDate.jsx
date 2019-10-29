import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import utc from 'dayjs/plugin/utc'
import PropTypes from 'prop-types'
import React from 'react'

dayjs.extend(utc)
dayjs.extend(relativeTime)

class RelativeDate extends React.Component {
  static propTypes = {
    date: PropTypes.string,
    label: PropTypes.string,
  }

  constructor(props) {
    super(props)

    /*
      Make day.js say 'just now' if the time difference is less
      than five seconds either way to get round non-sync'd server and
      client time.
      This may make 'a few seconds ago' somewhat redundant, but it's
      worth it.
    */
    dayjs.prototype.fromNowOrNow = function (a) {
      console.log(this)
      if (Math.abs(dayjs().diff(this)) < 5000) {
        return `just now`
      }
      return this.fromNow(a)
    }
  }

  render() {
    const { date, label } = this.props
    return (
      <div title={dayjs.utc(date).local().format(`dddd, D MMMM YYYY, h:mm:ss a`)}>
        {label} {dayjs.utc(date).local().fromNowOrNow()}
      </div>
    )
  }
}

export default RelativeDate
