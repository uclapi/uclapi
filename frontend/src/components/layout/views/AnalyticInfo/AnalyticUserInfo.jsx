import { Container, AnalyticInfo } from 'Layout/Items.jsx'
import React  from 'react'
import './AnalyticInfo.scss'

/**
REQUIRED ATTRIBUTES:
this.props.users (total number of users)
this.props.usersPerDept (array of Objects with `department` and `count` fields)
**/

const cleanDepartment = dept => dept.replace(`Dept of `, ``)

const AnalyticUserInfo = ({
  users,
  usersPerDept,
}) => {
  return (
    <Container noPadding>
      <AnalyticInfo analytic='users' value={users} />
      {users > 0 && (
        <Container className="analytic-info-row" noPadding>
          <div>Users by dept.</div>
          <div className='analytic-user-dept'>
            {usersPerDept.map((dept, index) =>
              <AnalyticInfo
                key={index}
                analytic={cleanDepartment(dept.department)}
                value={dept.count}
                height='initial'
              />
            )}
          </div>
        </Container>
      )}
    </Container>
  )
}

export default AnalyticUserInfo
