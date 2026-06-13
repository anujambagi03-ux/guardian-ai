import { useEffect, useState } from "react";
import axios from "axios";

function VehicleDetection() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [detections, setDetections] = useState<any[]>([]);

  const loadAnalytics = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/cv/analytics"
      );

      setAnalytics(response.data);
    } catch (error) {
      console.error("Analytics Error:", error);
    }
  };

  const loadDetections = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/cv/detections"
      );

      console.log("DETECTIONS DATA:");
      console.log(response.data);

      setDetections(response.data);
    } catch (error) {
      console.error("Detection Error:", error);
      setDetections([]);
    }
  };

  const simulateDetection = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/cv/simulate"
      );

      await loadAnalytics();
      await loadDetections();
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadAnalytics();
    loadDetections();
  }, []);

  return (
    <div>
      <h2 className="mb-4">
        Vehicle Detection Center
      </h2>

      <button
        className="btn btn-primary mb-4"
        onClick={simulateDetection}
      >
        Simulate Detection
      </button>

      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Total Frames</h5>
            <h2>{analytics?.total_frames || 0}</h2>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Total Vehicles</h5>
            <h2>{analytics?.total_vehicles || 0}</h2>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Average Vehicles</h5>
            <h2>{analytics?.average_vehicles || 0}</h2>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card p-3 text-center">
            <h5>Risk Level</h5>
            <h2>{analytics?.risk_level || "LOW"}</h2>
          </div>
        </div>
      </div>

      <div className="card p-4">
        <h3 className="mb-4 text-center">
          Detection History
        </h3>

        <table className="table table-striped table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Frame ID</th>
              <th>Vehicle Count</th>
              <th>Timestamp</th>
            </tr>
          </thead>

          <tbody>
            {detections && detections.length > 0 ? (
              detections.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.frame_id}</td>
                  <td>{item.vehicle_count}</td>
                  <td>{item.timestamp}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={4}
                  className="text-center"
                >
                  No detections found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default VehicleDetection;