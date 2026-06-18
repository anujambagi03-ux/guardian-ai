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

  const [temporal, setTemporal] = useState({
    peak_hour: 0,
    peak_risk_score: 0,
    high_risk_hours: [] as number[],
  });

  const [predictive, setPredictive] = useState({
    total_predictions: 0,
    high_risk_predictions: 0,
    average_confidence: 0,
  });

  const loadMonitoring = () => {
    api
      .get("/monitoring/live")
      .then((response) => {
        setData(response.data);
      })
      .catch(console.error);
  };

  const loadTemporal = () => {
    api
      .get("/temporal/analytics")
      .then((response) => {
        setTemporal(response.data);
      })
      .catch(console.error);
  };

  const loadPredictive = () => {
    api
      .get("/predictive/analytics")
      .then((response) => {
        setPredictive(response.data);
      })
      .catch(console.error);
  };

  useEffect(() => {
    loadMonitoring();
    loadTemporal();
    loadPredictive();

    const interval = setInterval(() => {
      loadMonitoring();
      loadTemporal();
      loadPredictive();
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

      <div className="row mt-4 g-4">

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

              <h5>{data.last_updated}</h5>

            </div>
          </div>
        </div>

      </div>

      <hr className="my-5" />

      <h2 className="mb-4">
        🧠 AI Intelligence Dashboard
      </h2>

      <div className="row g-4">

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>⏰ Peak Hour</h5>
              <h2>{temporal.peak_hour}:00</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>⚠ Peak Risk Score</h5>
              <h2>{temporal.peak_risk_score}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🔥 High Risk Hours</h5>
              <h2>
                {temporal.high_risk_hours.length}
              </h2>
            </div>
          </div>
        </div>

      </div>

      <div className="row g-4 mt-2">

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>📈 Predictions</h5>
              <h2>
                {predictive.total_predictions}
              </h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🎯 Confidence</h5>
              <h2>
                {predictive.average_confidence}%
              </h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h5>🚨 High Risk Predictions</h5>
              <h2>
                {predictive.high_risk_predictions}
              </h2>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Monitoring;