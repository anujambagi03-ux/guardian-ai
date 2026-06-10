import { useEffect, useState } from "react";
import api from "../services/api";

function Monitoring() {
  const [data, setData] = useState({
    total_vehicles: 0,
    total_violations: 0,
    total_accidents: 0,
    total_alerts: 0,
    risk_status: "LOW",
    last_updated: "",
  });

  const loadMonitoring = () => {
    api
      .get("/monitoring/live")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  useEffect(() => {
    loadMonitoring();

    const interval = setInterval(() => {
      loadMonitoring();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container-fluid">

      <h1 className="mb-4 fw-bold">
        📡 Real-Time Monitoring Center
      </h1>

      <div className="row g-4">

        <div className="col-md-3">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🚗 Vehicles</h5>
              <h1>{data.total_vehicles}</h1>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🚨 Violations</h5>
              <h1>{data.total_violations}</h1>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🚑 Accidents</h5>
              <h1>{data.total_accidents}</h1>
            </div>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🔔 Alerts</h5>
              <h1>{data.total_alerts}</h1>
            </div>
          </div>
        </div>

      </div>

      <div className="row mt-4">

        <div className="col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">

              <h4>Risk Status</h4>

              <h1
                className={
                  data.risk_status === "HIGH"
                    ? "text-danger"
                    : "text-success"
                }
              >
                {data.risk_status}
              </h1>

            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">

              <h4>Last Updated</h4>

              <h5>
                {data.last_updated}
              </h5>

            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Monitoring;