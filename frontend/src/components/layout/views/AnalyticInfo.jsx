import { Container } from 'Layout/Items.jsx'
import React  from 'react'

/**
REQUIRED ATTRIBUTES:
this.props.analytic (key for the analytic to display)
this.props.value (value for this analytic data point)
**/

const getFriendlyText = (key) => {
  switch (key) {
    case `remaining_quota`: return `Remaining Quota`
    case `requests`: return `Requests`
    case `users`: return `Users`
    case `users_per_dept`: return `Users by Dept.`
    default: return key
  }
}

const AnalyticInfo = ({
  analytic,
  value,
}) => {
  return (
    <Container
      className="checkbox"
      height={`55px`}
      noPadding
    >
      <div className="field-label">{getFriendlyText(analytic)}</div>
      <p>{value}</p>
    </Container>
  )
}

export default AnalyticInfo