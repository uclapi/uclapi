import { Container } from "@/components/layout/Items.jsx";
import React from "react";
import styles from "./AnalyticInfo.module.scss";

/**
REQUIRED ATTRIBUTES:
this.props.analytic (key for the analytic to display)
this.props.value (value for this analytic data point)
**/

const getFriendlyText = (key) => {
  switch (key) {
    case "remaining_quota":
      return "Remaining Quota";
    case "requests":
      return "Requests";
    case "users":
      return "Users";
    default:
      return key;
  }
};

const AnalyticInfo = ({ analytic, value }) => {
  return (
    <Container className={styles.analyticInfoRow} noPadding>
      <div>{getFriendlyText(analytic)}</div>
      <p>{value}</p>
    </Container>
  );
};

export default AnalyticInfo;
