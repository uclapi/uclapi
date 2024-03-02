import { useEffect, useState } from "react";
import styles from "@/styles/Dashboard.module.scss";

function AcceptableUsePolicy() {
  const [policy, setPolicy] = useState("");
  useEffect(() => {
    fetch(
      "https://raw.githubusercontent.com/uclapi/uclapi/master/backend/uclapi/uclapi/UCLAPIAcceptableUsePolicy.txt"
    )
      .then((res) => res.text())
      .then((res) => setPolicy(res));
  }, []);

  return (
    <div className={styles.aup} dangerouslySetInnerHTML={{ __html: policy }} />
  );
}

export default AcceptableUsePolicy;
