import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

function Documentation() {
  const [loaded, setLoaded] = useState(false)
  useEffect(() => {
    import("openapi-explorer/dist/es/openapi-explorer.js").then(() => setLoaded(true));
  }, []);

  return (
    <div className="vertical-padding">
      {loaded &&
        <openapi-explorer
          server-url="https://uclapi.com"
          spec-url="/uclapi.openapi.json"
        />
      }
    </div>
  );
}

export default dynamic(() => Promise.resolve(Documentation), { ssr: false });
