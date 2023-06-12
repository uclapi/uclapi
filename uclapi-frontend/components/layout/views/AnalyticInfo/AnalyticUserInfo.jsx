import { Container, AnalyticInfo } from "@/components/layout/Items.jsx";
import React from "react";
import styles from "./AnalyticInfo.module.scss";

/**
REQUIRED ATTRIBUTES:
this.props.users (total number of users)
this.props.usersPerDept (array of Objects with `department` and `count` fields)
**/

const cleanDepartment = (dept) => dept.replace("Dept of ", "");

const AnalyticUserInfo = ({ users, usersPerDept }) => {
  return (
    <Container noPadding>
      <AnalyticInfo analytic="users" value={users} />
      {users > 0 && (
        <Container className={styles.analyticInfoRow} noPadding>
          <div>Users by dept.</div>
          <div className={styles.analyticUserDept}>
            {usersPerDept.map((dept, index) => (
              <AnalyticInfo
                key={index}
                analytic={cleanDepartment(dept.department)}
                value={dept.count}
                height="initial"
              />
            ))}
          </div>
        </Container>
      )}
    </Container>
  );
};

export default AnalyticUserInfo;
