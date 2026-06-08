import { useEffect, useState } from "react";
import api from "../services/api";

const Dashboard = () => {
  const [data, setData] = useState({
    total_vehicles: 0,
    detected_violations: 0,
    accident_alerts: 0,
  });

  useEffect(() => {
    api
      .get("/dashboard")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("API Error:", error);
      });
  }, []);

  return (
    <div className="container-fluid">

      <h1 className="mb-4">🚦 Guardian AI Dashboard</h1>

      {/* KPI Cards */}

      <div className="row g-4">

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6 className="text-muted">Total Vehicles</h6>
              <h2>{data.total_vehicles}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6 className="text-muted">Detected Violations</h6>
              <h2>{data.detected_violations}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6 className="text-muted">Accident Alerts</h6>
              <h2>{data.accident_alerts}</h2>
            </div>
          </div>
        </div>

      </div>

      {/* Monitoring Section */}

      <div className="row mt-4">

        <div className="col-lg-6">
          <div className="card shadow border-0">
            <div className="card-body">
              <h4>Recent Alerts</h4>

              <ul className="list-group mt-3">

                <li className="list-group-item">
                  🚗 Overspeeding detected at Junction A
                </li>

                <li className="list-group-item">
                  🚦 Signal jump detected
                </li>

                <li className="list-group-item">
                  ⚠ Accident alert received
                </li>

              </ul>

            </div>
          </div>
        </div>

        <div className="col-lg-6">
          <div className="card shadow border-0">
            <div className="card-body">
              <h4>System Health</h4>

              <div className="mt-3">

                <p>
                  Backend Status:
                  <span className="badge bg-success ms-2">
                    Online
                  </span>
                </p>

                <p>
                  AI Detection Engine:
                  <span className="badge bg-success ms-2">
                    Running
                  </span>
                </p>

                <p>
                  Database:
                  <span className="badge bg-warning text-dark ms-2">
                    Coming Soon
                  </span>
                </p>

              </div>

            </div>
          </div>
        </div>

      </div>

      {/* Traffic Overview */}

      <div className="row mt-4">

        <div className="col-12">

          <div className="card shadow border-0">

            <div className="card-body">

              <h4>Traffic Overview</h4>

              <table className="table table-striped mt-3">

                <thead>
                  <tr>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Traffic Density</th>
                  </tr>
                </thead>

                <tbody>

                  <tr>
                    <td>Junction A</td>
                    <td>Normal</td>
                    <td>Medium</td>
                  </tr>

                  <tr>
                    <td>Junction B</td>
                    <td>Congested</td>
                    <td>High</td>
                  </tr>

                  <tr>
                    <td>Junction C</td>
                    <td>Clear</td>
                    <td>Low</td>
                  </tr>

                </tbody>

              </table>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
};

export default Dashboard;